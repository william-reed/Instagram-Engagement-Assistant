from sqlalchemy imoprt create_engine
from sqlalchemy.orm import sessionmaker

from InstagramApi import InstagramApi

import logging
import sys
import config
import models

# expects to be run as 'python scraper.py user1 user2 ...'

if __name__ == "__main__":
	logger = logging.getLogger("insta_engagement_scraper")
	logger.setLevel(config.DEBUG_LEVEL)

	# gather arguments
	if len(sys.argv == 1):
		logger.error("No input arguments supplied")
		logger.error("Try running as 'python scraper.py <user1> <user2> ...")
		logger.error("Goodbye")
		logger.shutdown()
		exit(1)

	# first arg is program name so we don't care about that, just the rest
	users = str(sys.argv)[1:]
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
	InstagramApi = InstagramAPI(config.INSTA_USER, config.INSTA_PASS)
	InstagramApi.login()

	###########################################################################
	## Processing
	###########################################################################
	init_scan()
	user_pks = fetch_users(users, InstagramApi)



def init_scan():

def fetch_users(usernames, api):
	"""
	Fetch the user objects from the api for the given usernames and insert them into the DB
	:usernames The list of usernames to look at
	:api The instagram API
	:returns list of pk's of the given usernames.
	"""
	pks = []
	for username in usernames:
		api.getInfoByName(username.strip())
		user = api.LastJson["user"];
		instagram_user = Instagram_User(instagram_user_id = user["pk"],
		 username=user["username"],
		 followers=user['follower_count'],
		 following=user['following_count'],
		 is_business=user['is_business'],
		 is_private=user['is_private'])

		pk.append(instagram_user.instagram_user_id)

		Logger.debug("Got user info for '" + username + "'")
		# can't make requests too fast
		time.sleep(config.SLEEP_TIME)

	Logger.debug("Gatered users committed to database")
	session.commit()
	return pks
