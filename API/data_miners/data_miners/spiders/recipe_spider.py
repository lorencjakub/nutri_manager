import scrapy
from scrapy.exceptions import CloseSpider
import re
import time
from typing import Tuple
from googletrans import Translator
from models import NutriRecipes, db


class NutriRecipeSpider(scrapy.Spider):
    name = "nutri_recipe_spider"
    count = 0
    data = []
    start_urls = [
        "https://www.zdravefitrecepty.cz/recepty"
    ]

    def __init__(self):
        super().__init__()
        self.urls = None

    def parse(self, response):
        data_string = [s for s in response.css("script") if "APOLLO_STATE" in s.get()][0].get()[44:-12]
        data = eval(eval('"""' + data_string + '"""').replace(
            "false", "False").replace("true", "True").replace("null", "None"))
        food_data = []

        for key in list(data.keys()):
            if "tags" not in list(data[key].keys()) or "title" not in list(
                    data[key].keys()) or "slug" not in list(data[key].keys()):
                continue

            recipe_hrefs = {
                "name": data[key]["title"],
                "tags": str(data[key]["tags"]["json"]),
                "url": "https://www.zdravefitrecepty.cz/recept/" + data[key]["slug"]
            }
            food_data.append(recipe_hrefs)

        NutriRecipeSpider.set_data(food_data)

        print(len(food_data))
        for u in food_data:
            print(u["url"])
            time.sleep(0.2)
            yield scrapy.Request(url=u["url"], callback=self.extract_data)

        else:
            raise CloseSpider("No URLs for zdravefitrecepty.cz detected.")

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

    def extract_data(self, response):
        recipe_name = response.css(".headingFlex h1::text").get()
        recipe_index, current_recipe = self.get_recipe(recipe_name)

        if len(NutriRecipes.query.filter_by(name=current_recipe["name"]).all()) == 0:
            ingredients = "|".join([re.sub("<.*?>", "", li.get()) for li in response.css(".recipeDetailIngredients ul li")])
            procedure = "|".join([re.sub("<.*?>", "", li.get()) for li in response.css("ol li")])
            response.css(".nutritionalValues tbody tr")
            response.css(".nutritionalValues tbody tr:nth-child(1) td:nth-child(2)::text")
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
            }

            current_recipe.update({
                "ingredients": ingredients,
                "procedure": procedure,
            })

            current_recipe.update(nutrients)

            self.write_data(current_recipe)

        else:
            print(f'DB already contains recipe <<{current_recipe["name"]}>>.')

    def write_data(self, data: dict) -> None:
        del data["url"]
        translator = Translator()

        try:
            translated = translator.translate(data["ingredients"], dest='en')
            text = translated.text

        except AttributeError:
            text = "?"

        data["eng_ingredients"] = text.lower()

        from models import NutriRecipes, db

        n = NutriRecipes().save_recipes(**data)

        try:
            if len(NutriRecipes.query.filter_by(name=data["name"]).all()) == 0:
                db.session.add(n)
                db.session.commit()

        except Exception as e:
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
