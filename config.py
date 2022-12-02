from dotenv import load_dotenv
import mysql.connector as conn
import os

class DefaultConfig():
    load_dotenv('.env')
    DEBUG = True
    TESTING = False
    LOCAL_DATABASE = True
    

    # Leave this alone, it sets the values automatically
    if(LOCAL_DATABASE):
        MYSQL = conn.connect(   user='root', 
                                password=os.environ.get('DB_PASS'),
                                host='localhost',
                                port=3306,
                                database='laundry_tracker_db'   )
    else:
        MYSQL = conn.connect(   user='flask', 
                                password=os.environ.get('DB_PASS'),
                                host=os.environ.get('DB_HOST'),
                                port=3306,
                                database='laundry_tracker_db',
                                ssl_ca='./etc/DigiCertGlobalRootCA.crt.pem',
                                ssl_disabled=False    )


class TestingConfig():
    load_dotenv('.env')
    DEBUG = True
    TESTING = True
    LOCAL_DATABASE = True