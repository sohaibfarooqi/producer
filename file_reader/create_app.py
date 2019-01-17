from flask import Flask
from .api import ALL_AVAILABLE_VERSIONS
from .config import DevelopmentConfig, TestingConfig

def create_app(testing=False):
  """
  Function to create Flask App. Registers
  all available api version as Blueprints

  Params:
  ------
    - testing(bool): Specify whether Flask App
      should load testing configurations.
  """
  app = Flask(__name__)

  config_module = DevelopmentConfig
  if testing is True:
      config_module = TestingConfig
  app.config.from_object(config_module)

  for api_version in ALL_AVAILABLE_VERSIONS:
    app.register_blueprint(api_version)

  return app
