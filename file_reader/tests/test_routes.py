from flask import url_for

def test_without_file(app):
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'))
    rv.status_code == 400

def test_invalid_file_format(app, invalid_file):
  data = {}
  data['file'] = (invalid_file, invalid_file.name)
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'), data=data)
    rv.status_code == 406

def test_successful_request(app, valid_file):
  data = {}
  data['file'] = (valid_file, valid_file.name)
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'), data=data)
    assert rv.status_code == 200
