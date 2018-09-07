# -*- coding: utf-8 -*-
from scrapy import FormRequest
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
import pandas as pd
class TestspiderSpider(Spider):
    name = 'CrawlerTest'

    def start_requests(self):
        start_urls = pd.read_csv('C:\Users\T440-Yu\source\repos\Myspider\CrawlerJiayuan\crawler\spiders\url.csv')
        start_urls = 'http://www.jiayuan.com/167625797'
        login_url = 'http://login.jiayuan.com/'
        item = TestItem()
         
        yield Request(url = login_url, callback = self.parse_login)

    def parse_login(self, response):
        login_data = {
            'name':'18612209787',
            'password':'shiyan5201314',
            #'remem_pass':'on',
            #'ajaxsubmit':'1',
            #'ljg_login':'1',
            }
        yield FormRequest.from_response(response, formdata = login_data, callback = self.parse)

    def parse(self, response):
        url = 'http://www.jiayuan.com/167625797'
        yield Request(url = url, callback = self.parse_item)

    def parse_item(self, response):
        title = response.xpath('//div[@class="fl f_gray_999"]/text()').extract()
        content = response.xpath('//ul//div[@class="fl pr"]/em/text()').extract()
        print(content)
        #pass
