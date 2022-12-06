from app.python import databaseAccess as db
from flask.testing import FlaskClient
from typing import Tuple
from time import time
import logging
log = logging.getLogger(__name__)

# methods to test:
# checkout (done)
# checkin (done)

def test_db_checkout(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'testUser', NULL, 'hash', 'salt'); ''')
    cursor.execute(''' INSERT INTO Machine VALUES ('501E_WH_1', 'Hall 1', 'Washer'); ''')
    assert db.checkout('501E_WH_1', 'fakeUser') == 1
    assert db.checkout('501E_WH_1', 'testUser') == 0
    cursor.execute(''' SELECT * FROM UsingMachine WHERE machine_id='501E_WH_1' AND email='user@gmail.com' AND username='testUser'; ''')
    assert len(cursor.fetchall()) != 0


def test_db_checkin(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'testUser', NULL, 'hash', 'salt'); ''')
    cursor.execute(''' INSERT INTO Machine VALUES ('501E_WH_1', 'Hall 1', 'Washer'); ''')
    cursor.execute(''' INSERT INTO UsingMachine VALUES ('501E_WH_1', 'user@gmail.com', 'testUser', %i); ''' % (int(time())-3600))
    assert db.checkin('501E_WH_1', 'testUser') == 0
    cursor.execute(''' SELECT * FROM UsingMachine WHERE machine_id='501E_WH_1' AND email='user@gmail.com' AND username='testUser'; ''')
    assert len(cursor.fetchall()) == 0