from data_miners.data_miners.spiders import *
from distinct_types import CrawlerSpider, Union, Dict

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

import datetime
import sys


class DataMiners:
    cs_nutri_recipe_spider: CrawlerSpider = CsNutriRecipeSpider
    en_nutri_recipe_spider: CrawlerSpider = EnNutriRecipeSpider
    de_nutri_recipe_spider: CrawlerSpider = DeNutriRecipeSpider
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
        print("Recipe DB is empty. The crawling of food database has been started."
              "\nThis task will take around one minute.")
        self.use_more_spiders()

    def use_more_spiders(self, data) -> None:
        self.start_timer()
        self.crawl(data)
        reactor.run()

        duration = datetime.datetime.now().timestamp() - self.start_time
        print(f"Done. {self.cs_nutri_recipe_spider().count + self.en_nutri_recipe_spider().count + self.de_nutri_recipe_spider().count} records added in {round(duration, 3)} seconds.")

    @classmethod
    @defer.inlineCallbacks
    def crawl(cls, data):
        if "cs" in data:
            yield cls.runner.crawl(cls.cs_nutri_recipe_spider)

        if "en" in data:
            yield cls.runner.crawl(cls.en_nutri_recipe_spider)

        if "de" in data:
            yield cls.runner.crawl(cls.de_nutri_recipe_spider)

        reactor.stop()


def crawl_nutri_recipes(locale_data: Dict[str, Dict[str, Union[CrawlerSpider, int]]]) -> None:
    crawler = DataMiners()
    locales_to_update = [key for [key, value] in list(locale_data.items()) if value["row_count"] == 0]

    if locales_to_update:
        print("No data in DB. Crawling starts...")
        crawler.use_more_spiders(locales_to_update)

    if '-U' in sys.argv or '--update' in sys.argv:
        print("Updating data...")
        crawler.use_more_spiders(list(locale_data.keys()))
