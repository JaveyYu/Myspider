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


USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

url = 'https://exam.sac.net.cn/pages/registration/sac-publicity-report.html'
option = webdriver.ChromeOptions()
option.add_argument("--start-maximized")
option.add_argument('user-agent=' + random.choice(USER_AGENTS))
browser = webdriver.Chrome(chrome_options = option)
browser.get(url)
wait = WebDriverWait(browser, 5)
wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//th')))


institutions = browser.find_elements_by_xpath('//tbody[@id="publicityOtherList"]//tr//td[2]')
institution = institutions[0]
institution.click()
browser.switch_to.window(browser.window_handles[1])
heads = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="ui-jqgrid-hbox"]//table[@class="ui-jqgrid-htable"]')))[0].text.replace("\n", "").split()

table_contents = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//tr[@class="ui-widget-content jqgrow ui-row-ltr"]')))
staff_info=[]
for content in table_contents:
    staff_info.append(content.text.split())
staff_info = pd.DataFrame(staff_info)
wait.until(EC.element_to_be_clickable((By.XPATH,'//td[@id="next"]'))).click()
staffs = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//td[@aria-describedby="list_RPI_NAME"]')))
staff = staffs[0]
wait.until(EC.element_to_be_clickable((By.XPATH,'//tbody//td[@aria-describedby="list_RPI_NAME"]'))).click()
browser.switch_to.window(browser.window_handles[2])
heads_cert = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tr//th')))

table_contents= wait.until(EC.presence_of_all_elements_located((By.XPATH,'//table[1]//tbody//tr//td')))[2:]
staff_info = []
for content in table_contents:
    staff_info.append(content.text)

heads_record = []
heads_record = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//table[2]//tbody[1]//tr[2]')))[0].text.split()

table_contents_record= wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody[2]//tr')))
content = table_contents_record[0].text.split()

browser.close()
browser.quit()





# 选择下拉框
#elememt = browser.find_element_by_xpath('//*[@id="otcId"]')

## 实例化Select
#select = Select(elememt)
#select.select_by_index(0)

#time.sleep(2)
#table = elememts = browser.find_elements_by_xpath('//tbody[@id="publicityOtherList"]//tr//td[@align="center"]')




self.institutions = pd.DataFrame(self.table_content, columns = self.head)
self.institutions.to_csv('institutions.csv',index=0, encoding = "utf-8")




