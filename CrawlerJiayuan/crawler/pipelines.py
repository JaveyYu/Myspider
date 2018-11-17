# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from crawler.spiders import util
from crawler.settings import *
import json
import logging

class CrawlerPipeline(object):
    def open_spider(self, spider):
        self.f = open('Member_Info37.csv','w', newline='')
        writer = csv.writer(self.f, delimiter =',')
        writer.writerow(['ID','学历','身高','购车','月薪','住房','体重','星座','民族','属相','血型','年龄','婚姻','文件名'])

    def process_item(self, item, spider):
        writer = csv.writer(self.f, delimiter =',')
        writer.writerow(list(item['content'].values()))
        return item

    def close_spide(self, spider):
        self.f.close()

#class MongoPipeline(object):
#    def __init__(self):
#        # set logger
#        self.logger = util.set_logger('pipeline', LOG_FILE_PIPELINE)

#        # 建立MongoDB server
#        self.db = util.set_mongo_server()

#        # 建立redis server
#        self.redis_server = util.set_redis_server()

    
#    def process_item(self, item, spider):
#        try:
#            # 如果item又有content又有fp，正常处理
#            if "content" in item:
#                #判断 item['content'] 是否是 dict 
#                content = item['content']
#                if type(content) == dict:
#                    self.db[spider.name].insert(content)
#                elif type(content) == unicode:
#                    content = json.loads(content)
#                    self.db[spider.name].insert(content)
#                else:
#                    self.logger.warn('Pipeline Error (unknown content type): %s %s' % (spider.name, str(type(content)), item['url']))

#        except Exception as ex:
#            self.logger.warn('Pipeline Error (others): %s %s' % (str(ex),  str(item['url'])))

