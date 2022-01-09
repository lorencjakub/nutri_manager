from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from distinct_types import *
from data_miner import crawl_nutri_tables

app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", default=str(os.urandom(24)))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db.session().expire_on_commit = False
os.environ["FLASK_APP"] = "migrate_db.py"

# REGISTRACE BLUEPRINTŮ
import nutri_tables
app.register_blueprint(nutri_tables.nutri_tables)

from models import *


@app.route("/")
def public_table() -> WebTemplate:
    return render_template("homepage.html")


if __name__ == '__main__':
    if "database.sqlite3" not in os.listdir(os.getcwd()):
        db.create_all()
        os.system("flask db init")
        crawl_nutri_tables()

    app.run(debug=True)
