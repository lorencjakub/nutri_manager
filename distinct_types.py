from typing import *
from scrapy import Spider
from api.models import NutriRecipes


WebTemplate = NewType("WebTemplate", object)

JsonDict = NewType("JsonDict", str)

JsonList = NewType("JsonDict", str)

CrawlerSpider = NewType('CrawlerSpider', Type[Spider])

GeneratedMenu = NewType("GeneratedMenu", List[NutriRecipes])

GeneratedMenuData = NewType("GeneratedMenuData",
                            Dict[str, Union[Dict[str, Dict[str, Union[str, int]]], Dict[str, float]]])

RecipeData = NewType("RecipeData", Dict[str, Union[str, float, int]])

CORSSettings = NewType("CORSSettings", Dict[str, Union[List[str], str]])

SecuritySettings = NewType("SecuritySettings", Dict[str, Union[List[str], str]])
