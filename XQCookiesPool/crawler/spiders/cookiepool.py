# -*- coding: utf-8 -*-
from scrapy import FormRequest
from scrapy import Request
from scrapy.spiders import Spider
from crawler.items import CookiePoolItem
from crawler.settings import *
from crawler.spiders import util
from selenium import webdriver
import json


class CookiepoolSpider(Spider):
    name = 'cookiepool'

    def start_requests(self):
        login_url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=token&client_id=100229413&redirect_uri=https://xueqiu.com/service/qqconnect&scope=get_user_info,add_share,add_t'
    
        yield Request(url = login_url, callback = self.parse_login)

    def parse_login(self, response):
        browser = webdriver.Chrome()


        login_data = {
            'u' : '3399516284',
            'p' : 'wx348528'
            }
        yield FormRequest.from_response(response, formdata = login_data, callback = self.parse)

    def parse(self,response):
        print(response)
        print
