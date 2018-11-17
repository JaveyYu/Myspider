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
         
        yield Request(url = login_url, callback = self.parse_login)

    def parse_login(self, response):
        login_data = {
            'name':'18612209787',
            'password':'shiyan5201314',
            }
        yield FormRequest.from_response(response, formdata = login_data, callback = self.parse)

    def parse(self, response):
        url = 'http://search.jiayuan.com/v2/search_v2.php'
        yield FormRequest(url = url, formdata = {'sex': 'f'}, meta = {'url':url, 'sex': 'f'}, callback = self.parse_page_num)
        #yield FormRequest(url = url, formdata = {'sex': 'm'}, meta = {'url':url, 'sex': 'm'}, callback = self.parse_page_num)

    def parse_page_num(self, response):
        url = response.meta['url']
        sex = response.meta['sex']
        result = json.loads(response.body)
        pageTotal = result['pageTotal']
        for p in range(1,2):
            yield FormRequest(url = url, formdata = {'sex' : sex, 'p' : str(p+1)}, meta = {'sex' : sex}, callback = self.parse_id)


    def parse_id(self, response):
        sex = response.meta['sex']
        result = json.loads(response.body)
        for uI in result['userInfo']:
            ID = uI['realUid']
            url =  'http://www.jiayuan.com/' + str(ID) + '?fxly=search_v2'
            print(url)
            yield Request(url = url, meta = {'ID':ID, 'sex':sex}, callback = self.parse_item)



    def parse_item(self, response):
        #pass
        print(str(response.url) + 'has been requested')
        item = TestItem()
        ID = response.meta['ID']
        sex = response.meta['sex']
        #try:
        item['content'] = {}
        item['content']['ID'] = response.meta['ID']
        item['content']['sex'] = response.meta['sex']

        box = response.xpath('//div[@class="js_box"]').extract()
        
        introduction = Selector(text = box[0]).xpath('//div[@class="js_text"]/text()').extract()[0].strip()
        item['content']['introduction'] = introduction

        requirement = {}
        requirement['age'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[0]
        requirement['height'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[1]
        requirement['ethnic'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[2]
        requirement['education'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[3]
        requirement['photo'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[4]
        requirement['marriage'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[5]
        requirement['integrity'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con"]/text()').extract()[6]
        requirement['residence'] = Selector(text = box[2]).xpath('//div[@class="ifno_r_con_1"]/text()').extract()[0]
        item['content']['requirement'] = requirement

        lifestyle = {}
        try:
            lifestyle['smoke'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[0]
            lifestyle['alcohol'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[1]
            lifestyle['exercise'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[2]
            lifestyle['diet'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[3]
            lifestyle['shopping'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[4]
            lifestyle['faith'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[5]
            lifestyle['Schedule'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[6]
            lifestyle['intercourse'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[7]
            lifestyle['consumption'] = Selector(text = box[3]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[8]
        except Exception as ex:
            lifestyle['content'] = 'unfilled'

        lifestyle['housework'] = Selector(text = box[3]).xpath('//dd[@class="cur"]/text()').extract()[0]
        lifestyle['pet'] = Selector(text = box[3]).xpath('//dd[@class="cur"]/text()').extract()[1]
        item['content']['lifestyle'] = lifestyle

        economy = {}
        economy['salary'] = Selector(text = box[4]).xpath('//div[@class="ifno_r_con"]/text()').extract()[0]
        economy['house'] = Selector(text = box[4]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[0]
        economy['car'] = Selector(text = box[4]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[1]
        economy['econ_concept'] = Selector(text = box[4]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[2]
        economy['investment'] = Selector(text = box[4]).xpath('//div[@class="ifno_r_con_1"]/em/text()').extract()[0]
        economy['foreign_debt'] = Selector(text = box[4]).xpath('//div[@class="ifno_r_con_1"]/em/text()').extract()[1]
        item['content']['economy'] = economy

        working = {}
        try:
            working['occupation'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[0]
            working['company_industry'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[1]
            working['company_type'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[2]
            working['welfare'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[3]
            working['working_status'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[4]
            working['working_transfer'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[5]
            working['career&family'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[6]
            working['working_overseas'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[7]
        except Exception as ex:
            working['working_content'] = 'unfilled'
        try:
            working['college'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[8]
            working['major'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[9]
            working['language_skills'] = Selector(text = box[5]).xpath('//div[@class="ifno_r_con_1"]/em/text()').extract()[0]
        except Exception as ex:
            working['study_content'] = 'unfilled'
        item['content']['working'] = working

        marr_cnpt = {}
        marr_cnpt['birthplace'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[0]
        marr_cnpt['regd_res'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[1]
        marr_cnpt['nation'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[2]
        marr_cnpt['character'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[3]
        marr_cnpt['humor'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[4]
        marr_cnpt['temper'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[5]
        marr_cnpt['treat'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[6]
        marr_cnpt['children'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[7]
        marr_cnpt['marr_time'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[8]
        marr_cnpt['exotic_love'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[9]
        try:
            marr_cnpt['live_parents'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[10]
            marr_cnpt['rankings'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[11]
            marr_cnpt['bro&sis'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[12]
            marr_cnpt['parents_econ'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[13]
            marr_cnpt['medi_ins'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con"]/em/text()').extract()[14]
            marr_cnpt['ideal_marr'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con_1"]/em/text()').extract()[0]
            marr_cnpt['parents_work'] = Selector(text = box[6]).xpath('//div[@class="ifno_r_con_1"]/em/text()').extract()[1]
        except Exception as ex:
            marr_cnpt['family_content'] = 'unfilled'
        item['content']['marr_cnpt'] = marr_cnpt
        #print(item)
        yield item
        

