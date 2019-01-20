from flask import url_for


def test_without_file(app):
  """
  Test file upload API without file. Endpoint should throw
  400 Bad Request.
  """
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'))
    rv.status_code == 400

def test_invalid_file_format(app, invalid_file):
  """
  Test file upload API with different file extention.
  Endpoint should throw 406 Unacceptable.
  """
  data = {}
  data['file'] = (invalid_file, invalid_file.name)
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'), data=data)
    rv.status_code == 406

def test_successful_request(app, valid_file):
  """
  Test file upload API with valid file. Endpoint should return
  200 Ok.
  """
  data = {}
  data['file'] = (valid_file, valid_file.name)
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'), data=data)
    assert rv.status_code == 200
