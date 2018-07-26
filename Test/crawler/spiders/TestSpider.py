# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from crawler.items import TestItem
from crawler.settings import *
from scrapy import Request
import re
from scrapy.selector import Selector
import copy
from crawler.spiders import util
import time
from datetime import datetime,timedelta

class TestspiderSpider(Spider):
    name = 'CrawlerTest'
    

    def start_requests(self):
         start_urls = 'http://guba.eastmoney.com/news,of000001,381159182.html'
         yield Request(url = start_urls, callback = self.parse)

    def parse(self, response):
        #try:
        #    filter_body = response.body.decode('utf-8')
        #except:
        #    try:
        #        filter_body = response.body.decode('gbk')
        #    except:
        #        try:
        #            filter_body = response.body.decode('gb2312')
        #        except Exception as ex:
        #            print('Decode web page failed:' + response.url)
        #response.replace(body = filter_body)

        item = TestItem()
        #replynum = response.meta['replynum']
        replynum = 48

        dt = response.xpath('//div[@class="zwfbtime"]/text()').extract()
        dt = re.search('\d{4}-.+\d{2}', dt[0]).group()
        create_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        #item['content']['create_time'] = create_time

        author_url = response.xpath('//div[@id="zwconttb"]//a/@href').extract()[0]
        item['content']['author_url'] = author_url

        postcontent = response.xpath('//div[@class="stockcodec"]/text()').extract()
        #item['content']['content'] = postcontent[0].strip()
        
        posttitle = response.xpath('//div[@id="zwconttbt"]/text()').extract()
        item['content']['title'] = posttitle[0].strip()

            #    if replynum:
    #        if rptotal % 30:
    #            rptotal = replynum // 30 +1
    #        else:
    #            rptotal = replynum //30
    #        head = re.search('(.+?)\.html', response.url).group(1)
    #        for i in range(1,rptotal + 1):
    #            reply_url = head + "_" + str(i) + ".html"
    #            yield Request(url = reply_url, meta = {'item', copy.deepcopy(item)}, callback = self.parse_reply)
    #    else:
    #        yield item

    #def parse_reply(self, response):
    #    item = response.meta['item']
        
    #    replists = response.xpath('//div[@class="zwli clearfix"]')
    #    for reply in replists:
    #        reply_author = reply.xpath('//span[@class="zwnick"]//span/text').extract()


