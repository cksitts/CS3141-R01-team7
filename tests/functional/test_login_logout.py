from flask.testing import FlaskClient
from werkzeug.datastructures import ImmutableMultiDict
from typing import Tuple
import logging
log = logging.getLogger(__name__)

# methods to test:
# index (done)
# logout (done)

# ---Index/Login---
# Test all URLs (/, /index, /login)
def test_index_GET_all_urls(test_client:FlaskClient):
    for url in ['/', '/index', '/login']:
        response = test_client.get(url, query_string={'validLogin':True})
        assert response.status_code == 200
        assert b'<title>Login</title>' in response.data

# Get, valid login
def test_index_GET_valid_login(test_client:FlaskClient):
    response = test_client.get('/login', query_string={'validLogin':True})
    assert response.status_code == 200
    assert b'<title>Login</title>' in response.data
    assert b'Invalid email or password' not in response.data

# Get, invalid login
def test_index_GET_invalid_login(test_client:FlaskClient):
    response = test_client.get('/login', query_string={'validLogin':False})
    assert response.status_code == 200
    assert b'<title>Login</title>' in response.data
    assert b'Invalid email or password' in response.data

# Post, user doesn't exist
def test_index_POST_invalid(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.post('/login', data=ImmutableMultiDict([('username', 'testUser'),('password', 'testPass')]))
    assert b'Redirecting...', b'/login?validLogin=False' in response.data

# ---Logout---
# Logged in
def test_logout(test_client:FlaskClient):
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.get('/logout')
    assert b'Redirecting...', b'/login' in response.data
    with test_client.session_transaction() as session:
        assert session.get('username') == None