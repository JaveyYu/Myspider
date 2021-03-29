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
    name='hudongyi4'

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
            if i%50==0:
                self.logger.info('%s (%s / %s) %s%%' % (stock['stkcd'], str(now_page_n), str(all_page_n), str(round(float(now_page_n) / all_page_n * 100, 1))))

            data = {'stockcode' : stock['stkcd'], 'pageSize':'500', 'pageNum':'1', 'orgId' : stock['orgID']}
            yield FormRequest(url = start_url, formdata = data, callback = self.parse, meta = {'page':1, 'stkcd':stock['stkcd'], 'orgId':stock['orgID']})

    def parse(self, response):
        page = response.meta['page']
        stkcd = response.meta['stkcd']
        orgId = response.meta['orgId']
        
        try:
            body = json.loads(response.body)    
            maxpage = body['totalPage']
            rows = body['rows']
            item = InteractItem()
            for row in rows:
                item['content'] = row
                item['content']['page'] = page
                item['content']['maxpage'] = maxpage
                yield item
            for page in range(2, (maxpage + 1)):
                data = {'stockcode' : stkcd, 'pageSize':'500', 'pageNum':str(page), 'orgId' : orgId}
                yield FormRequest(url = response.url, formdata = data, meta = {'page':page, 'stkcd':stkcd, 'orgId':orgId}, callback = self.parse_page)
        except Exception as ex:
            self.logger.warn('Parse Exception: %s %s' % (stkcd, str(page)))
    
    def parse_page(self, response):
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
                item['content']['page'] = page
                item['content']['maxpage'] = maxpage
                yield item
        except Exception as ex:
            self.logger.warn('Parse Exception: %s %s' % (stkcd, str(page)))



