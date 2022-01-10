import json

import scrapy
import os


class NutriRecipeUrlSpider(scrapy.Spider):
    name = "nutri_recipe_url_spider"
    data = []

    def start_requests(self):
        if len(self.get_data()) == 0:
            yield scrapy.Request(url="https://www.zdravefitrecepty.cz/recepty/snidane", callback=self.parse)

    @classmethod
    def add_data(cls, recipe_data: dict) -> list:
        cls.data.append(recipe_data)
        return cls.data

    @classmethod
    def get_data(cls) -> list:
        return cls.data

    @classmethod
    def save_urls(cls) -> None:
        with open(os.getcwd() + "/data_miners/urls.txt", "w", encoding='utf8') as urls:
            data = json.dumps(cls.data, ensure_ascii=False)
            urls.write(data)

    def parse(self, response) -> None:
        data_string = [s for s in response.css("script") if "APOLLO_STATE" in s.get()][0].get()[44:-12]
        data = eval(eval('"""' + data_string + '"""').replace(
            "false", "False").replace("true", "True").replace("null", "None"))

        for key in list(data.keys()):
            if "tags" not in list(data[key].keys()) or "title" not in list(
                    data[key].keys()) or "slug" not in list(data[key].keys()):
                continue

            recipe_hrefs = {
                "name": data[key]["title"],
                "tags": str(data[key]["tags"]["json"]),
                "url": "https://www.zdravefitrecepty.cz/recept/" + data[key]["slug"]
            }

            self.add_data(recipe_hrefs)

        self.save_urls()
