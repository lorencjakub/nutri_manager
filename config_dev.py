import os


SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SECRET_KEY = os.environ.get("SECRET_FLASK_KEY", default="xdex1fxb0>x98?Sxe5xd1xd8xbd0Yxfex03x8fx12hCxbcxbbU")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", default="sqlite:///database.sqlite3")
