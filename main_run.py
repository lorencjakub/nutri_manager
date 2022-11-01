from flask import Flask
from flask_cors import CORS
from utils.SecurityManager import SecurityHeaderManager

from utils.security_settings import set_cors, set_security_headers
from extensions import db, migrate
from api.routes import *

import os
import sys
import re


def create_app(env: str = "dev") -> Flask:
    """Create application factory
    :param env: The current environment.
    """
    config_object = "config_dev" if env == "dev" else "config_prod"

    app = Flask("nutri_manager")

    if __name__ == "__main__":
        CORS(app, **set_cors())
        SecurityHeaderManager(app, **set_security_headers())

    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    # register_errorhandlers(app)
    # register_shellcontext(app)
    # register_commands(app)
    # configure_logger(app)
    return app


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    db.init_app(app)
    # db.session().expire_on_commit = False

    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    return None


def register_blueprints(app: Flask) -> None:
    """Register Flask api."""
    app.register_blueprint(MENU_BLUEPRINT)

    return None


def main_loop() -> None:
    from api.models.models import CsNutriRecipes, EnNutriRecipes, DeNutriRecipes
    from sqlalchemy import func
    from data_miners.data_miner import crawl_nutri_recipes

    if "--help" in sys.argv:
        print("This module will run nutri manager app server.\n"
              "Usable flags:\n"
              "--help         see options\n"
              "-U --update    allow data crawling to update DB\n")

        return

    app = create_app()

    with app.app_context():
        if "database.sqlite3" not in os.listdir(os.getcwd()):
            print('No DB found. Creating...')
            db.create_all()
            os.system("flask db init")
            print('A new database has been created.')

        if "migrations" not in os.listdir(os.getcwd()):
            if "-m" in sys.argv:
                index_of_message_flag = sys.argv.index("-m")
                message = sys.argv[index_of_message_flag + 1]
                os.system(f'flask db init && flask db migrate -m "{message}"')

            else:
                os.system("flask db init && flask db migrate")

        elif "-m" in sys.argv:
            index_of_message_flag = sys.argv.index("-m")
            message = sys.argv[index_of_message_flag + 1]
            os.system(f'flask db migrate -m "{message}"')

        if "migrations" in os.listdir(os.getcwd()) and [re.findall("\.py$", v) for v in os.listdir(f'{os.getcwd()}/migrations/versions')]:
            os.system("flask db upgrade")

        db_row_counts = {
            "cs": {
                "spider": CsNutriRecipes,
                "row_count": db.session.query(func.count(CsNutriRecipes.id)).scalar()
            },
            "en": {
                "spider": EnNutriRecipes,
                "row_count": db.session.query(func.count(EnNutriRecipes.id)).scalar()
            },
            "de": {
                "spider": DeNutriRecipes,
                "row_count": db.session.query(func.count(DeNutriRecipes.id)).scalar()
            }
        }

        crawl_nutri_recipes(db_row_counts)

    app.run(debug=True)


if __name__ == "__main__":
    main_loop()
