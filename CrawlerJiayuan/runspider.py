import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
#spider_name = 'Jiayuan'
spider_name = 'member_info'
process.crawl(spider_name)
process.start()
