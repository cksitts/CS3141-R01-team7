import pytest
from app import create_app
from config import TestingConfig

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestingConfig)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client