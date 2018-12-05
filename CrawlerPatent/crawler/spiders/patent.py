# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import Spider
from scrapy import FormRequest
from crawler.items import PatentItem
from crawler.settings import *
from scrapy import Request
from scrapy.http import Response
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
from urllib.request import urlretrieve
import re
import time
import copy
import pymongo
import json

class PatentSpider(Spider):
    name = 'patent'

    def start_requests(self):
        login_url = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml'
        yield Request(url = login_url, callback = self.parse_captcha)

    def parse_captcha(self,response):
        captcha_url = response.urljoin(response.xpath('//div[@class="captcha-img"]//img/@src').extract()[0])
        captcha_response = Request(url = captcha_url, callback = self.parse_login)
        body = captcha_response.meta['body']
        with open('captcha\\captcha.png','wb') as f:
            f.write(captcha_response.body)

        yield Request(url = captcha_url, callback = self.parse_login)
        
    def parse_login(self,response):
        body = response.meta['body']
        body['response_body'] = response.body
        yield body
        

        #login_data = {
        #    'j_username':'javey',
        #    'j_password':'yujiawei960630'
        #    }

        #yield FormRequest.from_response(response, formdata = login_data, callback = self.parse)
        

    def parse(self, response):
        pass
