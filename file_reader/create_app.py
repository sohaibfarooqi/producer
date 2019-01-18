from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, UploadNotAllowed
from .config import DevelopmentConfig, TestingConfig
from .tasks import Producer

def create_app(testing=False):
  """
  Function to create Flask App. It registers flask_uploads
  (an extenstion to manage file uploads). It also registers
  a view function to upload csv file.

  Params:
  ------
    - testing(bool): Specify whether Flask App
      should load testing configurations.

  Returns:
  --------
    `flask.Flask` instance

  Example Invocation:
  ------------------
    The following code snippet can be used to
    invoke the file upload.
    ```
    import requests
    files = {'file': open('test.csv', 'rb')}
    requests.post('http://localhost:5000/upload', files=files)
    ```
  """
  app = Flask(__name__)

  config_module = DevelopmentConfig
  if testing is True:
      config_module = TestingConfig
  app.config.from_object(config_module)

  upload_set = UploadSet('datafiles', extensions=('csv',), default_dest=lambda x: app.config['DATA_FILE_PATH'])
  configure_uploads(app, (upload_set,))
  producer = Producer()

  @app.route('/upload', methods=('POST',))
  def upload():
    """
    Returns:
    --------
      - 200: Request Successful.
      - 406: Input file format not allowed.
      - 400: Empty file received.
    """
    try:

      data_file = request.files['file']
      file = upload_set.save(data_file)
      producer.s("{}/{}".format(app.config['DATA_FILE_PATH'], file)).apply_async()

    except UploadNotAllowed:
      return jsonify({"message": "Requested file format not allowed"}), 406

    except (StopIteration, RuntimeError):
      return jsonify({"message": "Received empty file"}), 400

    return jsonify({"message": "ok"}), 200

  return app
