import logging
import os

mysql_user = os.environ['MYSQL_USER']
mysql_pass = os.environ['MYSQL_PASS']
mysql_url = os.environ['MYSQL_URL']
db_name = os.environ['ENGAGAMENT_DB']

db_conneciton = 'mysql://' + mysql_user + ':' + mysql_pass + '@' + mysql_url + '/' + livethread_db

debug_level = logging.DEBUG