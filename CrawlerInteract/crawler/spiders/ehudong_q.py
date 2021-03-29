# -*- coding: utf-8 -*-
from crawler.spiders import util
from scrapy.spiders import Spider
from datetime import datetime
from scrapy import Request
from scrapy import FormRequest
from scrapy.selector import Selector
from crawler.items import InteractItem
from crawler.settings import *
from scrapy.utils.request import request_fingerprint
import re
import json
import time
import pandas as pd

class CoinSpider(Spider):
    start_at=datetime.now()
    name='ehudong_q'

    def start_requests(self):
        start_url="https://msns.sseinfo.com/api/index/getLatestQuestions.do?pageIndex=%d&pageSize=50&stockCode=%d&deviceType=2"
        db = util.set_mongo_server()
        
        stkcds = pd.read_csv('Stkcd_sse.csv')
        stkcds = list(stkcds['stkcd'])
        #stkcds = [600000]
        for stkcd in stkcds:
            url = start_url % (1, stkcd)
            yield Request(url = url, callback = self.parse, meta = {'page':1, 'start_url':start_url, 'stkcd':stkcd})

    def parse(self, response):
        page = response.meta['page']
        start_url = response.meta['start_url']
        stkcd = response.meta['stkcd']

        body = json.loads(response.body)
        if body['code'] == '2000201':
            results = body['info']['result']
            item = InteractItem()
            for result in results:
                    if isinstance(result,dict):
                        if result['qid'] != '':
                            item['content'] = result
                            yield item
                    else:
                        try:
                            result = json.loads(re.sub('\\x00','',result).strip())
                            item['content'] = result
                            yield item
                        except Exception as ex:
                            self.logger.warn('Parse Exception: %s %s' % (stkcd, str(page)))

            if len(results) == 50:
                page = page + 1
                url = start_url % (page, stkcd)
                yield Request(url = url, callback = self.parse, meta = {'page':page, 'start_url':start_url, 'stkcd':stkcd})

