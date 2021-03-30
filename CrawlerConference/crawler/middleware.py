# -*- coding: utf-8 -*-
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
from crawler.settings import *


logger = util.set_logger("http_proxy_middleware", LOG_FILE_MIDDLEWARE)

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
        request.cookies = self.cookies[0]

class CustomHttpTunnelMiddleware(object):
    def __init__(self):
        # 代理服务器
        self.proxy_server = "http://http-dyn.abuyun.com:9020"

        # 代理隧道验证信息
        # 别随便用老子花钱买的 API！
        proxy_user = PROXY_USER
        proxy_pass = PROXY_PASS
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



class RandomCookies(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, db = 15, decode_responses=True)
        self.type = 'cookies'
        self.website = 'xueqiu'

    def random(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机Cookies
        """
        return random.choice(self.db.hvals(self.name()))

    def name(self):
        """
        获取Hash的名称
        :return: Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)


    def process_request(self, request, spider):
        request.cookies = json.loads(self.random())

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
        self.option.add_argument('--disable-images')
        self.option.add_argument('user-agent=' + random.choice(USER_AGENTS))
        self.option.add_argument('--headless')
        self.option.add_argument('log-level=3')
        #self.option.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(service_args=service_args, options = self.option)
        #self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        while True:
            try:
                self.browser.get(request.url)
                return HtmlResponse(url = request.url, body = self.browser.page_source, request = request, encoding = 'utf-8', status = 200)
            except TimeoutException:
                #return HtmlResponse(url = request.url, status = 500, request = request) 
                continue

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout = crawler.settings.get('SELENIUM_TIMEOUT'), service_args = crawler.settings.get('CHROME_SERVICE_ARGS'))





