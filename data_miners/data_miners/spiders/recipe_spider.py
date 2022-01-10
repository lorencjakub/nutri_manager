import scrapy
from scrapy.exceptions import CloseSpider
import re
from typing import Tuple
import os


class NutriRecipeSpider(scrapy.Spider):
    name = "nutri_recipe_spider"
    count = 0
    data = []

    def start_requests(self):
        self.set_data()

        if len(self.get_data()) != 0:
            urls = [u["url"] for u in self.get_data()]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

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
    def set_data(cls) -> list:
        with open(os.getcwd() + "/data_miners/urls.txt", "r", encoding="utf8") as urls:
            cls.data = eval(urls.read())

        return cls.data

    def parse(self, response):
        recipe_name = response.css(".headingFlex h1::text").get()
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

        recipe_index, current_recipe = self.get_recipe(recipe_name)

        current_recipe.update({
            "ingredients": ingredients,
            "procedure": procedure,
        })

        current_recipe.update(nutrients)

        self.write_data(current_recipe)

    def write_data(self, data: dict) -> None:
        del data["url"]

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
