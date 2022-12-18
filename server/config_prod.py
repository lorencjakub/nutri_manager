import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env_prod'))

SECRET_KEY = os.environ.get("SECRET_KEY", default="super-secret-key")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = True if os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", default=True) == "True" else False
SQLALCHEMY_ECHO = True if os.environ.get("SQLALCHEMY_ECHO", default=True) == "True" else False
FE_ORIGIN = os.environ.get("FE_ORIGIN")
