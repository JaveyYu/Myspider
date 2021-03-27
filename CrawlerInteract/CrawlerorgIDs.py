import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo

url = 'http://irm.cninfo.com.cn/ircs/index'
orgIDs = list()
codes = pd.read_csv('stkcd.csv')
codes = list(codes['stkcd'])

# MongoDB
client = pymongo.MongoClient(host = 'localhost', port = 27018)
db = client['Interact']
collection = db['orgIDs']

# chrome配置
option = webdriver.ChromeOptions()
option.add_argument('--headless')
#option.add_argument("--start-maximized")


for code in codes:
    stkcd = '%06d' % code
    ### 以下循环
    try:
        browser = webdriver.Chrome(chrome_options=option)
        wait = WebDriverWait(browser, 5)
        browser.get(url)
        time.sleep(1)
        input_u = browser.find_element_by_id('header-search')
        input_u.send_keys(stkcd)
        browser.find_element_by_xpath('//*[@id="topApp"]/div[1]/div/div/span/span/i').click()
        time.sleep(0.5)
        browser.find_element_by_xpath('//*[@class="company-name"]//a').click()
        time.sleep(0.5)
        browser.switch_to.window(browser.window_handles[1])
        url = browser.current_url
        orgID = url.split('=')[-1]
        #orgIDs.append({'stkcd':stkcd, 'orgID':orgID})
        collection.insert_one({'stkcd':stkcd, 'orgID':orgID})
        print(str(orgID) + ': successful')
    except:
        print(str(orgID) + ':fail')
    browser.quit()

