# -*- coding: utf-8 -*-
from crawler.spiders import util
from scrapy.spiders import Spider
from datetime import datetime
from scrapy import Request
from scrapy.selector import Selector
from crawler.items import XQItem
from crawler.settings import *
from scrapy.utils.request import request_fingerprint
import re
import json
import time


class CubeInfoSpider(Spider):
    name = 'cube_info'
    logger = util.set_logger(name, LOG_FILE_CUBE_INFO)
    handle_httpstatus_list = [404]
    website_possible_httpstatus_list = [404]
    
    def start_requests(self):

        start_url = 'https://xueqiu.com/P/SP1048445'

        yield Request(start_url, callback = self.parse)


    def parse(self, response):
        content = response.xpath('//script[contain(.,)]').extract()

        print(response.body)



