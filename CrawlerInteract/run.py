import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
# running the different spiders seperately
#spider_name = 'hudongyi'
spider_name = 'hudongyi2'
#spider_name = 'test'
#spider_name = 'deb'
process.crawl(spider_name)
process.start()


