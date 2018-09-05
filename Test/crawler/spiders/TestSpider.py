# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from crawler.items import TestItem
from crawler.settings import *
from scrapy import Request
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
import re
import time
import copy
import pymongo
import json

class TestspiderSpider(Spider):
    name = 'CrawlerTest'
    

    def start_requests(self):
         start_urls = 'http://www.jiayuan.com/167625797'
         item = TestItem()
         yield Request(url = start_urls, callback = self.parse)

    def parse(self, response):
        title = response.xpath('//div[@class="fl f_gray_999"]/text()').extract()
        content = response.xpath('//ul//div[@class="fl pr"]/em/text()').extract()
        print(content)
        #pass
