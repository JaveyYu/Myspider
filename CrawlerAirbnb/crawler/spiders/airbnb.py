# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from crawler.items import AirbnbItem
from crawler.settings import *
from scrapy import FormRequest
from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from crawler.spiders import util
from datetime import datetime,timedelta
import re
import time
import copy
import pymongo
import json

class AirbnbSpider(Spider):
    name = 'airbnb'
    search_item = '杭州'
    search_type = '房源'
    IDs =[]

    def start_requests(self):
        start_url = 'https://zh.airbnb.com/s/' 
        if self.search_type == '房源':
            url = start_url + 'homes?refinement_paths%5B%5D=%2Fhomes&query=' + self.search_item
        else:
            url = start_url + 'experiences?refinement_paths%5B%5D=%2Fexperiences&query=' + self.search_item
        page = 1
        yield Request(url, meta={'url':url, 'page':page}, callback = self.parse_id)

    #def parse_page_max(self, response):
    #    url = response.meta['url']
    #    #获取下一页按钮
    #    page_choice = response.xpath('//ul[@data-id="SearchResultsPagination"]//li/@data-id').extract()
    #    #获取页面总数
    #    page_max = page_choice[-1].split('-')[1]
    #    page_max = int(page_max)

    #    page = 1
    #    yield Request(url, meta={'page':page, 'page_max':page_max}, callback = self.parse_id)

    def parse_id(self, response):
        page = response.meta['page']
        if page == 1:
            #获取下一页按钮
            page_choice = response.xpath('//ul[@data-id="SearchResultsPagination"]//li/@data-id').extract()
            #获取页面总数
            page_max = page_choice[-1].split('-')[1]
            page_max = int(page_max)
        else:
            page_max = response.meta['page_max']


        #获取每页上所有房源的ID
        ID_Path = response.xpath('//div[@class="_13ky0r6y"]//a/@href').extract()
        IDs =[ID.split('/')[-1] for ID in ID_Path]

        #获取下一页的链接
        next = response.xpath('//li[@class="_b8vexar"]//a/@href').extract()[0]
        next_url = 'https://zh.airbnb.com' + next

        for id in IDs:
            item = AirbnbItem()
            item['content'] = {}
            item['content']['id'] = id
            url_detail = 'https://zh.airbnb.com/api/v2/pdp_listing_details/%s?_format=for_rooms_show&adults=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'%id
            yield Request(url_detail, meta = {'item':item,  'id':id, 'page':page, 'page_max':page_max}, callback = self.parse_details)
        
        if page < page_max:
            yield Request(next_url, meta={'page':page+1, 'page_max':page_max}, callback = self.parse_id)


    def parse_details(self, response):
        item = response.meta['item']
        id = response.meta['id']

        detail = json.loads(response.body)
        item['content']['detail'] = detail['pdp_listing_detail']

        url_booking = 'https://zh.airbnb.com/api/v2/pdp_listing_booking_details?force_boost_unc_priority_message_type=&listing_id=%s&_format=for_web_dateless&_interaction_type=pageload&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=zh'%id

        yield Request(url_booking, meta = {'item':item,  'id':id}, callback = self.parse_booking_details)

    def parse_booking_details(self, response):
        item = response.meta['item']
        id = response.meta['id']

        booking_details = json.loads(response.body)
        item['content']['booking_details'] = booking_details['pdp_listing_booking_details']

        url_calendar = 'https://zh.airbnb.com/api/v2/calendar_months?_format=with_conditions&count=4&listing_id=%s&month=1&year=2019&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=zh'%id

        yield Request(url_calendar, meta = {'item':item,  'id':id}, callback = self.parse_calendar)

    def parse_calendar(self, response):
        item = response.meta['item']
        id = response.meta['id']

        calendar = json.loads(response.body)
        item['content']['calendar'] = calendar['calendar_months']
        yield item

            