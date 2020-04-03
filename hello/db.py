import psycopg2
import os
import subprocess

class myDB():
 def connect():
  try:
   db_url = str(os.environ['HEROKU_POSTGRESQL_CYAN_URL'])
  except:
   db_url = str(subprocess.run(["heroku", "config:get", "HEROKU_POSTGRESQL_CYAN_URL"])).strip()
   #db_url = 'postgres://rsbuhqmqigficf:652bd8fc4f26892df10cc924568a9698c53503351a202159356cc4f3292a962c@ec2-52-86-33-50.compute-1.amazonaws.com:5432/d8r5bdme8ltj0g'

  #MY_DATABASE_URL = db_url[0:len(db_url)-1]
  print (db_url)
  conn = psycopg2.connect(db_url, sslmode='require')
  return conn

