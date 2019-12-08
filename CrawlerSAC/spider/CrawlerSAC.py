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
        #self.option.add_argument("--proxy-server=http://47.112.218.30:8000")
        #self.option.add_argument("--window-size=1920,1080")
        self.option.add_argument("--start-maximized")
        #self.option.add_argument('--headless')
        self.option.add_argument('user-agent=' + random.choice(USER_AGENTS))
    
    def institution_page(self):
        '''
        爬取证券公司的机构信息统计
        '''
        # 首页表格headline
        heads = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//th')))
        self.head = []
        for head in heads:
            self.head.append(head.text.replace("\n", ""))

        time.sleep(5)
        # 首页表格内容
        page_source = self.browser.page_source
        table_contents = Selector(text = page_source).xpath('//tbody[@id="publicityOtherList"]//td/text() | //tbody[@id="publicityOtherList"]//td//a/text()').extract()
        self.table_content=[]
        for i in range(0,len(table_contents),11):
            self.table_content.append(table_contents[i:i+11])
        self.institutions = pd.DataFrame(self.table_content, columns = self.head)
        self.institutions.to_csv('institutions.csv',index=0, encoding = "utf-8")

    def staff_info_page(self):
        '''
        爬取各机构中所有人员的基本信息
        '''
        table_contents = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//tr[@class="ui-widget-content jqgrow ui-row-ltr"]')))

        for content in table_contents:
            self.staff_info.append(content.text.split())
        
    def staff_certificate_page(self):
        '''
        爬取每个人员的证书基本信息及注册变更记录
        '''

        # 证书基本信息
        table_contents_cert = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//table[1]//tbody//tr//td')))[2:]
        cert_info = []
        for content in table_contents_cert:
            cert_info.append(content.text)
        self.cert_info.append(cert_info)
        
        # 注册变更记录
        table_contents_record = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//table[2]//tbody[1]//tr[2]')))
        for record in table_contents_record:
            self.record.append(record.text.split())


    def main(self):
        self.browser = webdriver.Chrome(chrome_options = self.option)
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 5)
        print('开始获取首页机构信息....\n')
        # 第一层institution信息界面
        self.institution_page()
        print('机构信息获取完成\n')
        # 获取第一层页面上的所有insitution链接位置
        institutions = self.browser.find_elements_by_xpath('//tbody[@id="publicityOtherList"]//tr//td[2]')
        
        for i in range(0,len(institutions)):
            print('正在获取第%d个机构的人员信息\n'%(i+1))
            institutions[i].click()
            # 切换到第二层staff窗口
            self.browser.switch_to.window(self.browser.window_handles[1])
            # 确定页数
            staff_page_num = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//td[@dir="ltr"]//span[@id="sp_1"]')))[0].text
            staff_page_num = int(staff_page_num)
            # staff页面的表格headline
            self.heads_staff = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="ui-jqgrid-hbox"]//table[@class="ui-jqgrid-htable"]')))[0].text.replace("\n", "").split()
            self.staff_info = []
            page = 1
            while page <= staff_page_num:
                print('正获取第%d页的人员信息\n'%page)
                if page>1:
                    self.wait.until(EC.element_to_be_clickable((By.XPATH,'//td[@id="next"]'))).click()
                self.staff_info_page()
                # 获取该页所有staff的链接位置
                staffs = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tbody//td[@aria-describedby="list_RPI_NAME"]')))
                # 依次点击进入staff的证书页面
                for j in range(0,len(staffs)):
                    # 控制抓取的速度
                    #time.sleep(5)
                    print('正获取第%d页第%d个人员的证书及注册记录\n'%(page, j+1))
                    staffs[j].click()
                    #time.sleep(5)
                    self.browser.switch_to.window(self.browser.window_handles[2])
                    # 证书基本信息表格headline
                    self.heads_cert = []
                    heads_cert = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//tr//th')))
                    for head in heads_cert:
                        self.heads_cert.append(head)
                    # 注册变更记录表格headline
                    self.heads_record = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//table[2]//tbody[1]//tr[2]')))[0].text.split()
                    # 获取证书基本信息合注册变更记录内容
                    self.cert_info = []
                    self.record = []
                    self.staff_certificate_page()
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[1])
                page = page + 1
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])

        self.browser.quit()
        self.staff_info = pd.DataFrame(self.staff_info, columns = self.heads_staff)
        self.cert_info = pd.DataFrame(self.cert_info, columns = self.heads_cert)
        self.record = pd.DataFrame(self.record, columns = self.heads_record)
        self.staff_info.to_csv('staff_info.csv',index=0, encoding = "utf-8")
        self.cert_info.to_csv('cert_info.csv',index=0, encoding = "utf-8")
        self.record.to_csv('staff_record.csv',index=0, encoding = "utf-8")


if __name__ == '__main__':
    SAC.main()

