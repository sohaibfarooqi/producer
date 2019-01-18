from flask import url_for

def test_without_file(app):
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'))
    rv.status_code == 400

def test_empty_file(app, empty_file):
  data = {}
  data['file'] = (empty_file, empty_file.name)
  with app.app_context() as ctx:
    rv = app.test_client().post(url_for('upload'), data=data)
    assert rv.status_code == 400
