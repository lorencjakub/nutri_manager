from tests.unit.webapp import client
from unittest.mock import patch
from .mocking import mock_get_menu, mock_get_recipe
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

MOCKED_MENU_SUCCESS = mock_get_menu(True)
MOCKED_MENU_NONE = mock_get_menu()
MOCKED_RECIPE = mock_get_recipe()


def test_001_get_menu_success(client) -> None:
    with patch("api.routes.menu_generator.generate_menu", return_value=mock_get_menu(True)):
        response = client.get('/menu')

        assert response.status_code == 200
        assert client.get('/menu').json == MOCKED_MENU_SUCCESS


def test_002_get_menu_none(client) -> None:
    with patch("api.routes.menu_generator.generate_menu", return_value=mock_get_menu(None)):
        response = client.get('/menu')

        assert response.status_code == 200
        assert response.json == MOCKED_MENU_NONE


def test_003_get_menu_fail(client) -> None:
    with patch("api.routes.menu_generator.generate_menu", return_value=mock_get_menu(False)):
        response = client.get('/menu')

        assert response.status_code == 400
        assert response.data.decode() == "Wrong inputs"


def test_004_get_recipe_success(client) -> None:
    with patch("api.routes.menu_generator.get_recipe", return_value=mock_get_recipe()):
        response = client.get('/menu/1')

        assert response.status_code == 200
        assert response.json == MOCKED_RECIPE


def test_005_get_recipe_fail(client) -> None:
    with patch("api.routes.menu_generator.get_recipe", return_value=None):
        response = client.get('/menu/1')

        assert response.status_code == 404
        assert response.data.decode() == "Recipe not found"
