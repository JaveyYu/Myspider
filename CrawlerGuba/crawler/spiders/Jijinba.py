# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import Spider
from crawler.items import JijinbaItem
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

class JijinbaSpider(Spider):
    name = 'CrawlerJijinba'
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
        try:
            heads = re.search("of(.*?)\|", pager).group(1)
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
        except:
            yield Request(url = response.url, meta = {'item':item }, callback = self.parse_post_list)
                    

    def parse_post_list(self, response):
        item = response.meta['item']
        posts = response.xpath('//div[@class="articleh"]').extract()
        for post in posts:
            readnum = Selector(text = post).xpath('//span[@class="l1"]/text()').extract()
            if readnum:
                readnum = readnum[0]
                item['content']['readnum'] = readnum
            
            replynum = Selector(text = post).xpath('//span[@class="l2"]/text()').extract()
            if replynum:
                replynum = replynum[0]
                item['content']['replynum'] = replynum
            
            url = Selector(text = post).xpath('//span[@class="l3"]/a/@href').extract()
            posttype = Selector(text = post).xpath('//span[@class="l3"]//em[@class="hinfo"]/text()').extract()
            if url:
                url = url[0]
                guba_id = re.search('of(\d+?)_',response.url).group(1)
                if guba_id in url:
                    post_url = 'http://guba.eastmoney.com' + url
                    item['content']['post_id'] = re.split('\.', url)[0]
                    yield Request(url = post_url, meta = {'item':copy.deepcopy(item),'replynum':replynum,'posttype':posttype}, callback = self.parse_post)
    
    def parse_post(self, response):
        try:
            if response.status == 200:
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
            filter_body = re.sub('<[A-Z]+[0-9]*[^>]*>|</[A-Z]+[^>]*>', '', filter_body)
            response = response.replace(body = filter_body)
        
            item = response.meta['item']
            replynum = response.meta['replynum']
            posttype = response.meta['posttype']

            dt = response.xpath('//div[@class="zwfbtime"]/text()').extract()
            dt = re.search('\d{4}-.*:\d{2}', dt[0]).group()
            create_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            item['content']['create_time'] = create_time

            author_url = response.xpath('//div[@id="zwconttb"]//a/@href')
            if author_url:
                item['content']['author_url'] = author_url.extract()[0]

            if posttype:#针对公告的帖子
                try:
                        postcontent =response.xpath('//span[@class="zwtitlepdf"]//a/@href').extract()[0]
                        item['content']['content'] = postcontent
                except:
                    try:
                        postcontent =response.xpath('//div[@class="stockcodec"]//a/@href').extract()[0]
                        item['content']['content'] = postcontent
                    except Exception as ex:
                        print("Crawl announcement failed:" + response.url)

                posttitle = response.xpath('//div[@id="zwconttbt"]/text()').extract()
                item['content']['title'] = posttitle[0].strip() + "[Announcement]"
            else:#针对普通的帖子
                postcontent = response.xpath('//div[@class="stockcodec"]/text()').extract()
                postcontent = "".join(postcontent).strip()
                item['content']['content'] = postcontent
        
                posttitle = response.xpath('//div[@id="zwconttbt"]/text()').extract()
                item['content']['title'] = posttitle[0].strip()

            item['content']['reply'] = []
            if int(replynum):
                if int(replynum) % 30:
                    rptotal = int(replynum) // 30 +1
                else:
                    rptotal = int(replynum) //30
                head = re.search('(.+?)\.html', response.url).group(1)
                for i in range(1,rptotal + 1):
                    if i <rptotal:
                        reply_url = head + "_" + str(i) + ".html"
                        yield Request(url = reply_url, meta = {'item': item}, callback = self.parse_reply)
                    else:
                        reply_url = head + "_" + str(i) + ".html"
                        yield Request(url = reply_url, meta = {'item': item}, callback = self.parse_reply)
                        yield item
            else:
                yield item
        except Exception as ex:
            self.logger.warn('Parse Exception all: %s %s' % (str(ex), response.url))

    def parse_reply(self, response):
        item = response.meta['item']
        
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


