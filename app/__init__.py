from flask import Flask
import mysql.connector as conn
import os


def db_setup(use_local_database):
    # create the mysql parent object
    if (use_local_database):
        mysql = conn.connect(   user='root', 
                                password=os.environ.get('DB_PASS'),
                                host='localhost',
                                port=3306,
                                database='laundry_tracker_db'   )
    else:
        mysql = conn.connect(   user='flask', 
                                password=os.environ.get('DB_PASS'),
                                host=os.environ.get('DB_HOST'),
                                port=3306,
                                database='laundry_tracker_db',
                                ssl_ca='./etc/DigiCertGlobalRootCA.crt.pem',
                                ssl_disabled=False    )
    return mysql




def create_app(config_class):
    # define the flask instance and load the config file
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = os.environ.get('SECRET_KEY')

    with app.app_context():
        #import routes.py
        from . import routes

        return app

    
