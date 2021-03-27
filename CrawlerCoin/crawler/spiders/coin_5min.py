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
    name='coin_5min'
    #logger = util.set_logger(name, LOG_FILE_CUBE_INFO)
    #handle_httpstatus_list = [404]
    #website_possible_httpstatus_list = [404]

    def start_requests(self):
        start_url = "https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?convert=USD,BTC&format=chart_crypto_details&id=%d&interval=5m&time_end=%d&time_start=%d"

        #start_time = time.mktime(time.strptime('2013-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
        #start_time = int(start_time)
        #end_time = time.mktime(time.strptime('2021-03-05 00:00:00', '%Y-%m-%d %H:%M:%S'))
        #end_time = int(end_time)

        
        start_id = 1
        end_id = 8700
        for i in range(start_id, end_id):
            id = i
            start_time = 1367580600 - 2999400
            end_time = 1367580600
            for j in range(1,83):
                start_time = start_time +2999400
                end_time = end_time +2999400
                url = start_url %(i, end_time, start_time)
                yield Request(url=url, callback=self.parse, meta ={'id' : id})
    
    def parse(self, response):
        body = json.loads(response.body)        
        id = response.meta['id']

        for i in body['data']:
            item = CoinItem()
            content = {}
            content['id'] = id
            content['timestamp'] = i
            content['content'] =  body['data'][i]
            item['content'] = content
            yield item








 
