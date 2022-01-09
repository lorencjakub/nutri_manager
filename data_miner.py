from data_miners.data_miners.spiders import nutri_spider
from scrapy.crawler import CrawlerProcess
import datetime


def crawl_nutri_tables() ->  None:
    start = input("This function will start crawling of food database of kaloricketabulky.cz "
                  "(over 200 000  of records).\nThis task will take few minutes.\nAre you sure to start it? (y/n)")

    if start == "y":
        start_time = datetime.datetime.now().timestamp()
        nutri_spider.NutriTableSpider().reset_counter()

        process = CrawlerProcess()
        process.crawl(nutri_spider.NutriTableSpider)
        process.start()

        duration = datetime.datetime.now().timestamp() - start_time
        minutes = int(duration // 60)
        seconds = round(duration % 60, 3)
        print(f"Done. {nutri_spider.NutriTableSpider().count} records have been added in {minutes} minutes "
              f"and {seconds} seconds.")

