from flask.testing import FlaskClient
from typing import Tuple
from werkzeug.datastructures import ImmutableMultiDict
import logging
log = logging.getLogger(__name__)

# methods to test:
# addMachines (done)

# ---Add Machines---
# GET, success message false
def test_add_machines_GET_success_false(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['admin'] = 1
    response = test_client.get('/addmachines', query_string={'successMessage':False})
    assert response.status_code == 200
    assert b'Add Machines' in response.data
    assert b'document.getElementById("pMessage").innerHTML = "Hello World"' not in response.data

# GET, success message not false
def test_add_machines_GET_success_true(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['admin'] = 1
    response = test_client.get('/addmachines', query_string={'successMessage':'Hello World'})
    assert response.status_code == 200
    assert b'Add Machines' in response.data
    assert b'document.getElementById("pMessage").innerHTML = "Hello World"' in response.data

# GET, machine already exists
def test_add_machines_GET_machine_exists(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['admin'] = 1
    response = test_client.get('/addmachines', query_string={'machineAlreadyExists':True})
    assert response.status_code == 200
    assert b'Add Machines' in response.data
    assert b'document.getElementById("pMessage").innerHTML = "That machine already exists"' in response.data

# GET, machine doesn't exist
def test_add_machines_GET_machine_not_exists(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['admin'] = 1
    response = test_client.get('/addmachines', query_string={'machineAlreadyExists':False})
    assert response.status_code == 200
    assert b'Add Machines' in response.data
    assert b'document.getElementById("pMessage").innerHTML = "That machine already exists"' not in response.data

# POST, machine already exists
def test_add_machines_POST_machine_exists(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['admin'] = 1
    cursor.execute(''' INSERT INTO Machine VALUES ('500E_WH_1', 'Test Hall', 'Washer'); ''')
    response = test_client.post('/addmachines', data=ImmutableMultiDict([
        ('roomNumber', '500E'),
        ('building', 'WH'),
        ('machineNum', 1),
        ('location', 'Test Hall'),
        ('machineType', 'Washer')
    ]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/addmachines?machineAlreadyExists=True' in response.data

# POST, successful add
def test_add_machines_POST_success(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['admin'] = 1
    response = test_client.post('/addmachines', data=ImmutableMultiDict([
        ('roomNumber', '500E'),
        ('building', 'WH'),
        ('machineNum', 1),
        ('location', 'Test Hall'),
        ('machineType', 'Washer')
    ]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/addmachines?successMessage=500E_WH_1+added+successfully' in response.data