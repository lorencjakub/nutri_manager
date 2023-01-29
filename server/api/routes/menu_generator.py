from flask import jsonify, Blueprint, request, Response
from api.services import generate_menu, generate_random_menu, generate_random_meal, get_recipe
import json
from distinct_types import List


MENU_BLUEPRINT = Blueprint("menu", __name__)


@MENU_BLUEPRINT.route("/menu", methods=["POST"])
def get_menu() -> Response:
    data = request.json
    response = generate_menu(**data)

    return jsonify(response) if response \
        else Response(json.dumps({"message": "no_menu"}) if response is None else
                      json.dumps({"message": "wrong_menu_inputs"}), 400)


@MENU_BLUEPRINT.route("/random_menu", methods=["GET"])
def get_random_menu() -> Response:
    response = generate_random_menu()

    return jsonify(response) if response else Response(json.dumps({"message": "no_menu"}))


@MENU_BLUEPRINT.route("//random_reload_meal", methods=["POST"])
def get_random_meal() -> Response:
    meal_to_reload: str = request.json["meal_to_reload"]
    meal_ids: List[str] = request.json["meal_ids"]
    response = generate_random_meal(meal_to_reload, meal_ids)

    return jsonify(response) if response else Response(json.dumps({"message": "no_menu"}))


@MENU_BLUEPRINT.route("/menu/<recipe_id>", methods=["GET"])
def get_recipe_detail(recipe_id: str) -> Response:
    response = get_recipe(int(recipe_id))

    return jsonify(response) if response else Response(json.dumps({"message": "recipe_not_found"}), 404)
