from main_run import app
from flask import render_template, jsonify, session, request, Response
from distinct_types import *
import time
import random
import string


@app.route("/", methods=["GET"])
def public_table() -> WebTemplate:
    return render_template("homepage.html")


@app.route("/get-menu/<date>", methods=["GET"])
def get_menu(date: str) -> Tuple[Response, int]:
    # if "session_id" not in session:
    #     salt = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    #     session["session_id"] = str(time.time()).replace(".", "") + salt
    #
    # from api import Menu
    # menu = Menu()
    #
    # return jsonify(menu.create_menu()), 200
    return Response(date), 200
