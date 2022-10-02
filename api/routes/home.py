from flask import Blueprint


HOME_BLUEPRINT = Blueprint("home", __name__)


@HOME_BLUEPRINT.route("/")
def get_menu():
    return "hello world"
