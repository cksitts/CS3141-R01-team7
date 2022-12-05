from flask.testing import FlaskClient
from typing import Tuple
from werkzeug.datastructures import ImmutableMultiDict
import logging
log = logging.getLogger(__name__)

# methods to test:
# login_required (done)
# admin_only (done)

# ---Requires Login---
# logged in
def test_login_flag_true(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.post('/deleteaccount', data=ImmutableMultiDict([('email','user@gmail.com')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/home' in response.data

# not logged in
def test_login_flag_false(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.post('/deleteaccount', data=ImmutableMultiDict([('email','user@gmail.com')]))
    assert response.status_code == 302
    assert b'Redirecting...', b'/login' in response.data

# ---Admin Only---
# admin
def test_admin_flag_true(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['username'] = 'name'
        session['admin'] = 1
    response = test_client.get('/addmachines')
    assert response.status_code == 200
    assert b'Add Machines' in response.data

# not admin
def test_admin_flag_false(test_client:FlaskClient):
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.get('/addmachines')
    assert response.status_code == 403
    assert b'Forbidden, 403' in response.data