import csv
import os

import pytest

from producer import create_app


@pytest.fixture(scope='session')
def app():
    """
    This fixture creates Flask app with testing
    configurations.
    """
    yield create_app(testing=True)

@pytest.fixture
def invalid_file():
    """
    Fixture to generate invalid file extention.
    """
    file_name = 'invalid_test.txt'
    file = open(file_name, 'w')
    file.close()
    yield open(file_name, 'rb')
    os.remove(file_name)

@pytest.fixture
def valid_file():
    """
    Fixture to generate valid CSV file.
    """
    file_name = 'valid_test.csv'
    file = open(file_name, 'w')
    writer = csv.writer(file)
    writer.writerow(['abc', 'abc@def.com'])
    file.close()
    yield open(file_name, 'rb')
    os.remove(file_name)

@pytest.fixture
def file_with_header():
    """
    Fixture to generate valid CSV file with header.
    """
    file_name = 'file_with_header.csv'
    file = open(file_name, 'w')
    writer = csv.writer(file)
    writer.writerow(['name', 'email'])
    writer.writerow(['abc', 'abc@def.com'])
    file.close()
    yield open(file_name, 'r')
    os.remove(file_name)

@pytest.fixture
def file_with_seperator():
    """
    Fixture to generate valid CSV file with `|` seperator.
    """
    file_name = 'file_with_seperator.csv'
    file = open(file_name, 'w')
    writer = csv.writer(file, delimiter='|')
    writer.writerow(['abc', 'abc@def.com'])
    file.close()
    yield file_name
    os.remove(file_name)

@pytest.fixture
def custom_file_format():
    """
    Fixture to generate valid CSV file with header, '|' seperator
    and multiple rows.
    """
    file_name = 'custom_file_format.csv'
    file = open(file_name, 'w')
    writer = csv.writer(file, delimiter='|')
    writer.writerow(['email', 'name'])
    writer.writerow(['abc@def.com', 'abc'])
    writer.writerow(['abc@def.com', 'abc'])
    file.close()
    yield file_name
    os.remove(file_name)
