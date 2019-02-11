# -*- coding: utf-8 -*-
from scrapy import FormRequest
from scrapy.spiders import Spider
from crawler.items import TestItem
from crawler.settings import *
from scrapy import Request
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
#import re
#import time
#import copy
import pymongo
import json
#import pandas as pd
class TestspiderSpider(Spider):
    name = 'CrawlerTest'

    def start_requests(self):
        #start_urls = pd.read_csv('url.csv')
        start_urls = 'http://www.jiayuan.com/167625797'
        login_url = 'http://login.jiayuan.com/'
        item = TestItem()
         
        """
        初始化Redis连接
        :param host: abc
        :param port: hui
        :param password: buis
        """
        print(password)








