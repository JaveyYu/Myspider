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

class CoinSpider(Spider):
    start_at=datetime.now()
    name='hudongyi'

    def start_requests(self):
        start_url="http://irm.cninfo.com.cn/ircs/company/question"
        db = util.set_mongo_server()
        stocks = []
        for s in db.orgIDs.find():
            stocks.append(s)

        all_page_n = len(stocks)
        for i in range(all_page_n):
            now_page_n = i
            stock = stocks[i]
            data = {'stockcode' : stock['stkcd'], 'pageSize':'10', 'pageNum':'1', 'orgId' : stock['orgID']}
            yield FormRequest(url = start_url, formdata = data, callback = self.parse, meta = {'page':1, 'stkcd':stock['stkcd'], 'orgId':stock['orgID']})

    def parse(self, response):
        page = response.meta['page']
        stkcd = response.meta['stkcd']
        orgId = response.meta['orgId']
        try:
            body = json.loads(response.body)
            rows = body['rows']
            maxpage = body['totalPage']

            item = InteractItem()
            for row in rows:
                item['content'] = row
                yield item

            if page < maxpage:
                page = page + 1
                data = {'stockcode' : stkcd, 'pageSize':'10', 'pageNum':str(page), 'orgId' : orgId}
                yield FormRequest(url = response.url, formdata = data, meta = {'page':page, 'stkcd':stkcd, 'orgId':orgId}, callback = self.parse)
        except Exception as ex:
            self.logger.error('Parse Exception: %s %s' % (str(stkcd), str(page)))
