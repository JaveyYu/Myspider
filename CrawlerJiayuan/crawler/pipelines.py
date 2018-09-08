# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class CrawlerPipeline(object):
    def open_spider(self, spider):
        self.f = open('Jiayuan.csv','w')
        writer = csv.writer(self.f, delimiter =',')
        writer.writerow(['ID','学历','身高','购车','月薪','住房','体重','星座','民族','属相','血型'])

    def process_item(self, item, spider):
        writer = csv.writer(self.f, delimiter =',')
        writer.writerow(list(item.values()))
        return item

    def close_spide(self, spider):
        self.f.close()