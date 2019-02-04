import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
# running the different spiders seperately
spider_name = 'cube_info' #                    ZH/SP-1901 Done      需要开代理！
#spider_name = 'xq_cube_rb'#                        ZH/SP-1901 Done      需要开代理！
#spider_name = 'xq_cube_rb_sp'#                   SP-1901       Done      需要开代理！
#spider_name = 'xq_cube_ret'#                       ZH/SP-1901 Done      需要开代理！DOWNLOAD_DELAY = 0.05   
#spider_name = 'xq_cube_ret_sp'#                  SP-1901       Done      需要开代理！DOWNLOAD_DELAY = 0.005
#spider_name = 'xq_user_fans'#                      ZH/SP-1901 Done      不用开代理！
#spider_name = 'xq_user_follow'#                   ZH/SP-1901 Done      不用开代理！
#spider_name = 'xq_user_info'#                       ZH/SP-1901 Done      不用开代理！
#spider_name = 'xq_user_info_weibo'#           1901             Done      需要开代理！DOWNLOAD_DELAY = 0.025
#spider_name = 'xq_user_stock'#                    ZH/SP-1901  Done      不用开代理！
#spider_name = 'xq_user_cmt_zh'#                                         Done      需要开代理！DOWNLOAD_DELAY = 2
#spider_name = 'xq_user_cmt_sp'#                 1901              Done      需要开代理！DOWNLOAD_DELAY = 2
process.crawl(spider_name)
process.start()
 


