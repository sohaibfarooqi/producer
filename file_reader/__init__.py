from .create_app import create_app
from .tasks import celery_app

if __name__ == "__main__":
  app = create_app()
  app.run()
