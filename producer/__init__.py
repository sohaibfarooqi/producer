from .create_app import create_app
from .producer import celery_app, Producer

if __name__ == "__main__":
    app = create_app()
    app.run()
