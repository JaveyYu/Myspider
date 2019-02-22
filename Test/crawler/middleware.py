# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import redis
import time
import json
import base64
from crawler.settings import *
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.web._newclient import ResponseNeverReceived
from twisted.python.failure import Failure
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError, TCPTimedOutError, ConnectionDone
from datetime import datetime
from scrapy import signals
from crawler.spiders import util
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from logging import getLogger


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

class CustomHttpTunnelMiddleware(object):
    def __init__(self):
        # 代理服务器
        self.proxy_server = "http://http-dyn.abuyun.com:9020"

        # 代理隧道验证信息
        # 别随便用老子花钱买的 API！
        proxy_user = "H9834503A6P7XRKD"
        proxy_pass = "7C352A9FD0AF0C4B"
        auth = (proxy_user + ":" + proxy_pass).encode()
        self.proxy_auth = "Basic " + (base64.urlsafe_b64encode(auth)).decode()

    # 改造输入 request，增加代理
    def add_proxy(self, request):
        request.meta["proxy"] = self.proxy_server
        request.headers["Proxy-Authorization"] = self.proxy_auth
        request.dont_filter = True
        logger.debug("Use proxy to request %s" % request.url)
        request.priority = request.priority + RETRY_PRIORITY_ADJUST
        #time.sleep(HTTPPROXY_DELAY)
        return request

    def process_request(self, request, spider):
        # 所有spider全都开启代理
        request.meta['proxy'] = self.proxy_server
        request.headers['Proxy-Authorization'] = self.proxy_auth            

    def process_response(self, request, response, spider):         
        # 如果代理API请求太频繁，重新请求
        if response.status in [429]:
            logger.info("%s Please slow down!" % response.status)
            return self.add_proxy(request)

        # response正常，进入后续处理
        return response

    def process_exception(self, request, exception, spider):
        print("process_exception_middleware")
        DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError, TCPTimedOutError, ConnectionDone)

        if isinstance(exception, (ConnectionDone)):
            logger.info("Error: ConnectionDone")
            return self.add_proxy(request)

        if isinstance(exception, DONT_RETRY_ERRORS):
            logger.info("Middleware Exception %s, %s" % (request.url, exception))
            return self.add_proxy(request)


class SeleniumMiddleware(object):
    def __init__(self, timeout, service_args):
        self.logger = getLogger
        self.timeout = timeout
        #self.chrome_options = Options()
        #self.chrome_options.add_argument('--headless')
        #self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(service_args=service_args)#, options = self.chrome_options)
        #self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.username = USERNAME
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        try:
            self.browser.get(request.url)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'iconfont')))
            #找到首页上的登录按钮并点击
            self.browser.find_element_by_xpath('//div[@class="nav__login__btn"]//i[@class="iconfont"]').click()
            #找到登录界面的QQ登录按钮并点击
            self.browser.find_element_by_xpath('//*[@id="app"]/div[4]/div[1]/div[3]/div[2]/div[5]/ul/li[2]/a/i').click()
            #找到账号密码登录按钮并点击
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.switch_to.frame('ptlogin_iframe')
            self.browser.find_element_by_id('switcher_plogin').click()
            #输入账号密码
            input_u = self.browser.find_element_by_id('u')
            input_u.send_keys(self.username)
            input_p = self.browser.find_element_by_id('p')
            input_p.send_keys(self.password)
            #点击授权并登录
            time.sleep(1)
            self.browser.find_element_by_class_name('btn').click()
            return HtmlResponse(url = request.url, body = self.browser.page_source, request = request, encoding = 'utf-8', status = 200)
        except TimeoutException:
            return HtmlResponse(url = request.url, status = 500, request = request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout = crawler.settings.get('SELENIUM_TIMEOUT'), service_args = crawler.settings.get('CHROME_SERVICE_ARGS'))

