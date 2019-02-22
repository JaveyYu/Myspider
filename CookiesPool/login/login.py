import os
import cv2
import time
import string  
import zipfile
import random
import pymongo
import numpy as np
from PIL import Image
from io import BytesIO
from retrying import retry
from cookiespool import util
from cookiespool.config import *
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login.proxy_extension import create_proxy_auth_extension


class CookiesGenerate(object):
    def __init__(self, username, password):
        self.url = 'https://xueqiu.com/'
        self.username = username
        self.password = password
        #self.logger = util.set_logger('login', LOG_FILE_LOGIN)
        self.__init__chrome_option()

    def __init__chrome_option(self):
        self.option = webdriver.ChromeOptions()
        #chrome 配置
        self.option.add_argument("--start-maximized")
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--disable-javascript')
        self.option.add_argument('--disable-java')
        self.option.add_argument('--disable-images')
        self.option.add_argument('user-agent=' + random.choice(USER_AGENTS))
        
        #代理配置
        if PROXY_ENABLED:
            proxy_auth_plugin_path = create_proxy_auth_extension(
                proxy_host=PROXYHOST,
                proxy_port=PROXYPORT,
                proxy_username=PROXYUSER,
                proxy_password=PROXYPASS)
            self.option.add_extension(proxy_auth_plugin_path)
        #else:
            #self.option.add_argument('--headless')
            #self.option.add_argument('--disable-gpu')
    def login(self, count):
        while True:
            try:
                self.open()
                self.username_input()
                self.password_input()
                self.submit(count)
                break
            except:
                self.browser.quit()
                time.sleep(0.5)

    def open(self):
        self.browser = webdriver.Chrome(chrome_options=self.option)
        #self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 5)
        self.browser.get(self.url)
        if PROXY_ENABLED:
            #若开启代理，会弹出一个奇怪的界面，点击首页
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/nav/div/div[1]/div/a[1]'))).click()
        #找到首页上的登录按钮并点击
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="nav__login__btn"]//i[@class="iconfont"]'))).click()
        #找到登录界面的QQ登录按钮并点击
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[4]/div[1]/div[3]/div[2]/div[5]/ul/li[2]/a/i'))).click()
        #找到账号密码登录按钮并点击
        time.sleep(0.5)
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.wait.until(EC.frame_to_be_available_and_switch_to_it('ptlogin_iframe'))
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'帐号密码登录'))).click()

    def username_input(self):
        #输入账号
        input_u = self.browser.find_element_by_id('u')
        input_u.send_keys(self.username)
        time.sleep(1)

    def password_input(self):
        #输入密码
        input_p = self.browser.find_element_by_id('p')
        input_p.send_keys(self.password)
        #点击授权并登录
        time.sleep(1)

    def submit(self, count):
        #点击提交按钮
        print('%s: 正在尝试第%d次登录：' % (self.username,count))
        self.browser.find_element_by_class_name('btn').click()

    def get_slider(self):
        """
        定位滑块
        """
        #重新调整到窗口1，切换进入验证码的嵌套iframe
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.switch_to.frame('ptlogin_iframe')
        self.browser.switch_to.frame('tcaptcha_iframe')
        slider = self.wait.until(EC.element_to_be_clickable((By.ID,'tcaptcha_drag_button')))
        return slider

    def get_position(self, id):
            img = self.wait.until(EC.presence_of_element_located((By.ID,id)))
            location = img.location
            size = img.size
            top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
            return (top, bottom, left, right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self):
        (top, bottom, left, right) = self.get_position('slideBg')
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left+100, top+100, right+100, bottom+100))
        return captcha

    def match_template(self, image):
        for i in range(1,5):
            template = Image.open('login/template/template%s.png'%i)
            pixel_tmp = image.getpixel((101,101))
            pixel_img = image.getpixel((101,101))
            if abs(pixel_tmp[0]-pixel_img[0]) < 5:
                return i
                break

    def get_distance(self, i):
        if i ==3:
            distance = 170+random.randint(-1,1)
        else:
            distance = 175+random.randint(-1,1)
        return distance

    def get_track(self, distance):
        track=[]
        #间隔通过随机范围函数来获得,每次移动一步或者两步
        x=random.randint(1,3)
        #生成轨迹并保存到list内
        while distance-x>=5:
            track.append(x)
            distance=distance-x
            x=random.randint(1,3)
        #最后五步都是一步步移动
        for i in range(distance):
            track.append(1)
        return track

    def move_to_gap(self, slider, tracks):
        # 实例化一个action对象
        time.sleep(0.5)
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=random.randint(-1,1)).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def verify(self):
        slider = self.get_slider()
        captcha = self.get_image()
        i = self.match_template(captcha)
        distance = self.get_distance(i)
        tracks = self.get_track(distance)
        self.move_to_gap(slider, tracks)

    def verify_successfully(self):
        try:
            self.browser.find_element_by_id('slideBg') 
            return False
        except:
            print(self.username, '：验证成功')
            return True

    def login_successfully(self):
        self.browser.switch_to.window(self.browser.window_handles[0])
        #要设置一定时间的延迟网页才会加载完,title 1.5s
        time.sleep(1.5)
        if self.browser.title == '我的首页 - 雪球':
            return True
        else:
            return False

    def get_error(self):
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.switch_to.frame('ptlogin_iframe')
        err_msg = self.browser.find_element_by_xpath( '//*[@id="err_m"]').text
        return err_msg


    def get_cookie(self):
        cookies = self.browser.get_cookies()
        cookie = {}
        for item in cookies:
            if (item['name'] == 'xq_a_token') | (item['name']=='xq_r_token'):
                cookie[item['name']] = item['value']
        return cookie

    def main(self):
        count = 1
        while True:
            self.login(count)
            if self.login_successfully():
                #self.logger.info('%s: 无需验证码登录成功' % (self.username))
                print('%s: 无需验证码登录成功' % (self.username))
                cookie = self.get_cookie()
                self.browser.quit()
                return cookie
            else: 
                while True:
                    try:
                        #self.logger.info('%s: 开始验证码验证' % (self.username))
                        print('%s: 开始验证码验证....' % (self.username))
                        self.verify()
                        time.sleep(0.5)
                        while not self.verify_successfully():
                            self.verify()
                            time.sleep(0.5)
                    except:
                        if self.login_successfully():
                            #self.logger.info('%s: 登录成功' % (self.username))
                            print('%s: 登录成功' % (self.username))
                            cookie = self.get_cookie()
                            return cookie
                            self.browser.quit()
                        else:
                            #self.logger.info('%s: 登录失败' % (self.username))
                            err_msg = self.get_error()
                            print('%s: 登录失败，失败原因：%s\n' % (self.username,err_msg))
                            #self.browser.quit()
                            if '密码不正确' in err_msg:
                                count = count + 1
                                time.sleep(2)
                                self.password_input()
                                self.submit(count)
                            else:
                                self.browser.quit()
                                return None
                                

if __name__ == '__main__':
    CookiesGenerate.main()


