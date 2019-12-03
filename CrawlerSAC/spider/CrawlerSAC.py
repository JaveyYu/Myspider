import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from spider.settings import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import pandas as pd

class SAC(object):

    def __init__(self):
        self.url = 'https://exam.sac.net.cn/pages/registration/sac-publicity-report.html'
        self.option = webdriver.ChromeOptions()
        #chrome 配置
        #self.option.add_argument("--window-size=1920,1080")
        self.option.add_argument("--start-maximized")
        #self.option.add_argument('--headless')
        self.option.add_argument('user-agent=' + random.choice(USER_AGENTS))
    
    def open(self):
        self.browser = webdriver.Chrome(chrome_options = self.option)
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 5)
        heads = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//th')))
        time.sleep(5)
        page_source = self.browser.page_source
        tables = Selector(text = page_source).xpath('//tbody[@id="publicityOtherList"]//td/text() | //tbody[@id="publicityOtherList"]//td//a/text()').extract()
        for table in tables:
            print(table.text)

# 选择下拉框
#elememt = browser.find_element_by_xpath('//*[@id="otcId"]')

## 实例化Select
#select = Select(elememt)
#select.select_by_index(0)

#time.sleep(2)
#table = elememts = browser.find_elements_by_xpath('//tbody[@id="publicityOtherList"]//tr//td[@align="center"]')
    def main(self):
        self.open()

if __name__ == '__main__':
    SAC.main()

