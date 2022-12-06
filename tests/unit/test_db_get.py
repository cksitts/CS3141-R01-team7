from app.python import databaseAccess as db
from app.python.helper import generateHashAndSalt
from flask.testing import FlaskClient
from typing import Tuple
from time import time
import logging
log = logging.getLogger(__name__)

# methods to test:
# validLogin (done)
# getLaundryRooms (done)
# getLocations (done)
# getAllMachines (done)
# getUsernameFromEmail (done)
# getUserData (done)
# getUserMachines (done)

def test_db_validLogin(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    _hash, salt = generateHashAndSalt('testPass')
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'testUser', NULL, %s, %s); ''', (_hash, salt))
    assert db.validLogin('testUser', 'testPass')
    assert db.validLogin('user@gmail.com', 'testPass')
    assert not db.validLogin('fakeUser', 'testPass')
    assert not db.validLogin('testUser', 'fakePass')

def test_db_getLaundryRooms(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO Machine VALUES ('501E_WH_1', 'Hall 1', 'Washer'), ('502E_WH_1', 'Hall 2', 'Washer'), ('502E_WH_2', 'Hall 2', 'Washer'); ''')
    result = db.getLaundryRooms()
    assert '501E Wads (Hall 1)', '502E Wads (Hall 2)' in result

def test_db_getLocations(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO Machine VALUES ('501E_WH_1', 'Hall 1', 'Washer'), ('502E_WH_1', 'Hall 2', 'Washer'), ('502E_WH_2', 'Hall 2', 'Washer'); ''')
    result = db.getLocations()
    assert 'Hall 1', 'Hall 2' in result

def test_db_getAllMachines(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO Machine VALUES ('501E_WH_1', 'Hall 1', 'Washer'), ('502E_WH_1', 'Hall 2', 'Washer'), ('502E_WH_2', 'Hall 2', 'Washer'); ''')
    result = db.getAllMachines()
    assert {'machine-id': '501E_WH_1', 'machine-type': 'Washer', 'location': 'Hall 1', 'username': 'None', 'time-remaining': 0, 'available': True} in result
    assert {'machine-id': '502E_WH_1', 'machine-type': 'Washer', 'location': 'Hall 2', 'username': 'None', 'time-remaining': 0, 'available': True} in result
    assert {'machine-id': '502E_WH_2', 'machine-type': 'Washer', 'location': 'Hall 2', 'username': 'None', 'time-remaining': 0, 'available': True} in result

def test_db_getUsernameFromEmail(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    _hash, salt = generateHashAndSalt('testPass')
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'testUser', NULL, %s, %s); ''', (_hash, salt))
    assert db.getUsernameFromEmail('user@gmail.com') == 'testUser'

def test_db_getUserData(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    _hash, salt = generateHashAndSalt('testPass')
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'testUser', NULL, %s, %s); ''', (_hash, salt))
    assert db.getUserData('testUser') == {'email':'user@gmail.com', 'username':'testUser', 'preferredRoom':None}
    assert db.getUserData('fakeUser') is None

def test_db_getUserMachines(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    _hash, salt = generateHashAndSalt('testPass')
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'testUser', NULL, %s, %s); ''', (_hash, salt))
    cursor.execute(''' INSERT INTO Machine VALUES ('501E_WH_1', 'Hall 1', 'Washer'), ('502E_WH_1', 'Hall 2', 'Washer'), ('502E_WH_2', 'Hall 2', 'Washer'); ''')
    cursor.execute(''' INSERT INTO UsingMachine VALUES ('501E_WH_1', 'user@gmail.com', 'testUser', %i); ''' % (int(time())-1800))
    assert {'machine-id':'501E_WH_1', 'machine-type':'Washer', 'location':'Hall 1', 'time-remaining':30} in db.getUserMachines('testUser')
    