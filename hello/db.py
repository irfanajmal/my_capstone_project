import psycopg2
import os
import subprocess

class myDB():
 def connect():
  try:
   my_db_url = str(os.environ['HEROKU_POSTGRESQL_CYAN_URL']) 
  except:
   db_url = subprocess.run(["heroku", "config:get", "HEROKU_POSTGRESQL_CYAN_URL"], capture_output=True)
   my_db_url = db_url.stdout.strip()

  conn = psycopg2.connect(my_db_url, sslmode='require')
  return conn

