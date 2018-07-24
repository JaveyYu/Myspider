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

class TestSpider(Spider):
    name = 'test'

    def start_requests(self):
         start_urls = 'http://guba.eastmoney.com/list,of000004.html'
         yield Request(url = start_urls, callback = self.parse_page_num)
    
    def parse_page_num(self, response):
            #item = response.meta['item']
            item = JijinbaItem()
            pager = response.xpath('//div[@class="pager"]').extract()[0]
            postnums = re.search("_\|(\d+)\|",pager).group(1)
            item['content']['postnums'] = int(postnums)
            heads = re.search("of(.*?)\|",pager).group(1)

            if item['content']['postnums'] % 80:
                page_total = item['content']['postnums'] // 80 + 1
            else:
                page_total = item['content']['postnums'] // 80

            if page_total:
                for i in range(1,page_total):
                    page_url = "http://guba.eastmoney.com/list,of"+heads+str(i)+".html"
                    yield Request(url = page_url, meta = {'item':item }, callback = self.parse_post_list)
            else:
                   yield item


    def parse_post_list(self, response):
            item = response.meta['item']
            posts = response.xpath('//div[@class="articleh"]').extract()
            for post in posts:
                readnum = Selector(text = post).xpath('//span[@class="l1"]/text()').extract()
                if readnum:
                    readnum = readnum[0]
                    item['content']['readnum'] = readnum[0]
            
                replynum = Selector(text = post).xpath('//span[@class="l2"]/text()').extract()
                if replynum:
                    replynum = replynum[0]
                    item['content']['replynum'] = replynum
            
                url = Selector(text = post).xpath('//span[@class="l3"]/a/@href').extract()
                if url:
                    url = url[0]
                    guba_id = re.search('of(\d+?)_',response.url).group(1)
                    if guba_id in url:
                        post_url = 'http://guba.eastmoney.com' + url
                        item['content']['post_id'] = re.split('\.', url)[0]
                        yield Request(url = post_url, meta = {'item':copy.deepcopy(item),'replynum':replynum}, callback = self.parse_post)
    
    def parse_post(self, response):
            try:
                filter_body = response.body.decode('utf-8')
            except:
                try:
                    filter_body = response.body.decode('gbk')
                except:
                    try:
                        filter_body = response.body.decode('gb2312')
                    except Exception as ex:
                        print('Decode web page failed:' + response.url)
            response.replace(body = filter_body)
            item = response.meta['item']
            dt = response.xpath('//div[@class="zwfbtime"]/text()').extract()
            dt = re.search('\d{4}-.+\d{2}', dt[0]).group()
            create_time = datetime.striptime(dt, '%Y-%m-%d %H:%M:%S')
            item['content']['create_time'] = create_time



