from data_miners.data_miners.spiders.recipe_spider import NutriRecipeSpider, EnNutriRecipeSpider
from distinct_types import CrawlerSpider

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

import datetime
import sys


class DataMiners:
    main_nutri_recipe_spider: CrawlerSpider = NutriRecipeSpider
    en_nutri_recipe_spider: CrawlerSpider = EnNutriRecipeSpider
    runner = CrawlerRunner()
    process = CrawlerProcess()

    def __init__(self) -> None:
        self.start_time: float = datetime.datetime.now().timestamp()
        self.set_runner()

    def set_runner(self) -> None:
        configure_logging()
        settings = get_project_settings()
        self.runner = CrawlerRunner(settings)

    def start_timer(self) -> None:
        self.start_time = datetime.datetime.now().timestamp()

    def intial_db_crawling(self) -> None:
        print("Recipe DB is empty. The crawling of food database of zdravefitrecepty.cz..."
              "\nThis task will take around one minute.")
        self.use_more_spiders()

    def use_more_spiders(self) -> None:
        self.start_timer()
        self.crawl()
        reactor.run()

        duration = datetime.datetime.now().timestamp() - self.start_time
        print(f"Done. {self.main_nutri_recipe_spider().count} records added in {round(duration, 3)} seconds.")

    def use_en_spider(self) -> None:
        if '-U' in sys.argv or '--update' in sys.argv:
            update = input("Some of recipes does not contain english variant of ingredients."
                           "\nThis task will take around one minute.\nDo you want try to update?(y/n)")
        else:
            update = 'n'

        if update.lower() == 'y':
            print('Updating...')
            self.start_timer()
            self.process.crawl(EnNutriRecipeSpider)
            self.process.start()

        duration = datetime.datetime.now().timestamp() - self.start_time

        if duration > 100:
            print(f"Done. {self.en_nutri_recipe_spider().count} records updated in {round(duration, 3)} seconds.")

        else:
            print('DB check is completed, app is starting...')

    @classmethod
    @defer.inlineCallbacks
    def crawl(cls):
        yield cls.runner.crawl(cls.main_nutri_recipe_spider)
        yield cls.runner.crawl(cls.en_nutri_recipe_spider)

        reactor.stop()


def crawl_nutri_recipes(rows_count: int, rows_with_en_ingredients_count: int) -> None:
    crawler = DataMiners()

    if rows_with_en_ingredients_count == 0:
        print("No data in DB. Crawling starts...")
        crawler.use_more_spiders()

    if rows_count != rows_with_en_ingredients_count:
        crawler.use_en_spider()

    if '-U' in sys.argv or '--update' in sys.argv:
        print("Updating data...")
        crawler.use_more_spiders()
