from cookiespool.db import RedisClient
from cookiespool.config import *
import pandas as pd

class Import(object):
    def __init__(self):
        self.conn = RedisClient('accounts', 'xueqiu')

    def set(self, account, sep='----'):
        username, password = account.split(sep)
        result = self.conn.set(username, password)
        username, password = account.split(sep)
        print('账号：%s，密码：%s'%(username, password))
        print('录入成功\n' if result else '账号已存在\n')

    def scan(self):
        accouns_path = 'accounts/' + ACCOUNTS_FILE
        accounts = pd.read_table(accouns_path, header=None)
        for account in accounts[0]:
            self.set(account)
        print('账号录入完成\n')

if __name__ == '__main__':
    scan()

