from flask import jsonify, Blueprint, request, Response
from api.services import generate_menu, generate_random_menu, generate_meal, get_recipe
import json
from distinct_types import List


MENU_BLUEPRINT = Blueprint("menu", __name__)


def parse_tagged_data(data):
    tags = {
        "breakfast_tags": data["breakfast_tags"],
        "lunch_tags": data["lunch_tags"],
        "snack_tags": data["snack_tags"],
        "dinner_tags": data["dinner_tags"]
    }

    data["tags"] = tags
    del data["breakfast_tags"]
    del data["lunch_tags"]
    del data["snack_tags"]
    del data["dinner_tags"]

    return data


@MENU_BLUEPRINT.route("/menu", methods=["POST"])
def get_menu() -> Response:
    data = parse_tagged_data(request.json)
    response = generate_menu(**data)

    return jsonify(response) if response \
        else Response(json.dumps({"message": "no_menu"}) if response is None
                      else json.dumps({"message": "wrong_menu_inputs"}), 400)


@MENU_BLUEPRINT.route("/random_menu", methods=["GET"])
def get_random_menu() -> Response:
    response = generate_random_menu()

    return jsonify(response) if response \
        else Response(json.dumps({"message": "no_menu"}) if response is None
                      else json.dumps({"message": "wrong_menu_inputs"}), 400)


@MENU_BLUEPRINT.route("/reload_meal", methods=["POST"])
def get_meal() -> Response:
    data = parse_tagged_data(request.json["menu_data"])
    meal_to_reload: str = request.json["meal_to_reload"]
    meal_ids: List[str] = request.json["meal_ids"]
    response = generate_meal(meal_to_reload, meal_ids, kwargs=data)

    return jsonify(response) if response \
        else Response(json.dumps({"message": "no_menu"}) if response is None
                      else json.dumps({"message": "wrong_menu_inputs"}), 400)


@MENU_BLUEPRINT.route("/menu/<recipe_id>", methods=["GET"])
def get_recipe_detail(recipe_id: str) -> Response:
    response = get_recipe(int(recipe_id))

    return jsonify(response) if response else Response(json.dumps({"message": "recipe_not_found"}), 400)
