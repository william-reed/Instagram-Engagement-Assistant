import logging
import os

MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASS = os.environ['MYSQL_PASS']
MYSQL_URL = os.environ['MYSQL_URL']
DB_NAME = os.environ['ENGAGEMENT_DB']

DB_CONNECTION = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASS + '@' + MYSQL_URL + '/' + DB_NAME

DEBUG_LEVEL = logging.DEBUG

INSTA_USER = os.environ['INSTA_USER']
INSTA_PASS = os.environ['INSTA_PASS']