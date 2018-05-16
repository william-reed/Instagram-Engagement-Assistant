import logging
import os

MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASS = os.environ['MYSQL_PASS']
MYSQL_URL = os.environ['MYSQL_URL']
DB_NAME = os.environ['ENGAGEMENT_DB']

# ALTER DATABASE engagement CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
DB_CONNECTION = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASS + '@' + MYSQL_URL + '/' \
	+ DB_NAME + '?charset=utf8mb4'

DEBUG_LEVEL = logging.DEBUG

INSTA_USER = os.environ['INSTA_USER']
INSTA_PASS = os.environ['INSTA_PASS']

# time in seconds to sleep between api calls
SLEEP_TIME = 5