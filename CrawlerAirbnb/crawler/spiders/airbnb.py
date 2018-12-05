# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from crawler.items import AirbnbItem
from crawler.settings import *
from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
import re
import time
import copy
import pymongo
import json

class AirbnbSpider(Spider):
    name = 'airbnb'

    def start_requests(self):
        start_urls = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%9D%AD%E5%B7%9E&allow_override%5B%5D=&s_tag=1gmYNi3O'
        yield SplashRequest(start_urls, self.parse)

    def parse(self, response):
        a = response.xpath('//div[@class="_v72lrv"]')
        print(response.body)
