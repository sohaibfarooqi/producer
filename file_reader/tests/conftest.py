import pytest, csv, os
from file_reader.create_app import create_app

@pytest.fixture(scope='session')
def app():
    """
    This fixture creates Flask app with testing
    configurations.
    """
    yield create_app(testing=True)

@pytest.fixture(scope='session')
def empty_file():
    """
    This fixture creates Flask app with testing
    configurations.
    """
    file_name = 'test.csv'
    file = open(file_name, 'w')
    file.close()
    yield open(file_name, 'rb')
    os.remove(file_name)



