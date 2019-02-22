from login.login import CookiesGenerate
from accounts.importer import Import
from cookiespool.scheduler import Scheduler
from cookiespool.tester import XueqiuValidTester

username = '511856180'
password = '123456789'

def main():
    #l = CookiesGenerate(username,password)
    #cookie = l.main()
    #s = Import()
    #s.scan()
    #print('a')
    s = Scheduler()
    s.run()
    #t=XueqiuValidTester()
    #t.run()
    


if __name__ == '__main__':
    main()
