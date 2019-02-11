import requests
username = '3399516284'
password = 'wx348528'
#class Login(object):
#    def __init__(self):
login_url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=token&client_id=100229413&redirect_uri=https://xueqiu.com/service/qqconnect&scope=get_user_info,add_share,add_t'


    #def login(self, username, password):
headers = {
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
    }
post_data = {
    'u' : username,
    'p' : password
    }

response = requests.post(url = login_url, data = post_data,headers=headers)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.get('https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=token&client_id=100229413&redirect_uri=https://xueqiu.com/service/qqconnect&scope=get_user_info,add_share,add_t')
browser.switch_to.frame('ptlogin_iframe')
input_u = browser.find_element_by_id('u')
button = wait.until(EC.element_to_be_clickable((By.ID,'login_button')))
print(button)
button = browser.find_elements_by_class_name('btn')
input_u.send_keys(username)
input_p = browser.find_element_by_id('p')
input_p.send_keys(password)
button = browser.find_element_by_id('login_button')
button.click()

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')

cookie = response.cookies

response.text()