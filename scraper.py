from sqlalchemy imoprt create_engine
from sqlalchemy.orm import sessionmaker

import logging
# TODO: import config and setup packages

if __name__ == "__main__":
	logger = logging.getLogger("insta_engagement_scraper")
	logger.setLevel(config.debug_level)

	engine = create_engine(config.db_connection)
	logger.debug("Database engine created")

	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	logger.debug("Database session binded to engine")

	# create tables if they don't exist
	Base.metadata.create_all(engine)
	logger.debug("Tables created / exist")