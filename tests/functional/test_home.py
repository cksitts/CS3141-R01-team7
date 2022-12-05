from flask.testing import FlaskClient
from typing import Tuple
import logging
log = logging.getLogger(__name__)

# methods to test:
# home (done)

def test_home(test_client_with_db:Tuple[FlaskClient, any]):
    test_client, cursor = test_client_with_db
    cursor.execute(''' INSERT INTO MachineUser VALUES ('test@gmail.com', 'testUser', '500E Wads (Test Hall)', 'hash', 'salt'); ''')
    cursor.execute(''' INSERT INTO Machine VALUES ('500E_WH_1', 'Test Hall', 'Washer'), ('501E_WH_1', 'Test Hall 2', 'Dryer'); ''')
    cursor.execute(''' INSERT INTO UsingMachine VALUES ('501E_WH_1', 'test@gmail.com', 'testUser', '1800000000'); ''')
    with test_client.session_transaction() as session:
        session['username'] = 'testUser'
    response = test_client.get('/home')
    
    assert response.status_code == 200
    for item in [
        b'<title>Home</title>',
        b'document.currentScript.previousElementSibling.innerHTML = "Dryer " + getNumber("501E_WH_1") + " - " + getRoom("501E_WH_1") + " (Test Hall 2)"',
        b'<h2>Available Machines</h2>',
        b'<option value=\'500E Wads (Test Hall)\' selected>500E Wads (Test Hall)</option>',
        b'<h2>Unavailable Machines</h2>'
    ]:
        assert item in response.data
