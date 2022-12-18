from flask import jsonify, Blueprint, request, Response
from api.services import generate_menu, get_recipe
import json


MENU_BLUEPRINT = Blueprint("menu", __name__)


@MENU_BLUEPRINT.route("/menu")
def get_menu() -> Response:
    data = dict(request.args)
    response = generate_menu(**data)

    return jsonify(response) if response \
        else Response(json.dumps({"message": "no_menu"}) if response is None else
                      json.dumps({"message": "wrong_menu_inputs"}), 400)


@MENU_BLUEPRINT.route("/menu/<recipe_id>")
def get_recipe_detail(recipe_id: str) -> Response:
    response = get_recipe(int(recipe_id))

    return jsonify(response) if response else Response(json.dumps({"message": "recipe_not_found"}), 404)
