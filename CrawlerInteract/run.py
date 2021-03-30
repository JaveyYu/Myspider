import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
# running the different spiders seperately
spider_name = 'hudongyi'
#spider_name = 'test'
#spider_name = 'test_qa'
#spider_name = 'deb'
#spider_name = 'ehudong_qa'
#spider_name = 'ehudong_q'
process.crawl(spider_name)
process.start()


