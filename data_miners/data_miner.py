from data_miners.data_miners.spiders.nutri_spider import NutriTableSpider
from data_miners.data_miners.spiders.recipe_spider import NutriRecipeSpider
from data_miners.data_miners.spiders.recipe_url_spider import NutriRecipeUrlSpider
from scrapy.crawler import CrawlerProcess
import datetime
import os


def crawl_nutri_tables() -> None:
    start_time = datetime.datetime.now().timestamp()
    NutriTableSpider().reset_counter()

    process = CrawlerProcess()
    process.crawl(NutriTableSpider)
    process.start()

    duration = datetime.datetime.now().timestamp() - start_time
    minutes = int(duration // 60)
    seconds = round(duration % 60, 3)
    print(f"Done. {NutriTableSpider().count} records have been added in {minutes} minutes and {seconds} seconds.")


def crawl_nutri_recipes_url() -> None:
    print("Crawling of urls for zdravefitrecepty.cz is starting.")
    process = CrawlerProcess()
    process.crawl(NutriRecipeUrlSpider)
    process.start()


def crawl_nutri_recipes() -> None:
    print("Crawling of recipes from zdravefitrecepty.cz is starting.")
    NutriRecipeSpider.reset_counter()
    start_time = datetime.datetime.now().timestamp()

    process = CrawlerProcess()
    process.crawl(NutriRecipeSpider)
    process.start()

    duration = datetime.datetime.now().timestamp() - start_time
    print(f"Done. {NutriRecipeSpider().count} records have been added in {round(duration, 3)} seconds.")

    if os.path.isfile(os.getcwd() + "/data_miners/urls.txt"):
        os.remove(os.getcwd() + "/data_miners/urls.txt")


def crawl_all() -> None:
    start_time = datetime.datetime.now().timestamp()

    process = CrawlerProcess()

    nutri_tables = input("This function will start crawling of food database of kaloricketabulky.cz (over 200 000 "
                         "of records).\nThis task can take up to few hours.\nAre you sure to start it? (y/n)")

    if nutri_tables == "y":
        process.crawl(NutriTableSpider)

    nutri_recipes = input("This function will start crawling of food database of zdravefitrecepty.cz."
                          "\nThis task will take around one minute.\nAre you sure to start it? (y/n)")

    if nutri_recipes == "y":
        process.crawl(NutriRecipeUrlSpider)
        process.crawl(NutriRecipeSpider)

    if nutri_tables == "y" or nutri_recipes == "y":
        process.start()
        duration = datetime.datetime.now().timestamp() - start_time
        minutes = int(duration // 60)
        seconds = round(duration % 60, 3)
        print(f"Done. Crawling tooks {minutes} minutes and {seconds} seconds.")

    if os.path.isfile(os.getcwd() + "/data_miners/urls.txt"):
        os.remove(os.getcwd() + "/data_miners/urls.txt")
