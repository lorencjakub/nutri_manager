import scrapy
from scrapy.exceptions import CloseSpider
from googletrans import Translator
from models import FoodNutrients, db
import time


class NutriTableSpider(scrapy.Spider):
    name = "nutri_spider"
    count = 0

    def start_requests(self):
        urls = [
            "https://www.kaloricketabulky.cz/tabulka-potravin"
        ]

        for i in range(2, 250000):
            urls.append(f"https://www.kaloricketabulky.cz/tabulka-potravin?page={i}")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.xpath("//tbody/tr")[:-1].css(f"td:nth-child(2)::text").get():
            for row in response.xpath("//tbody/tr")[:-1]:
                food_data = {
                    "name": row.css("td:nth-child(1) div div a::text").get(),
                    "energy": row.css("td:nth-child(2)::text").get(),
                    "proteins": row.css("td:nth-child(3)::text").get(),
                    "carbs": row.css("td:nth-child(4)::text").get(),
                    "fats": row.css("td:nth-child(5)::text").get(),
                    "fiber": row.css("td:nth-child(6)::text").get(),
                }

                if len(FoodNutrients.query.filter_by(name=food_data["name"]).all()) == 0:
                    self.write_data(food_data)

                else:
                    print(f'DB already contains food <<{food_data["name"]}>>.')

        else:
            raise CloseSpider("Empty table, crawling is done.")

    def write_data(self, data: dict) -> None:
        time.sleep(0.2)
        for key, value in list(data.items())[1:]:
            string_without_whitespaces = value.replace(" ", "").replace(",", ".")
            data[key] = float(string_without_whitespaces) if string_without_whitespaces != "" else 0

        translator = Translator()

        try:
            translated = translator.translate(data["name"], dest='en')
            language = translated.src
            text = translated.text

        except AttributeError:
            language = "cs"
            text = "?"

        if language == "cs" and len(data["name"].split(" ")) <= 3:
            data["eng_name"] = text.lower()

            n = FoodNutrients().save_nutrients(**data)

            try:
                if len(FoodNutrients.query.filter_by(name=data["name"]).all()) == 0:
                    db.session.add(n)
                    db.session.commit()

            except Exception as e:
                print(e)
                raise CloseSpider("Problem with adding data to the DB.")

            self.count_one()

    @classmethod
    def reset_counter(cls):
        cls.count = 0

    @classmethod
    def count_one(cls):
        cls.count += 1
