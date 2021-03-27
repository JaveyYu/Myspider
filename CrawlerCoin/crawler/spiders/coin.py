# -*- coding: utf-8 -*-
from crawler.spiders import util
from scrapy.spiders import Spider
from datetime import datetime
from scrapy import Request
from scrapy.selector import Selector
from crawler.items import CoinItem
from crawler.settings import *
from scrapy.utils.request import request_fingerprint
import re
import json
import time

class CoinSpider(Spider):
    start_at=datetime.now()
    name='coin'
    #logger = util.set_logger(name, LOG_FILE_CUBE_INFO)
    #handle_httpstatus_list = [404]
    #website_possible_httpstatus_list = [404]

    def start_requests(self):
        start_url="https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1&convert=USD&time_start=1609804800&time_end=1614902400"
        start_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id="

        start_time = time.mktime(time.strptime('2013-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
        start_time = int(start_time)
        end_time = time.mktime(time.strptime('2021-03-05 00:00:00', '%Y-%m-%d %H:%M:%S'))
        end_time = int(end_time)

        start_id = 1
        end_id = 8700
        for i in range(start_id, end_id):
            id = i
            url = start_url + str(i) + '&convert=USD&time_start=' + str(start_time) + '&time_end=' + str(end_time)
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        body = json.loads(response.body)
        
        id = body['data']['id']
        name = body['data']['name']
        for i in body['data']['quotes']:
            item = CoinItem()
            i['id'] = id
            i['name'] = name
            item['content'] = i
            yield item








 