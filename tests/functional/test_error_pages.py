from flask.testing import FlaskClient
from typing import Tuple
import logging
log = logging.getLogger(__name__)

# methods to test:
# page_not_found (done)
# internal_error (done)
# forbidden_page (done)
# im_a_teapot (done)

# ---Page Not Found (404)---
# 404 error when trying to access a nonexistent page
def test_error_404(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.get('/madeupurl')
    assert response.status_code == 404
    assert b'Page not found, 404' in response.data

# ---Internal Error (500)---
# 500 error in checkout
def test_error_500_checkout(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.get('/checkout/madeUpID')
    assert response.status_code == 500
    assert b'Internal server error, 500' in response.data

# ---Forbidden Page (403)---
# 403 when trying to access a page when not logged in
def test_error_403_login(test_client:FlaskClient):
    response = test_client.get('/home')
    assert b'Redirecting...', b'/login' in response.data

# 403 when trying to access an admin page
def test_error_403_admin(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.get('/addmachines')
    assert response.status_code == 403
    assert b'Forbidden, 403' in response.data

# ---Teapot (418)---
# Teapot access page
def test_error_418_teapot(test_client:FlaskClient):
    with test_client.session_transaction() as session:
        session['username'] = 'name'
    response = test_client.get('/teapot')
    assert response.status_code == 418
    assert b'Error 418', b"This server is a teapot, not a coffee machine." in response.data
