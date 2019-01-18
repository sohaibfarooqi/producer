class Config(object):
    """
    Base config object.
    """
    DEBUG = False
    TESTING = False
    DATA_FILE_PATH = "data_files"

class DevelopmentConfig(Config):
    """
    Development config class. Enable hot
    reloading to expedite development.
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Testing config class to facilitate unit test
    with Flask test client.
    """
    TESTING = True
    SERVER_NAME = "localhost"
