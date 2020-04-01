import subprocess
import psycopg2

class myDB():
	def connect():
		db_url = os.environ['HEROKU_POSTGRESQL_CYAN_URL']
		MY_DATABASE_URL = db_url[0:len(db_url)-1]
		conn = psycopg2.connect(MY_DATABASE_URL, sslmode='require')
		return conn


