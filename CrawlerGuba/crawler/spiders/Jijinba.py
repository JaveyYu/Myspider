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
from datetime import datetime,timedelta

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
            for i in range(1,page_total + 1):
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

        item = response.meta['item']
        replynum = response.meta['replynum']

        dt = response.xpath('//div[@class="zwfbtime"]/text()').extract()
        dt = re.search('\d{4}-.+\d{2}', dt[0]).group()
        create_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        item['content']['create_time'] = create_time

        author_url = response.xpath('//div[@id="zwconttb"]//a/@href').extract()[0]
        item['content']['author_url'] = author_url

        postcontent = response.xpath('//div[@class="stockcodec"]/text()').extract()
        psotcontent = postcontent[0].strip()
        item['content']['content'] = content
        
        posttitle = response.xpath('//div[@id="zwconttbt"]/text()').extract()
        posttitle = posttitle[0].strip()
        item['content']['title'] = posttitle

        if replynum:
            if rptotal % 30:
                rptotal = replynum // 30 +1
            else:
                rptotal = replynum //30
            head = re.search('(.+?)\.html', response.url).group(1)
            for i in range(1,rptotal + 1):
                reply_url = head + "_" + str(i) + ".html"
                yield Request(url = reply_url, meta = {'item', copy.deepcopy(item)}, callback = self.parse_reply)
        else:
            yield item

    def parse_reply(self, response):
        item = response.meta['item']
        
        replists = response.xpath('//div[@class="zwli clearfix"]')
        for reply in replists:
            reply_author = reply.xpath('//span[@class="zwnick"]//span/text').extract()



