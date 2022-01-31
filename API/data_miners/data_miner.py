from data_miners.data_miners.spiders.nutri_spider import NutriTableSpider
from data_miners.data_miners.spiders.recipe_spider import NutriRecipeSpider
from scrapy.crawler import CrawlerProcess
import datetime


def crawl_nutri_tables() -> None:
    nutri_tables = input("This function will start crawling of food database of kaloricketabulky.cz (over 200 000 "
                         "of records).\nThis task can take up to few hours.\nAre you sure to start it? (y/n)").lower()

    if nutri_tables == "y":
        start_time = datetime.datetime.now().timestamp()
        NutriTableSpider().reset_counter()

        process = CrawlerProcess()
        process.crawl(NutriTableSpider)
        process.start()

        duration = datetime.datetime.now().timestamp() - start_time
        minutes = int(duration // 60)
        seconds = round(duration % 60, 3)
        print(f"Done. {NutriTableSpider().count} records have been added in {minutes} minutes and {seconds} seconds.")


def crawl_nutri_recipes() -> None:
    nutri_recipes = input("This function will start crawling of food database of zdravefitrecepty.cz."
                          "\nThis task will take around one minute.\nAre you sure to start it? (y/n)").lower()

    if nutri_recipes == "y":
        NutriRecipeSpider.reset_counter()
        start_time = datetime.datetime.now().timestamp()

        process = CrawlerProcess()
        process.crawl(NutriRecipeSpider)
        process.start()

        duration = datetime.datetime.now().timestamp() - start_time
        print(f"Done. {NutriRecipeSpider().count} records have been added in {round(duration, 3)} seconds.")


def crawl_all() -> None:
    start_time = datetime.datetime.now().timestamp()
    process = CrawlerProcess()

    nutri_tables = input("This function will start crawling of food database of kaloricketabulky.cz (over 200 000 "
                         "of records).\nThis task can take up to few hours.\nAre you sure to start it? (y/n)").lower()

    if nutri_tables == "y":
        process.crawl(NutriTableSpider)

    nutri_recipes = input("This function will start crawling of food database of zdravefitrecepty.cz."
                          "\nThis task should take up to few minutes.\nAre you sure to start it? (y/n)").lower()

    if nutri_recipes == "y":
        process.crawl(NutriRecipeSpider)

    if nutri_tables == "y" or nutri_recipes == "y":
        process.start()
        duration = datetime.datetime.now().timestamp() - start_time
        minutes = int(duration // 60)
        seconds = round(duration % 60, 3)
        print(f"Done. Crawling tooks {minutes} minutes and {seconds} seconds.")


def clear_not_cz_foods():
    from models import FoodNutrients, db
    import re
    from googletrans import Translator

    translator = Translator()
    names_with_exception = [
        "banán",
        "Mozzarella light Galbani",
        "Mozzarella Galbani",
        "rukola",
        "ananas",
        "cuketa",
        "kakao",
        "dalamánek",
        "majonéza",
        "veka",
        "slanina",
        "kefír",
        "mák",
        "quinoa",
        "jitrnice",
        "lilek",
        "ocet",
        "kokos",
        "nachos",
        "mascarpone",
        "jelito",
        "skyr",
        "RC cola",
        "papája",
        "marakuja",
        "ricota",
        "mochyně",
        "angrešt",
        "okoun",
        "oves",
        "cejn",
        "pšenice"
    ]

    for name in [food.name for food in FoodNutrients.query.all()]:
        if re.search("[^\w ]", name):
            FoodNutrients.query.filter_by(name=name).delete()
            db.session.commit()
            continue

        print(f"Translating of {name}...")
        try:
            translated = translator.translate(name, dest="en")

        except:
            print("Some problem appeared, translating again...")
            translated = translator.translate(name, dest="en")

        if translated.src not in "en, sk, cs, pl" and name not in names_with_exception:
            print(f"Food <<{name}>> removed because src is <<{translated.src}>>.")
            FoodNutrients.query.filter_by(name=name).delete()

        else:
            print(f"Eng_name for food <<{name}>> added: {translated.text}.")
            food = FoodNutrients.query.filter_by(name=name).first()
            food.eng_name = re.sub("\s+", " ", re.sub("([^a-zA-Z ])", "", translated.text))

        db.session.commit()

    foods = FoodNutrients.query.order_by(FoodNutrients.id.asc()).all()

    for i in range(len(foods)):
        foods[i].id = i + 1
        db.session.commit()
