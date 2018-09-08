# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JiayuanItem(Item):
    ID = Field()
    Education = Field()
    Height = Field()
    Car = Field()
    Salary = Field()
    House = Field()
    Weight = Field()
    Constellation = Field()
    Ethnic = Field()
    zodiac = Field()
    Blood_type = Field()

