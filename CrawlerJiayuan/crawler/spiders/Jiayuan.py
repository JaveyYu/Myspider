# -*- coding: utf-8 -*-
from scrapy import FormRequest
from scrapy.spiders import Spider
from crawler.items import JiayuanItem
from crawler.settings import *
from scrapy import Request
import pandas as pd
import re

class JiayuanSpider(Spider):
    name = 'Jiayuan'

    def start_requests(self):
        urls = pd.read_csv('C:\\Users\\T440-Yu\\Source\\Repos\\Myspider\\CrawlerJiayuan\\crawler\\spiders\\url.csv', 
                                header = None, sep = ',', names = ['urls'])
        urls = list(urls['urls'])
        login_url = 'http://login.jiayuan.com/'
        
        yield Request(url = login_url, meta = {'urls' : urls} ,callback = self.parse_login)

    def parse_login(self, response):
        urls = response.meta['urls']
        login_data = {
            'name':'18612209787',
            'password':'shiyan5201314',
            }
        yield FormRequest.from_response(response, formdata = login_data, meta = {'urls':urls}, callback = self.parse)
    
    def parse(self, response):
        urls = response.meta['urls']
        for url in urls:
            yield Request(url = url, callback = self.parse_item)

    def parse_item(self, response):
        item = JiayuanItem()
        #title = response.xpath('//div[@class="fl f_gray_999"]/text()').extract()
        content = response.xpath('//ul//div[@class="fl pr"]/em/text()').extract()
        if content:
            item['ID'] = re.search('.com\/(\d*)', response.url).group(1)
            item['Education'] = content[0]
            item['Height'] = content[1]
            item['Car'] = content[2]
            item['Salary'] = content[3]
            item['House'] = content[4]
            item['Weight'] = content[5]
            item['Constellation'] = content[6]
            item['Ethnic'] = content[7]
            item['zodiac'] = content[8]
            item['Blood_type'] = content[9]
            yield item


        
