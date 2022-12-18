import unittest
import os
from dotenv import load_dotenv
from main_run import create_app
from extensions import db
from api.models import CsNutriRecipes, EnNutriRecipes, DeNutriRecipes
from distinct_types import List, Dict


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


TEST_RECIPES_CS = [
    {
        "name": "Test breakfast cs",
        "energy": 400,
        "proteins": 40,
        "fats": 15,
        "carbs": 40,
        "fiber": 10,
        "tags": 15,
        "url": "Test breakfast URL cs",
        "recipe_id": 1,
        "portions": 1
    },
    {
        "name": "Test lunch cs",
        "energy": 700,
        "proteins": 50,
        "fats": 8,
        "carbs": 70,
        "fiber": 10,
        "tags": 16,
        "url": "Test lunch URL cs",
        "recipe_id": 2,
        "portions": 2
    },
    {
        "name": "Test dinner cs",
        "energy": 600,
        "proteins": 35,
        "fats": 12,
        "carbs": 30,
        "fiber": 15,
        "tags": 16,
        "url": "Test dinner URL cs",
        "recipe_id": 3,
        "portions": 3
    },
    {
        "name": "Test snack cs",
        "energy": 300,
        "proteins": 10,
        "fats": 5,
        "carbs": 20,
        "fiber": 5,
        "tags": 34,
        "url": "Test snack URL cs",
        "recipe_id": 4,
        "portions": 4
    }
]


def create_db_mutation(locale: str, recipes: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    This function creates variant of non-cs DB data, but pops the snack recipe,
    so the snack recipe is become as the CS only variant.
    :param locale: language string code
    :param recipes: list of recipe data for DB
    :return: Recipes data with new language code suffix in name and URL. The snack recipe is not included.
    """
    mutation = [r for r in recipes]
    del mutation[-1]
    localized_data = []

    for recipe in mutation:
        recipe_data = {}

        for key, value in recipe.items():
            recipe_data[key] = value.replace("cs", locale) if key in ["name", "url"] else value

        localized_data.append(recipe_data)

    return localized_data


TEST_RECIPES_EN = create_db_mutation("en", TEST_RECIPES_CS)
TEST_RECIPES_DE = create_db_mutation("de", TEST_RECIPES_CS)


class CustomTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.app.testing = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        self.app.config["SQLALCHEMY_ECHO"] = False

        with self.app.app_context():
            db.create_all()

            cs_data = [CsNutriRecipes(**kwargs) for kwargs in TEST_RECIPES_CS]
            en_data = [EnNutriRecipes(**kwargs) for kwargs in TEST_RECIPES_EN]
            de_data = [DeNutriRecipes(**kwargs) for kwargs in TEST_RECIPES_DE]
            cs_data.extend(en_data)
            cs_data.extend(de_data)

            s = db.session

            for r in cs_data:
                s.add(r)
            db.session.commit()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        with self.app.app_context():
            db.drop_all()

    def get_app(self):
        return self.app
