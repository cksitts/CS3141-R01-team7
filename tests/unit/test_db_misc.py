from app.python import databaseAccess as db
from flask.testing import FlaskClient
from typing import Tuple
import logging
log = logging.getLogger(__name__)

# methods to test:
# addMachine (done)

def test_db_addMachine(test_client_with_db:Tuple[FlaskClient, any]):
    _, cursor = test_client_with_db
    assert db.addMachine('501E_WH_1', 'Hall 1', 'Washer') == 0
    assert db.addMachine('501E_WH_1', 'Hall 1', 'Washer') == 1 