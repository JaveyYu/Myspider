import json
import time
from cookiespool.db import RedisClient
from login.login import CookiesGenerate


class XQCookiesGenerator(object):
    def __init__(self, website):
        """
        初始化一些对象
        :param website: 网站名称
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    #def __del__(self):
    #    self.browser.close()

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()
        
        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号：', username, '密码：', password)
                cookie = self.new_cookies(username, password)
                # 成功获取
                if cookie:
                    print('成功获取到Cookies', cookie)
                    if self.cookies_db.set(username, json.dumps(cookie)):
                        print('成功保存Cookies')
                time.sleep(15)

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return CookiesGenerate(username, password).main()


if __name__ == '__main__':
    XQCookiesGenerator.run(website)

