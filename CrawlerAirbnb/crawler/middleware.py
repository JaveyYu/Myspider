# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import redis
import time
import json
from datetime import datetime
from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from logging import getLogger
from crawler.settings import *


class RandomRequestHeaders(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents, cookies):
        self.agents = agents
        self.cookies = cookies

    @classmethod
    def from_crawler(cls, crawler):
        ua = crawler.settings.getlist('USER_AGENTS')
        ck = crawler.settings.getlist('COOKIES')
        return cls(ua, ck)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))       


class SeleniumMiddleware(object):
    def __init__(self, timeout, service_args):
        self.logger = getLogger
        self.timeout = timeout

        #chrome 配置
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--start-maximized")
        #self.option.add_argument('--ignore-certificate-errors')
        #self.option.add_argument('--disable-javascript')
        #self.option.add_argument('--disable-java')
        #self.option.add_argument('--disable-images')
        self.option.add_argument('user-agent=' + random.choice(USER_AGENTS))
        #chrome_options.add_experimental_option("prefs", {
        #      "download.default_directory": "/path/to/download/dir",
        #      "download.prompt_for_download": False,
        #    })
        #self.option.add_argument('--headless')
        #self.option.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(service_args=service_args, options = self.option)
        #self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)



    #def __del__(self):
        #self.browser.close()

    def process_request(self, request, spider):
        if 'api' not in request.url:
            while True:
                try:
                    self.browser.get(request.url)
                    self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_13ky0r6y"]')))
                    return HtmlResponse(url = request.url, body = self.browser.page_source, request = request, encoding = 'utf-8', status = 200)
                except TimeoutException:
                    #return HtmlResponse(url = request.url, status = 500, request = request) 
                    continue

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout = crawler.settings.get('SELENIUM_TIMEOUT'), service_args = crawler.settings.get('CHROME_SERVICE_ARGS'))

