import random
import redis
from crawler.settings import *


#存储模块
class RedisClient(object):
    type = 'accounts'
    website = 'XQ'
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT):

        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def name(self):
        #获取Hash名称
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        #设置键值对
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        #获取键值对
        return self.db.hget(self.name(), username)

    def delete(self, username):
        #删除键值对
        return self.db.hdel(self.name(), username)

    def count(self):
        #获取数目
        return self.db.hlen(self.name())

    def random(self):
        #随机得到键值，用于随机获取Cookie
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        #获取所有账户信息
        return self.db.hkeys(self.name())

    def all(self):
        #获取所有键值对
        return self.db.hgetall(self.name())


#生成模块
#for username in accounts_usernames:
class 
login_url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=token&client_id=100229413&redirect_uri=https://xueqiu.com/service/qqconnect&scope=get_user_info,add_share,add_t'


#检测模块
class ValidTester(object):
    def __init__(self, website='default'):
        pass
