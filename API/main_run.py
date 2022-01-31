import os
import sys
sys.path.append(os.getcwd() + r"\API")
from distinct_types import *

try:
    from flask import Flask, render_template

except ModuleNotFoundError:
    in_venv = input("I can't find neccessary packages, but I can install them.\n"
                    "Am I in virtual environment now, where I could do it? (y/n)")

    if in_venv != "y":
        print("OK, let me create a new one with all wonderfulness!")
        os.system("py -m venv venv")
        os.system(r".\venv\Scripts\activate")
        os.system("pip install -r requirements.txt -y")

from flask_sqlalchemy import SQLAlchemy
import logging
logging.getLogger('scrapy').propagate = False

app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", default=str(os.urandom(24)))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
db.session().expire_on_commit = False
os.environ["FLASK_APP"] = "migrate_db.py"


@app.route("/")
def public_table() -> WebTemplate:
    return render_template("homepage.html")


if __name__ == '__main__':
    from models import *
    from sqlalchemy import func
    from data_miners.data_miner import crawl_all, crawl_nutri_tables, crawl_nutri_recipes, clear_not_cz_foods

    if "database.sqlite3" not in os.listdir(os.getcwd()):
        cleanup = input(
            "Do you want also clean up DB after crawling? This will delete all records with names marked by googletrans"
            "different from cz, sk or eng and add eng_names to the food without "
            "this value.\n(y/n)").lower()

        db.create_all()
        os.system("flask db init")
        crawl_all()

        if cleanup == "y":
            clear_not_cz_foods()

    if db.session.query(func.count(NutriRecipes.id)).scalar() == 0:
        cleanup = input(
            "Do you want also clean up DB after crawling? This will delete all records with names marked by googletrans"
            "different from cz, sk or eng and add eng_names to the food without "
            "this value.\n(y/n)").lower()

        print("NO RECIPES, CRAWLING STARTING...")
        crawl_nutri_recipes()

        if cleanup == "y":
            clear_not_cz_foods()

    if db.session.query(func.count(FoodNutrients.id)).scalar() == 0:
        cleanup = input(
            "Do you want also clean up DB after crawling? This will delete all records with names marked by googletrans"
            "different from cz, sk or eng and add eng_names to the food without "
            "this value.\n(y/n)").lower()

        print("NO NUTRIENTS, CRAWLING STARTING...")
        crawl_nutri_tables()

        if cleanup == "y":
            clear_not_cz_foods()

    if db.session.query(func.count(NutriRecipes.id)).scalar() != 0 and \
            db.session.query(func.count(FoodNutrients.id)).scalar() != 0:
        cleanup = input(
            "Do you want also clean up DB after crawling? This will delete all records with names marked by googletrans"
            "different from cz, sk or eng and add eng_names to the food without "
            "this value.\n(y/n)").lower()

        if cleanup == "y":
            clear_not_cz_foods()

    app.run(debug=True)
