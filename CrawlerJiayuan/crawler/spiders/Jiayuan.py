# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class JiayuanSpider(scrapy.Spider):
    name = 'Jiayuan'


    def start_requests(self):
        path = 'crawler/spiders/'
        start_urls = pd.read_csv(path + 'url.csv')
        for url in start_urls:
           yield Request(url = url, callback = self.parse)

    def parse(self, response):
        title = response.xpath("//div[@class='fl f_gray_999']/em/text()").extract()
        content = response.xpath("//div[@class='fl pr']/em/text()").extract()






