from flask import Flask
from flask_mysqldb import MySQL

# define the flask instance and create a secret key for the webpage
l_app = Flask(__name__)
l_app.secret_key = "b3mex0c5xd7^x8c/xdcv#xbfkBq1)xb4C`>xffqu"

# create the mysql parent object
mysql = MySQL(l_app)

l_app.config['MYSQL_HOST'] = 'localhost'
l_app.config['MYSQL_USER'] = 'root'
l_app.config['MYSQL_DB'] = 'laundry_tracker_db'
l_app.config['MYSQL_PASSWORD'] = 'MRy_0VE9ARuv2zgcgaeepw'

from app import routes