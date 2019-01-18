import os

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
