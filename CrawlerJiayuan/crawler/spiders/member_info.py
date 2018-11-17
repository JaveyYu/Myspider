# -*- coding: utf-8 -*-
from scrapy import FormRequest
from scrapy.spiders import Spider
from crawler.items import JiayuanItem
from crawler.settings import *
from scrapy import Request
from crawler.spiders import util
from datetime import datetime,timedelta
from scrapy.selector import Selector
import pandas as pd
import re
import time
import copy
import pymongo
import json
import os

class JiayuanSpider(Spider):
    name = 'member_info'

    def start_requests(self):
        filenames = os.listdir('E:\\Spider\\Myspider\\CrawlerJiayuan\\url38\\')
        login_url = 'http://login.jiayuan.com/'
        yield Request(url = login_url, meta = {'filenames':filenames}, callback = self.parse_login)

    def parse_login(self, response):
        filenames = response.meta['filenames']
        login_data = {
            'name':'18612209787',
            'password':'shiyan5201314',
            }
        yield FormRequest.from_response(response,meta = {'filenames':filenames}, formdata = login_data, callback = self.parse)

    def parse(self, response):
        filenames = response.meta['filenames']
        for filename in filenames:
            urls = pd.read_excel('E:\\Spider\\Myspider\\CrawlerJiayuan\\url38\\' + filename,  
                             header = None)[0]
            for url in urls:
                yield Request(url = url, meta = {'filename':filename}, callback = self.parse_item)

    def parse_item(self, response):
        item = JiayuanItem()
        filename = response.meta['filename']
        try:
            item['content'] = {}
            box = response.xpath('//ul[@class="member_info_list fn-clear"]/li//em/text()').extract()
            item['content']['id'] = re.search('(\d+)',response.url).group()
            item['content']['education'] = box[0]
            item['content']['height'] = box[1]
            item['content']['car'] = box[2]
            item['content']['salary'] = box[3]
            item['content']['house'] = box[4]
            item['content']['weight'] = box[5]
            item['content']['constellation'] = box[6]
            item['content']['ethnic'] = box[7]
            item['content']['zodiac'] = box[8]
            item['content']['blood_type'] = box[9]
            member = response.xpath('//h6[@class="member_name"]/text()').extract()[0]
            item['content']['age'] = re.split('，',member)[0]
            item['content']['marriage'] = re.split('，',member)[1]
            item['content']['filename'] = filename
            yield item
        except Exception as ex:
            print("Parse Exception: " + response.url)
        
