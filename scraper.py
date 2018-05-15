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