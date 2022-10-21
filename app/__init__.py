from flask import Flask
from flask_mysqldb import MySQL

import os

# define the flask instance and create a secret key for the webpage
l_app = Flask(__name__)
l_app.secret_key = os.environ.get('TSP_SECRET_KEY')

# create the mysql parent object
mysql = MySQL(l_app)

l_app.config['MYSQL_HOST'] = 'localhost'
l_app.config['MYSQL_USER'] = 'root'
l_app.config['MYSQL_DB'] = 'laundry_tracker_db'
l_app.config['MYSQL_PASSWORD'] = os.environ.get('TSP_DB_PASS')

from app import routes