from login.login_weibo_selenium import CookiesGenerate
from accounts.importer import Import
from cookiespool.scheduler import Scheduler
from cookiespool.tester import XueqiuValidTester

#username = '18245386342'
#password = '263293fg'
username = '15945394312'
password = '984542ho'
username = '15846741530'
password = '729063bm'

def main():
    l = CookiesGenerate(username,password)
    cookie = l.main()

    s = Scheduler()
    s.run()
    


if __name__ == '__main__':
    main()
