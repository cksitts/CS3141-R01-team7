from flask.testing import FlaskClient
from typing import Tuple
from werkzeug.datastructures import ImmutableMultiDict
import logging
log = logging.getLogger(__name__)
from app.python.helper import generateHashAndSalt

# methods to test:
# passwordReset (done)
# editAccount (done)
# deleteAccount (done)

# ---Password Reset---
# GET, valid login
def test_password_reset_GET_valid(test_client:FlaskClient):
    response = test_client.get('/passwordreset', query_string={'validLogin':True})
    assert response.status_code == 200
    assert b'Password Reset' in response.data
    assert b'That username is invalid.' not in response.data

# GET, invalid login
def test_password_reset_GET_invalid(test_client:FlaskClient):
    response = test_client.get('/passwordreset', query_string={'validLogin':False})
    assert response.status_code == 200
    assert b'Password Reset' in response.data
    assert b'That username is invalid.' in response.data

# POST, valid user
def test_password_reset_POST_valid(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    response = test_client.post('/passwordreset', data=ImmutableMultiDict([('usernameInput', 'username'),('passwordInput', 'password')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/verify' in response.data
    with test_client.session_transaction() as session:
        assert session.get('resetPass') is True
        assert session.get('inputCount') == 0
        assert session.get('validCode') is True

# POST, invalid user
def test_password_reset_POST_invalid(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.post('/passwordreset', data=ImmutableMultiDict([('usernameInput', 'username'),('passwordInput', 'password')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/passwordReset' in response.data
    with test_client.session_transaction() as session:
        assert session.get('username') is None

# ---Edit Account---
# GET, status code 1 (email error)
def test_edit_account_GET_status_1(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.get('/editaccount', query_string={'status_code':1})
    assert response.status_code == 200
    assert b'Edit Account' in response.data
    assert b'That email already has an account.' in response.data

# GET, status code 2 (username error)
def test_edit_account_GET_status_2(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.get('/editaccount', query_string={'status_code':2})
    assert response.status_code == 200
    assert b'Edit Account' in response.data
    assert b'That username already has an account.' in response.data

# GET, status code 3 (email and username error)
def test_edit_account_GET_status_3(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.get('/editaccount', query_string={'status_code':3})
    assert response.status_code == 200
    assert b'Edit Account' in response.data
    assert b'That email and username already has an account.' in response.data

# GET, status code -1 (incorrect password)
def test_edit_account_GET_status_neg1(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.get('/editaccount', query_string={'status_code':-1})
    assert response.status_code == 200
    assert b'Edit Account' in response.data
    assert b'Incorrect password.' in response.data

# GET, valid email
def test_edit_account_GET_valid_email(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.get('/editaccount', query_string={'emailValid':True})
    assert response.status_code == 200
    assert b'Edit Account' in response.data
    assert b'That email is invalid' not in response.data

# GET, invalid email
def test_edit_account_GET_invalid_email(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.get('/editaccount', query_string={'emailValid':False})
    assert response.status_code == 200
    assert b'Edit Account' in response.data
    assert b'That email is invalid.' in response.data

# POST, status 0 (success)
def test_edit_account_POST_success(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    hash, salt = generateHashAndSalt('testPass')
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, %s, %s); ''', (hash, salt))
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.post('/editaccount', data=ImmutableMultiDict([('oldEmail', 'user@gmail.com'),('email', 'user@gmail.com'),('username','username'),('password', 'testPass')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/home' in response.data

# POST, status not 0 (fail)
def test_edit_account_POST_failure(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'username'
    response = test_client.post('/editaccount', data=ImmutableMultiDict([('oldEmail', 'user@gmail.com'),('email', 'user@gmail.com'),('username','username'),('password', 'wrongPass')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/editaccount' in response.data

# ---Delete Account---
# Successful Delete
def test_delete_account(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.post('/deleteaccount', data=ImmutableMultiDict([('email', 'user@gmail.com')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/' in response.data