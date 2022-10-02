import scrapy
from scrapy.exceptions import CloseSpider
import re
import time
from typing import Tuple, List
from database import db
from api.models.models import NutriRecipes
import json


class NutriRecipeSpider(scrapy.Spider):
    name = "nutri_recipe_spider"
    count: int = 0
    data = []
    locale: str = None
    recipe_base_url: str = 'https://www.zdravefitrecepty.cz/recept/'
    start_urls: List[str] = ['https://www.zdravefitrecepty.cz']
    custom_settings = {
        'DOWNLOAD_DELAY': 0
    }

    def __init__(self) -> None:
        super().__init__()
        self.urls = None

        if not self.locale:
            self.set_locale('cs')

    def parse(self, response, **kwargs):
        data_string = [s for s in response.css("script") if "STORE_REHYDRATION" in s.get()][0].get()[45:-12]
        data = eval(eval('"""' + data_string + '"""').replace(
            "false", "False").replace("true", "True").replace("null", "None"))
        food_data = []

        for key in list(data.keys()):
            elements = data[key]

            if not isinstance(elements, list) or len(elements) == 0 or (
                isinstance(elements[0], dict) and "slug" not in list(elements[0].keys())
            ):
                continue

            for el in elements:
                if 'id' not in list(el.keys()) or 'title' not in list(el.keys()) or \
                        'tags' not in list(el.keys()) or 'slug' not in list(el.keys()) or \
                        'portionCount' not in list(el.keys()):
                    continue

                recipe_hrefs = {
                    "name": el["title"],
                    "tags": json.dumps(el['tags']) if (isinstance(el['tags'], list) or isinstance(el['tags'], list))
                    else str(el['tags']),
                    "url": f'{self.recipe_base_url}{el["slug"]}',
                    'recipe_id': int(el['id']),
                    'portions': int(el['portionCount'])
                }
                food_data.append(recipe_hrefs)

        self.set_data(food_data)

        try:
            for u in food_data:
                time.sleep(0.2)
                yield scrapy.Request(url=u["url"], callback=self.extract_data)

        except Exception:
            raise CloseSpider("No URLs detected.")

    @classmethod
    def get_recipe(cls, name: str) -> Tuple[int, dict]:
        recipe = [r for r in cls.data if r["name"] == name][0]

        return cls.data.index(recipe), recipe

    @classmethod
    def get_data(cls) -> list:
        return cls.data

    @classmethod
    def set_data(cls, foods: list) -> None:
        cls.data = foods

    @classmethod
    def set_locale(cls, locale: str) -> None:
        base_urls = {
            'cs': ['https://www.zdravefitrecepty.cz/recept/'],
            'de': ['https://www.fitnesszauberin.de/rezept/'],
            'en': ['https://www.fitfoodwizard.com/recipe/'],
        }

        cls.start_urls = ['/'.join(base_urls[locale][0].split('/')[0:-2])]
        cls.recipe_base_url = base_urls[locale][0]
        cls.locale = locale

    def extract_data(self, response):
        recipe_name = response.css(".headingFlex h1::text").get()
        recipe_index, current_recipe = self.get_recipe(recipe_name)

        if self.locale == 'cs':
            if len(NutriRecipes.query.filter_by(recipe_id=current_recipe["recipe_id"]).all()) == 0:
                ingredients = "|".join([re.sub("<.*?>", "", li.get())
                                        for li in response.css(".recipeDetailIngredients ul li")])
                procedure = "|".join([re.sub("<.*?>", "", li.get()) for li in response.css("ol li")])
                nutrients = {
                    "energy": float(response.css(
                        ".nutritionalValues tbody tr:nth-child(1) td:nth-child(2)::text").get().split(" ")[0]),
                    "proteins": float(response.css(
                        ".nutritionalValues tbody tr:nth-child(4) td:nth-child(2)::text").get().split(" ")[0]),
                    "carbs": float(response.css(
                        ".nutritionalValues tbody tr:nth-child(2) td:nth-child(2)::text").get().split(" ")[0]),
                    "fats": float(response.css(
                        ".nutritionalValues tbody tr:nth-child(5) td:nth-child(2)::text").get().split(" ")[0]),
                    "fiber": float(response.css(
                        ".nutritionalValues tbody tr:nth-child(3) td:nth-child(2)::text").get().split(" ")[0]),
                    "url": response.url
                }

                current_recipe.update({
                    "ingredients": ingredients,
                    "procedure": procedure,
                    **nutrients
                })

                self.write_data(current_recipe)

            else:
                print(f'DB already contains recipe <<{current_recipe["name"]}>>.')

        else:
            if len(NutriRecipes.query.filter_by(recipe_id=current_recipe["recipe_id"]).all()) != 0:
                ingredients = "|".join([re.sub("<.*?>", "", li.get())
                                        for li in response.css(".recipeDetailIngredients ul li")])
                current_recipe.update({"ingredients": ingredients})
                self.update_data(current_recipe)

            else:
                print(f'Recipe <<{current_recipe["name"]}>> not found in DB.')
                print(f'locale: {self.locale} recipe_id: {current_recipe["recipe_id"]} name: {current_recipe["name"]}')

    def write_data(self, data: dict) -> None:
        n = NutriRecipes().create(**data)

        try:
            if len(NutriRecipes.query.filter_by(name=data["name"]).all()) == 0:
                db.session.add(n)
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(e)
            raise CloseSpider("Problem with adding data to the DB.")

        self.count_one()

    def update_data(self, data: dict) -> None:
        try:
            recipe = NutriRecipes.query.filter_by(recipe_id=data["recipe_id"]).first()
            recipe.en_ingredients = data['ingredients']
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(e)
            raise CloseSpider("Problem with adding data to the DB.")

        self.count_one()

    @classmethod
    def reset_counter(cls):
        cls.count = 0
        cls.data = []

    @classmethod
    def count_one(cls):
        cls.count += 1


class EnNutriRecipeSpider(NutriRecipeSpider):
    name = "en_nutri_recipe_spider"

    def __init__(self):
        super().__init__()
        self.urls = None
        self.set_locale('en')
