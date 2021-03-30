# -*- coding: utf-8 -*-
from crawler.spiders import util
from scrapy.spiders import Spider
from datetime import datetime
from scrapy import Request
from scrapy import FormRequest
from scrapy.selector import Selector
from crawler.items import ConferenceItem
from crawler.settings import *
from scrapy.utils.request import request_fingerprint
import re
import json
import time
import pandas as pd

class CoinSpider(Spider):
    start_at=datetime.now()
    name='scio_gov'

    def start_requests(self):
        start_url="http://www.scio.gov.cn/xwfbh/gbwxwfbh/index.html"
        db = util.set_mongo_server()
        
        yield Request(url = start_url, callback = self.parse)

    def parse(self, response):
        hrefs = response.xpath('//li//a[@class="fColor_12326A"]/@href').extract()
        for href in hrefs:
            url = 'http://www.scio.gov.cn/xwfbh/gbwxwfbh/' + href
            #url = 'http://www.scio.gov.cn/xwfbh/gbwxwfbh/' + hrefs[36]
            sector_url = re.sub('index.htm', '', url)
            yield Request(url = url, callback = self.parse_depart, meta = {'sector_url' : sector_url})


    def parse_depart(self, response):
        sector_url = response.meta['sector_url']
        sector = response.xpath('//div[@class="fl"]//span/text()').extract()[0]
        documents = response.xpath('//div[@class="fl list_t"]//a/@href').extract()
        item = ConferenceItem()
        item['content'] = {}
        item['content']['sector'] = sector

        for document in documents:
            document_url = sector_url + document
            yield Request(url = document_url, callback = self.parse_news, meta = {'item':item})

        #last_page = response.xpath('//td//a/@href').extract()[-1]
        last_page = response.xpath('//a[@id="naviLastPage"]/text()').extract()
        if last_page:
            #max_page = int(re.search('index_(\d+)',last_page).group(1)) + 1
            max_page = last_page[0]        
            for page in range(1, int(max_page)):
                page_url = sector_url + 'index_%d.htm' %(page)
                yield Request(url = page_url, callback = self.parse_page, meta = {'item':item, 'sector_url':sector_url})       

    def parse_page(self, response):
       item = response.meta['item']
       sector_url = response.meta['sector_url']
       documents = response.xpath('//div[@class="fl list_t"]//a/@href').extract()
       for document in documents:
            document_url = sector_url + document
            yield Request(url = document_url, callback = self.parse_news, meta = {'item':item})

    def parse_news(self, response):
        item =response.meta['item']

        title = response.xpath('//div[@class="tc A_title"]/text()').extract()[0]
        item['content']['title'] = title

        content = response.xpath('//div[@id="content"]//*/text()').extract()
        content = "".join(content).strip()
        item['content']['content'] = content
        
        pubtime = response.xpath('//div[@style="DISPLAY: inline"]/text()').extract()[0]
        pubtime = re.search('(\d+-\d+-\d+)', pubtime).group(1)
        item['content']['pubtime'] = pubtime
        yield item


