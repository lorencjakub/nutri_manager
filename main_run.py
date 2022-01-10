from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from distinct_types import *

app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", default=str(os.urandom(24)))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db.session().expire_on_commit = False
os.environ["FLASK_APP"] = "migrate_db.py"


@app.route("/")
def public_table() -> WebTemplate:
    return render_template("homepage.html")


if __name__ == '__main__':
    if "database.sqlite3" not in os.listdir(os.getcwd()):
        from data_miners.data_miner import crawl_all
        from models import *
        db.create_all()
        os.system("flask db init")
        crawl_all()

    app.run(debug=True)
