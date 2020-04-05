import psycopg2
import os
import subprocess
import sys
import random

class myDB():
 def connect():
  try:
   my_db_url = str(os.environ['HEROKU_POSTGRESQL_CYAN_URL'])
  except:
   process = subprocess.Popen(['heroku', 'config:get', 'HEROKU_POSTGRESQL_CYAN_URL'], stdout=subprocess.PIPE, universal_newlines=True)
   output = process.stdout.readline()
   my_db_url = output.strip()

  conn = psycopg2.connect(my_db_url, sslmode='require')
  return conn

 def randomValue(length):
     #salt_chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXVYZ!@#$%^&*()'
     salt_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
     return ''.join(random.choice(salt_chars) for x in range(length))
