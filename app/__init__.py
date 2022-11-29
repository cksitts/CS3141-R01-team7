from flask import Flask
import mysql.connector as conn

import os

# define the flask instance and create a secret key for the webpage
l_app = Flask(__name__)
l_app.secret_key = os.environ.get('TSP_SECRET_KEY')


# create the mysql parent object
# use the local db if this is true
use_local_database = False

if (use_local_database):
    mysql = conn.connect(   user='root', 
                            password=os.environ.get('TSP_DB_PASS'),
                            host='localhost',
                            port=3306,
                            database='laundry_tracker_db'   )
else:
    mysql = conn.connect(   user='flask', 
                            password=os.environ.get('TSP_DB_PASS'),
                            host=os.environ.get('TSP_DB_HOST'),
                            port=3306,
                            database='laundry_tracker_db',
                            ssl_ca='./etc/DigiCertGlobalRootCA.crt.pem',
                            ssl_disabled=False    )



from app import routes