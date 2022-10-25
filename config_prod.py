import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

SECRET_KEY = os.environ.get("SECRET_KEY", default="super-secret-key")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", default="sqlite:///database.sqlite3")
SQLALCHEMY_TRACK_MODIFICATIONS = True if os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", default=True) == "True" else False
SQLALCHEMY_ECHO = True if os.environ.get("SQLALCHEMY_ECHO", default=True) == "True" else False
