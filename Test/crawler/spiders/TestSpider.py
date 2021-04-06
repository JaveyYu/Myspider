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
        start_url = 'https://im0.xueqiu.com/im-comet/v2/notifications/4869304/ping.json?'
         #https://im0.xueqiu.com/im-comet/v2/notifications/4869304/ping.json?user_id=2270920225
        data = {'user_id' : '2270920225'}
        yield FormRequest(start_url, formdata = data, callback = self.parse)

    def parse(self, response):
        body = response.body
         
        print(body)








