import scrapy
from scrapy.exceptions import CloseSpider
import re


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
                    "name": row.css(f"td:nth-child(1) div div a::text").get(),
                    "energy": row.css(f"td:nth-child(2)::text").get(),
                    "proteins": row.css(f"td:nth-child(3)::text").get(),
                    "carbs": row.css(f"td:nth-child(4)::text").get(),
                    "fats": row.css(f"td:nth-child(5)::text").get(),
                    "fiber": row.css(f"td:nth-child(6)::text").get(),
                }

                self.write_data(food_data)

        else:
            raise CloseSpider("Empty table, crawling is done.")

    def write_data(self, data: dict) -> None:
        for key, value in list(data.items())[1:]:
            string_without_whitespaces = value.replace(" ", "").replace(",", ".")
            data[key] = float(string_without_whitespaces) if string_without_whitespaces != "" else 0

        data["name"] = self.edit_name(data["name"])

        from models import FoodNutrients, db
        n = FoodNutrients().save_nutrients(**data)

        try:
            db.session.add(n)
            db.session.commit()

        except Exception as e:
            print(e)
            raise CloseSpider("Problem with adding data to the DB.")

        self.count_one()

    @staticmethod
    def edit_name(name: str) -> str:
        wrong_characters = "ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġ" \
                           "ĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ"
        correct_characters = "AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgG" \
                             "gGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs"

        for index, char in enumerate(name):
            try:
                char_list = list(name)
                char_list[index] = correct_characters[wrong_characters.index(char)]
                name = "".join(char_list)

            except ValueError:
                continue

        return re.sub(r'\W+', '', name.lower().replace(" ", "_"))

    @classmethod
    def reset_counter(cls):
        cls.count = 0

    @classmethod
    def count_one(cls):
        cls.count += 1