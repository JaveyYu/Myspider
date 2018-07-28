# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from crawler.items import TestItem
from crawler.settings import *
from scrapy import Request
import re
from scrapy.selector import Selector
import copy
from crawler.spiders import util
import time
from datetime import datetime,timedelta

class TestspiderSpider(Spider):
    name = 'CrawlerTest'
    

    def start_requests(self):
         start_urls = 'http://guba.eastmoney.com/list,of000001.html'
         yield Request(url = start_urls, callback = self.parse_post_list)

    def parse(self, response):
        pass


    def parse_post_list(self, response):
        item = TestItem()
        item['content'] = {}
        posts = response.xpath('//div[@class="articleh"]').extract()
        for post in posts:
            readnum = Selector(text = post).xpath('//span[@class="l1"]/text()').extract()
            if readnum:
                readnum = readnum[0]
                item['content']['readnum'] = readnum
            
            replynum = Selector(text = post).xpath('//span[@class="l2"]/text()').extract()
            if replynum:
                replynum = replynum[0]
                item['content']['replynum'] = replynum
                print(item['content']['replynum'])


