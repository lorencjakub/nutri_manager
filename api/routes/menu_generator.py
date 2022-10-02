from flask import jsonify, Blueprint, json, request, Response
from api.services import generate_menu, get_recipe
from distinct_types import Type, Union, Tuple, GeneratedMenuData


MENU_BLUEPRINT = Blueprint("menu", __name__)


@MENU_BLUEPRINT.route("/menu")
def get_menu():
    data = dict(request.args)
    response = generate_menu(**data)

    return jsonify(response) if response else Response("Wrong inputs", 404)


@MENU_BLUEPRINT.route("/menu/<recipe_id>")
def get_recipe_detail(recipe_id: str) -> Response:
    response = get_recipe(int(recipe_id))

    return jsonify(response) if response else Response("Recipe not found", 404)
