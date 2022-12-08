from dotenv import load_dotenv
import pytest
import mysql.connector as conn
import os
from app import create_app
from config import TestingConfig

@pytest.fixture(scope='function')
def test_client_with_db():
    load_dotenv('.env')
    flask_app = create_app(TestingConfig)
    
    flask_app.config['MYSQL'] = conn.connect(   user='root', 
                            password=os.environ.get('DB_PASS'),
                            host='localhost',
                            port=3306,
                            database='laundry_tracker_db'   )
    
    # Setup Database
    cursor = flask_app.config["MYSQL"].cursor()
    cursor.execute(''' SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE ''')
    cursor.execute(''' START TRANSACTION ''')
    cursor.execute(''' DROP DATABASE IF EXISTS laundry_tracker_test; ''')
    cursor.execute(''' CREATE DATABASE laundry_tracker_test; ''')
    cursor.execute(''' USE laundry_tracker_test;  ''')
    cursor.execute(''' create table MachineUser (	email varchar(64) primary key not null, 
                            username varchar(64) unique not null, 
                            preferred_room varchar(32),
                            pass_hash char(64) not null, 
                            pass_salt char(16) not null); ''')
    cursor.execute(''' create table Machine (	machine_id char(10) primary key not null, 
                            location varchar(32) not null,
                            machine_type char(8) not null ); ''')
    cursor.execute(''' create table UsingMachine (	machine_id char(10) primary key not null, 
                            email varchar(64) not null,
                            username varchar(64) not null, 
                            time_started numeric(15,0) not null default 0, 
                            foreign key (machine_id) references Machine(machine_id)
                            on update cascade
                            on delete cascade,
                            foreign key (email) references MachineUser(email)
                            on update cascade
                            on delete cascade,
                            foreign key (username) references MachineUser (username)
                            on update cascade
                            on delete cascade	); ''')
    cursor.execute(''' COMMIT ''')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield (testing_client, cursor)

    # Teardown Database
    if not cursor : cursor = flask_app.config["MYSQL"].cursor() 
    cursor.execute(''' DROP DATABASE laundry_tracker_test; ''')
    cursor.execute(''' COMMIT ''')
    cursor.close()

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestingConfig)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client