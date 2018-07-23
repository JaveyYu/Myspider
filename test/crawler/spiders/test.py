# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import Spider
from crawler.items import JijinbaItem
from crawler.settings import *
from scrapy import Request
import re
from scrapy.selector import Selector
import copy
from crawler.spiders import util
import time

class TestSpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
         start_urls = 'http://guba.eastmoney.com/news,of000001,774033512.html'
         yield Request(url = start_urls, callback = self.parse)
    

    def parse_post(self, response):
        try:
             if response.status == 200:
                 try:
                     filter_body = response.body.decode('utf8')
                 except:
                     try:
                         filter_body = response.body.decode("gbk")
                     except:
                         try:
                             filter_body = response.body.decode("gb2312")
                         except Exception as ex:
                             print("Decode webpage failed: " + response.url)
                             return
        item = response.meta['item']




