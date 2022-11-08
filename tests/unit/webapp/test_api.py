from tests.unit import client
from unittest.mock import patch
from tests.unit.webapp.mocking import mock_get_menu, mock_get_recipe
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
        assert response.json == MOCKED_MENU_SUCCESS


def test_002_get_menu_none(client) -> None:
    with patch("api.routes.menu_generator.generate_menu", return_value=mock_get_menu(None)):
        response = client.get('/menu')

        assert response.status_code == 400
        assert response.data.decode() == "no_menu"


def test_003_get_menu_fail(client) -> None:
    with patch("api.routes.menu_generator.generate_menu", return_value=mock_get_menu(False)):
        response = client.get('/menu')

        assert response.status_code == 400
        assert response.data.decode() == "wrong_menu_inputs"


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


def test_011_security_headers() -> None:
    with patch("api.routes.menu_generator.get_recipe", return_value=None):
        from tests.unit.CustomTestCase import CustomTestCase
        from flask_cors import CORS
        from utils.SecurityManager import SecurityHeaderManager
        from utils.security_settings import set_cors, set_security_headers

        case = CustomTestCase()
        case.setUp()
        app = case.get_app()

        CORS(app, **set_cors())
        SecurityHeaderManager(app, **set_security_headers())
        client = app.test_client()

        response = client.get('/menu/1')
        case.tearDown()

        assert response.access_control_allow_headers is None
        assert response.access_control_allow_origin == "http://localhost:1234"
        assert response.access_control_allow_methods is None
        assert response.access_control_allow_credentials is False

        assert response.headers["Permissions-Policy"] == ", ".join([
            "camera='none'",
            "display-capture='none'",
            "fullscreen='none'",
            "geolocation='none'",
            "microphone='none'"
        ])
        assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        assert response.headers.get("Cache-Control") == "max-age=0 must-revalidate no-cache no-storeprivate"
        assert response.headers.get("Access-Control-Allow-Origin") == "http://localhost:1234"
        assert response.headers["Content-Security-Policy"] == "; ".join([
            "default-src 'self'",
            "connect-src 'self'",
            "img-src 'self' data: https:",
            "style-src 'self' 'unsafe-inline' 'nonce-" + os.environ.get("NONCE") + "'",
            "script-src 'self' blob: cdnjs.cloudflare.com",
            "child-src 'self'",
            "frame-src 'self'",
            "frame-ancestors 'self'",
            "font-src 'self'"
        ])
