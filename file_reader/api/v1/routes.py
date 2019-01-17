from flask import Blueprint

version1 = Blueprint('version1', __name__)

@version1.route('/upload', methods=('POST',))
def upload_file():
  pass
