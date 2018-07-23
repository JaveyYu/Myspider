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


class JijinbaSpider(Spider):
    name = 'Jijinba'
     #logger = util.set_logger(name, LOG_FILE_JIJINBA)
    #handle_httpstatus_list = [404]
     #website_possible_httpstatus_list = [404]
    def start_requests(self):
         start_urls = 'http://fund.eastmoney.com/allfund.html'
         yield Request(url = start_urls, callback = self.parse)

        #解析一开始的网址
    def parse(self, response):
        fund_all = response.xpath('//div[@class="num_box"]//li//a[1]/text()')
        fund_all
        #爬取所有基金吧的地址和名字
        for fund in fund_all:
            item = JijinbaItem()
            item['content'] = {} 
            fund_name = fund.extract()
            item['content'] ['jijinba_name'] = fund_name
            url_fund = "http://jijinba.eastmoney.com/topic," + re.search('(\d+)',fund_name).group() + ".html"
            item['content'] ['jijinba_url'] = url_fund
            yield Request(url = url_fund, meta = {'item':item}, callback = self.parse_page_num)

        #解析每个论坛的页数  
    def parse_page_num(self, response):
        item = response.meta['item']
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
        hxs = Selector(response)
        posts = hxs.xpath('//div[@class="articleh"]').extract()
        for post in posts:
            readnum = Selector(text = post).xpath('//span[@class="l1"]/text()').extract()
            if readnum:
                item['content']['readnum'] = readnum[0]
            
            replynum = Selector(text = post).xpath('//span[@class="l2"]/text()').extract()
            if replynum:
                item['content']['replynum'] = replynum[0]
            
            url = Selector(text = post).xpath('//span[@class="l3"]/a/@href').extract()
            if url:
                item['content']['post_url'] = 'guba.eastmoney.com' + url[0]
                item['content']['post_id'] = re.search('of(\d+?),',url[0]).group(1)
                print(item['content']['post_id'])

  
            #yield Request(url = post_url, meta = {item:copy.deepcopy('item')}, callback = self.parse_post)

    #def parse_post(self, response):







