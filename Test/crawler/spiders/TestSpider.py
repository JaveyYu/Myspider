# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from crawler.items import TestItem
from crawler.settings import *
from scrapy import Request
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
import re
import time
import copy
import pymongo
import json

class TestspiderSpider(Spider):
    name = 'CrawlerTest'
    

    def start_requests(self):
         start_urls = 'http://guba.eastmoney.com/news,of160630,230625294_1.html'
         item = TestItem()
         item['content'] = {}
         item['content']['reply'] = []
         head = 'http://guba.eastmoney.com/news,of160630,230625294'
         rptotal = 1
         yield Request(url = start_urls, meta = {'item': item, 'head':head, 'page':1, 'rptotal':rptotal}, callback = self.parse_reply)

    #def parse(self, response):
    #    pass


    def parse_reply(self, response):
        item = response.meta['item']
        rptotal = response.meta['rptotal']
        head = response.meta['head']
        page = response.meta['page']
        
        replists = response.xpath('//div[@class="zwli clearfix"]').extract()
        for replist in replists:
            reply = {} 
            try:
                reply_author = Selector(text = replist).xpath('//span[@class="zwnick"]//a/text()').extract()[0]
                reply['reply_author'] = reply_author
                reply_authour_url = Selector(text = replist).xpath('//span[@class="zwnick"]//a/@href').extract()[0]
                reply['reply_author_url'] = reply_authour_url
            except:
                try:
                    reply_author = Selector(text = replist).xpath('//span[@class="gray"]/text()').extract()[0]
                    reply['reply_author'] = reply_author
                except Exception as ex:
                    print("Decode webpage failed:" + response.url)
                    return
            

            reply_time = Selector(text = replist).xpath('//div[@class="zwlitime"]/text()').extract()[0]
            reply_time = re.search('\d{4}-.*:\d{2}', reply_time).group()
            reply_time = datetime.strptime(reply_time, "%Y-%m-%d %H:%M:%S")
            reply['reply_time'] = reply_time


            reply_content = Selector(text = replist).xpath('//div[@class="zwlitext stockcodec"]/text()').extract()
            if reply_content:
                reply['reply_content'] = reply_content[0].strip()


            #xpath的@class后面引号内容最后带有一个空格
            reply_quote_author = Selector(text = replist).xpath('//div[@class="zwlitalkboxtext "]//a/text()').extract()
            if reply_quote_author:
                reply['reply_quote_author'] = reply_quote_author[0]
                
            reply_quote_author_url = Selector(text = replist).xpath('//div[@class="zwlitalkboxtext "]//a/@href').extract()
            if reply_quote_author_url:
                reply['reply_quote_author_url'] = reply_quote_author_url[0]

            reply_quote_content = Selector(text = replist).xpath('//div[@class="zwlitalkboxtext "]//span/text()').extract()
            if reply_quote_content:
                reply['reply_quote_content'] = reply_quote_content[0].strip()

            item['content']['reply'].append(reply)

            print(item['content']['reply'][0:])

        if page < rptotal:
            reply_url = head + "_" + str(page + 1) + ".html#storeply"
            yield Request(url = reply_url, meta = {'item': item, 'head':head, 'page':page + 1, 'rptotal':rptotal}, callback = self.parse_reply)
        else:
            yield item
                       



