from flask_migrate import Migrate
from main_run import app
from models import *

migrate = Migrate(app, db, compare_type=True, render_as_batch=True)
