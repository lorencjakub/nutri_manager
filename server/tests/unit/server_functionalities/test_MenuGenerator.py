from api.services.MenuGenerator import Menu
from api.services.functions import get_recipe
from tests.unit.webapp.mocking import mock_get_menu, mock_get_recipe
from tests.unit.CustomTestCase import CustomTestCase


class TestMenuGenerator(CustomTestCase):
    def test_006_MenuGenerator_valid(self):
        generator = Menu()

        assert generator.is_valid() is True

    def test_007_MenuGenerator_non_valid(self):
        generator = Menu(energy="non_valid_value")

        assert generator.is_valid() is False

    def test_008_MenuGenerator_no_menu(self):
        with self.app.app_context():
            generator = Menu(energy=100)

            assert generator.create_menu() is None

    def test_009_MenuGenerator_create_menu(self):
        with self.app.app_context():
            generator = Menu()

            assert generator.create_menu() == mock_get_menu(True)[0]

    def test_010_MenuGenerator_get_recipe(self):
        with self.app.app_context():
            assert get_recipe(1) == mock_get_recipe()
