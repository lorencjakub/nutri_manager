from flask import Flask
from flask_cors import CORS
from utils.SecurityManager import SecurityHeaderManager

from utils.security_settings import set_cors, set_security_headers
from extensions import *
from api.routes import *

import os
import sys
import re
import json
from distinct_types import Union


BE_ENV = os.environ.get("BE_ENV")
print(BE_ENV)

def create_app(with_secutiry: bool = True) -> Flask:
    """Create application factory
    """
    config_object = f'config_{BE_ENV if BE_ENV is not None else "dev"}'
    app = Flask("nutri_manager")
    app.config.from_object(config_object)

    cors_settings = set_cors()
    security_headers = set_security_headers()

    if with_secutiry:
        fe_origin = os.environ.get("FE_ORIGIN")

        if fe_origin:
            try:
                fe_origin = json.loads(fe_origin)
                
            except:
                pass

            cors_settings["origins"] = [*fe_origin] if isinstance(fe_origin, list) else [fe_origin]
        CORS(app, **cors_settings)
        SecurityHeaderManager(app, **security_headers)

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


def main_loop() -> Union[None, Flask]:
    from api.models.models import CsNutriRecipes, EnNutriRecipes, DeNutriRecipes
    from sqlalchemy import func
    from data_miners.data_miner import crawl_nutri_recipes

    host = None
    port = None

    if "--help" in sys.argv:
        print("This module will run nutri manager app server.\n"
              "Usable flags:\n"
              "--help         see options\n"
              "-U --update    allow data crawling to update DB\n")

        return

    if "--host" in sys.argv:
        host_index = sys.argv.index("--host")
        host = sys.argv[host_index + 1]

    if "--port" in sys.argv or "-p" in sys.argv:
        port_index = sys.argv.index("--port") or sys.argv.index("-p")
        port = int(sys.argv[port_index + 1])

    app = create_app()

    with app.app_context():
        empty_db = (len(inspect(db.engine).get_table_names()) == 0) if BE_ENV == "prod" else \
            "database.sqlite3" not in os.listdir(os.getcwd())

        if empty_db:
            print('No DB found. Creating...')

            if "migrations" in os.listdir(os.getcwd()) and "versions" not in os.listdir(f'{os.getcwd()}/migrations'):
                os.rmdir(f'{os.getcwd()}/migrations')

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

        if "versions" in os.listdir(f'{os.getcwd()}/migrations') and [
            re.findall("py$", v) for v in os.listdir(f'{os.getcwd()}/migrations/versions')
        ]:
            os.system("flask db upgrade")

        if BE_ENV != "test":
            db_row_counts = {
                "cs": {
                    "spider": CsNutriRecipes,
                    "row_count": db.session.query(func.count(CsNutriRecipes.id)).scalar() if
                    inspect(db.engine).has_table("cs_nutri_recipes") else 0
                },
                "en": {
                    "spider": EnNutriRecipes,
                    "row_count": db.session.query(func.count(EnNutriRecipes.id)).scalar() if
                    inspect(db.engine).has_table("en_nutri_recipes") else 0
                },
                "de": {
                    "spider": DeNutriRecipes,
                    "row_count": db.session.query(func.count(DeNutriRecipes.id)).scalar() if
                    inspect(db.engine).has_table("de_nutri_recipes") else 0
                }
            }

            crawl_nutri_recipes(db_row_counts)

    if BE_ENV == "prod":
        return app
    
    else:
        app.run(debug=(BE_ENV != "prod"), host=host, port=port)


if __name__ == "__main__":
    main_loop()
