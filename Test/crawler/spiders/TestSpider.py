# -*- coding: utf-8 -*-
from scrapy import FormRequest
from scrapy.spiders import Spider
from crawler.items import TestItem
from crawler.settings import *
from scrapy import Request
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
#import re
#import time
#import copy
import pymongo
import json
#import pandas as pd
class TestspiderSpider(Spider):
    name = 'CrawlerTest'

    def start_requests(self):
        start_url = 'https://xueqiu.com'
        yield Request(start_url, callback = self.parse)

    def parse(self, response):
        next = response.xpath('//li[@class="_b8vexar"]//a/@href').extract()
         
        print()








