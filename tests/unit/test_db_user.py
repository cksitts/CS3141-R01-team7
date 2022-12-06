from app.python import databaseAccess as db
from flask.testing import FlaskClient
from typing import Tuple
import logging
log = logging.getLogger(__name__)

# methods to test:
# checkEmailAndUsernameTaken (done)
# registerUser (done)
# deleteUser (done)

def test_db_checkEmailAndUsernameTaken(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('taken@gmail.com', 'taken', NULL, 'hash', 'salt'); ''')
    assert db.checkEmailAndUsernameTaken('nottaken@gmail.com', 'nottaken') == 0
    assert db.checkEmailAndUsernameTaken('taken@gmail.com', 'nottaken') == 1
    assert db.checkEmailAndUsernameTaken('nottaken@gmail.com', 'taken') == 2
    assert db.checkEmailAndUsernameTaken('taken@gmail.com', 'taken') == 3

def test_db_registerUser(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    db.registerUser({'email':'test@gmail.com', 'username':'testUser', 'password':'testPass', 'preferredRoom':None})
    cursor.execute(''' SELECT * FROM MachineUser WHERE email='test@gmail.com' AND username='testUser'; ''')
    assert len(cursor.fetchall()) != 0

def test_db_deleteUser(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('test@gmail.com', 'testUser', NULL, 'hash', 'salt'); ''')
    db.deleteUser('test@gmail.com')
    cursor.execute(''' SELECT * FROM MachineUser WHERE email='test@gmail.com'; ''')
    assert len(cursor.fetchall()) == 0