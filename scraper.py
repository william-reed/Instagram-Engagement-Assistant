from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from InstagramAPI import InstagramAPI

from models import Scan, Instagram_User, Media, Comment, Interaction, Base

import logging
import sys
import config
import models
import time
import re

def fetch_users(usernames, caller_username, api, session, force_update=False):
	"""
	Fetch the user objects from the api for the given usernames and insert them into the DB.
	Records that a scan instance occured by the given user on each of the given usernames
	:usernames The list of usernames to look at.
	:caller_username The username that initiated the scan
	:api The instagram API
	:session the db session
	:force_update if true the queries will overide previous user entries in the db to update them
	:returns list of pk's of the given usernames.
	"""
	logger.info("Fetching users")

	api.getInfoByName(caller_username.strip())
	caller_user = api.LastJson["user"];
	caller_user_pk = caller_user["pk"]

	# need their user object too
	# TODO: just recycle this information from above
	usernames.insert(0, caller_username)
	time.sleep(config.SLEEP_TIME)

	pks = []

	for username in usernames:
		user_pk = fetch_user(username, api, session, force_update)

		if user_pk == None:
			continue

		if username != caller_username:

			pks.append(user_pk)

			# create scan row
			scan = Scan(instagram_user_id=user_pk, 
				initiated_by=caller_user_pk)
			session.add(scan)

	session.commit()
	logger.info("Gatered users committed to database")
	logger.info(pks)
	return pks

def fetch_user(username, api, session, force_update=False):
	"""
	Fetch this specific user from the api and add them to the db
	:username the insta username to get info about
	:api the instagram api
	:session the dbsession
	:returns the user pk
	"""
	try:
		api.getInfoByName(username.strip())
		user = api.LastJson["user"];
	except KeyError:
		# key error shows the user is not found
		logger.warn("User '" + username + "' not found")
		return

	user_pk = user["pk"]

	# does the DB contain the user_pk?
	# would demorgans make this more readable?
	if session.query(Instagram_User).get(user_pk) != None and not force_update:
		# just return the pk since we want to scan this users new posts but don't
		# want to update their information
		logger.debug(user["username"] + " already exists in DB. Not updating.")
		return user_pk

	instagram_user = Instagram_User(instagram_user_id = user["pk"],
	 username=user["username"],
	 followers=user['follower_count'],
	 following=user['following_count'],
	 is_business=user['is_business'],
	 is_private=user['is_private'])
	session.add(instagram_user)

	
	logger.debug(user["username"] + " row created")

	session.commit()
	# can't make requests too fast
	time.sleep(config.SLEEP_TIME)

	return user_pk


def fetch_media(user_pks, api, session, force_update=False):
	"""
	Fetch the media for these user pk's and isnert them into the DB
	:user_pks a list of instagram user primary keys
	:api The isntagram API
	:session the dbsession
	:force_update if true the queries will overide previous user entries in the db to update them
	:returns a list of media pk's
	"""
	logger.info("Fetching media")
	pks = []
	for user_pk in user_pks:
		api.getUserFeed(user_pk)
		media = api.LastJson["items"]

		# The user likely has more photos but I am not sure they are relevant
		# older photos leads to less currently relevant data

		# is medium the singular? probably not...
		for medium in media:
			media_pk = medium["pk"]

			pks.append(media_pk)

			# make sure pk not in db
			if session.query(Media).get(media_pk) != None and not force_update:
				# we still want to check for comments at this point so 
				# append the pk anyway
				continue
			
			is_picture = True if medium['media_type'] == 1 else False

			instagram_media = Media(media_id=media_pk,
				instagram_user_id=user_pk,
				is_picture=is_picture)
			session.add(instagram_media)

			logger.debug("Got media " + str(media_pk) + " for user " + str(user_pk))

		# can't make requests too fast
		time.sleep(config.SLEEP_TIME)
		session.commit()

	session.commit()
	logger.info("Gatered media committed to database")
	return pks


def fetch_comments(media_pks, api, session):
	"""
	Fetch the comments for each of the given media ids. Update the DB with these comments.
	If duplicate comment pk's exist - they are ignored. No reason to re process those
	:media_pks the media primary keys to scan
	:api the instagram api
	:session the db session
	:returns a set of users which exist in the comments for the given media picutres
	"""
	logger.info("Fetching comments")
	user_pks = set()

	for media_pk in media_pks:
		api.getMediaComments(str(media_pk))

		comments = api.LastJson["comments"]

		# check if there are more comments to fetch
		while api.LastJson["has_more_comments"]:
			logger.debug("Getting more comments for " + str(media_pk))
			# the next max id to send back

			# instagram must have retrofitted their api to backsupport so i have to extract like this
			server_cursor = re.findall('"([^"]*)"', api.LastJson["next_max_id"])[1]
			api.getMediaComments(str(media_pk), max_id=server_cursor)
			comments.extend(api.LastJson["comments"])

			# can't make requests too fast
			time.sleep(config.SLEEP_TIME)

		poster_id = session.query(Media).get(media_pk).instagram_user.instagram_user_id

		for comment in comments:
			comment_pk = comment["pk"]
			commenter_pk = comment["user_id"]

			# ignoring if they comment on their own post
			if commenter_pk == poster_id:
				continue

			# if in db already, ignore it. 
			if session.query(Comment).get(comment_pk) != None:
				continue

			# fetch the user now to avoid foreign key constraint issues
			fetch_user(comment["user"]["username"], api, session)

			user_pks.add(commenter_pk)
			instagram_comment = Comment(comment_id=comment_pk,
				media_id=media_pk,
				instagram_user_id=commenter_pk,
				text=comment["text"],
				type=comment["type"])
			session.add(instagram_comment)

			logger.debug("Got comment '" + comment["text"] + "' from user " + str(commenter_pk))

		# can't make requests too fast
		time.sleep(config.SLEEP_TIME)
		session.commit()

	session.commit()
	logger.info("Gatered comments committed to database")
	return user_pks

# expects to be run as 'python scraper.py calling_user user_to_scan_1 user_to_scan_2 ...'
logging.basicConfig(stream=sys.stdout, level=config.DEBUG_LEVEL)
logger = logging.getLogger("insta_engagement_scraper")
logger.setLevel(config.DEBUG_LEVEL)

# gather arguments
if not len(sys.argv) > 2:
	logger.error("No input arguments supplied")
	logger.error("Try running as 'python scraper.py calling_user_insta_name user_to_scan_1 user_to_scan_2 ...")
	logger.error("Goodbye")
	logging.shutdown()
	exit(1)

calling_username = str(sys.argv[1])
users = sys.argv[2:]
logger.info("Users loaded from input arguments")

engine = create_engine(config.DB_CONNECTION)
logger.debug("Database engine created")

DBSession = sessionmaker(bind=engine)
session = DBSession()
logger.debug("Database session binded to engine")

# create tables if they don't exist
Base.metadata.create_all(engine)
logger.debug("Tables created / exist")

# setup instagram
api = InstagramAPI(config.INSTA_USER, config.INSTA_PASS)
api.login()

###########################################################################
## Processing
###########################################################################
user_pks = fetch_users(users, calling_username, api, session)
media_pks = fetch_media(user_pks, api, session)
commenter_pks = fetch_comments(media_pks, api, session)

# cleanup
session.commit()
session.close()
api.logout()

logger.info("Exiting succesfully. Goodbye")
logging.shutdown()

# TODO
# Auto update if data older than a week?
# looks like sleeping is dropping ig connections
# auto setup charset
# securing passwords better than environ vars