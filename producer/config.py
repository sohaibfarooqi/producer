import os


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


class CeleryConfig:
    """
    Configuration for Celery
    """
    broker_url = os.environ.get('CELERY_BROKER_URL', 'pyamqp://')

    enable_utc = True
    timezone = "UTC"

    task_always_eager = os.environ.get('CELERY_ALWAYS_EAGER', False)
    task_eager_propagates = os.environ.get('CELERY_EAGER_PROPAGATES', False)
    task_create_missing_queues = True
