from flask.testing import FlaskClient
from pytest import raises
from typing import Tuple
from werkzeug.datastructures import ImmutableMultiDict
import logging
log = logging.getLogger(__name__)

# methods to test:
# signup (done)
# verify (done)


# ---signup GET---
# Valid email
def test_signup_GET_valid_email(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.get('/signup', query_string={'emailValid':True})
    assert b'<p id="invalidMessage">That email is invalid.</p>' not in response.data

# Invalid email
def test_signup_GET_invalid_email(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.get('/signup', query_string={'emailValid':False})
    assert b'<p id="invalidMessage">That email is invalid.</p>' in response.data

# Email taken
def test_signup_GET_email_taken(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.get('/signup', query_string={'status_code':1})
    assert b'<p id="invalidMessage">That email already has an account.</p>' in response.data

# Username taken
def test_signup_GET_username_taken(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.get('/signup', query_string={'status_code':2})
    assert b'<p id="invalidMessage">That username already has an account.</p>' in response.data

# Email and username taken
def test_signup_GET_both_taken(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.get('/signup', query_string={'status_code':3})
    assert b'<p id="invalidMessage">That email and username already has an account.</p>' in response.data

# Incorrect password
def test_signup_GET_incorrect_password(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    response = test_client.get('/signup', query_string={'status_code':-1})
    assert b'<p id="invalidMessage">Incorrect password.</p>' in response.data



# ---signup POST---
# Email not taken
def test_signup_POST_email_not_taken(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    # Email not taken:
    response = test_client.post('/signup', data=ImmutableMultiDict([('email', 'user@gmail.com'), ('username', 'name'), ('password', 'pass'), ('preferredRoom', 'room')]), follow_redirects=True)
    with test_client.session_transaction() as session:
        # Session verificationCode is not null
        assert session['verificationCode'] is not None
        # Session storedUser is not null
        assert session['storedUser']['email'] == 'user@gmail.com'
        # Session inputCount is 1
        assert session['inputCount'] is 1
        # Session validCode is true
        assert session['validCode'] is True

    # Redirect to verification page
    assert b'<title>Email Verification</title>' in response.data

# Email taken
def test_signup_POST_email_taken(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    # Email taken
    cursor.execute(''' INSERT INTO MachineUser VALUES ('user@gmail.com', 'username', null, 'hash', 'salt'); ''')
    response = test_client.post('/signup', data=ImmutableMultiDict([('email', 'user@gmail.com'), ('username', 'name'), ('password', 'pass'), ('preferredRoom', 'room')]), follow_redirects=True)
    assert b'<title>Sign Up</title>' in response.data
    assert b'<p id="invalidMessage">That email already has an account.</p>' in response.data



# ---verify GET---
# Valid code
def test_verify_GET_valid_code(test_client:FlaskClient):
    with test_client.session_transaction() as session:
        session['validCode'] = True
        session['inputCount'] = 0
    response = test_client.get('/verify')
    assert b'<title>Email Verification</title>' in response.data
    assert b'<p>Invalid Code.</p>' not in response.data

# Invalid code
def test_verify_GET_invalid_code(test_client:FlaskClient):
    with test_client.session_transaction() as session:
        session['validCode'] = False
        session['inputCount'] = 0
    response = test_client.get('/verify', follow_redirects=True)
    assert b'<title>Email Verification</title>' in response.data
    assert b'<p>Invalid Code.</p>' in response.data



# ---verify POST---
# Incorrect code, input count < 3
def test_verify_POST_incorrect_code_2_tries(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['verificationCode'] = 'Correct Code'
        session['inputCount'] = 2
    response = test_client.post('/verify', data=ImmutableMultiDict([('codeInput','Incorrect Code')]), follow_redirects=True)
    # Check input count increased
    with test_client.session_transaction() as session:
        assert session['inputCount'] == 3
    # Check verify redirect
    assert b'<title>Email Verification</title>' in response.data
    assert b'<p>Invalid Code.</p>' in response.data

# Incorrect code, input count = 3
def test_verify_POST_incorrect_code_3_tries(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['verificationCode'] = 'Correct Code'
        session['inputCount'] = 3
    response = test_client.post('/verify', data=ImmutableMultiDict([('codeInput','Incorrect Code')]))
    # Check signup redirect
    assert b'Redirecting...', b'/signup' in response.data

# Correct code
def test_verify_POST_correct_code(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    with test_client.session_transaction() as session:
        session['verificationCode'] = 'Correct Code'
        session['inputCount'] = 0
        session['storedUser'] = ImmutableMultiDict([('email', 'user@gmail.com'), ('username', 'name'), ('password', 'pass'), ('preferredRoom', 'room')])
    response = test_client.post('/verify', data=ImmutableMultiDict([('codeInput','Correct Code')]))
    # Check user registered
    cursor.execute(''' SELECT * FROM MachineUser WHERE email = 'user@gmail.com'; ''')
    assert len(cursor.fetchall()) != 0
    # Check session data cleared
    with raises(KeyError):
        with test_client.session_transaction() as session:
            assert session['storedUser'] is None
    # Check index redirect
    assert b'Redirecting...', b'/login' in response.data
