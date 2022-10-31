from flask import jsonify, Blueprint, request, Response, json
from api.services import generate_menu, get_recipe


MENU_BLUEPRINT = Blueprint("menu", __name__)


@MENU_BLUEPRINT.route("/menu")
def get_menu() -> Response:
    data = dict(request.args)
    response = generate_menu(**data)

    return Response(json.dumps(response), 200 if isinstance(response, dict) else 400) if response \
        else Response("wrong_menu_inputs", 400)


@MENU_BLUEPRINT.route("/menu/<recipe_id>")
def get_recipe_detail(recipe_id: str) -> Response:
    response = get_recipe(int(recipe_id))

    return jsonify(response) if response else Response("Recipe not found", 404)
