import asyncio
import random
import time
from pyppeteer import launch
from cookiespool.config import *

async def main():
    #browser = await launch({'headless' : False, 'args' : ['--no-sandbox', '--window-size=1366,850']})
    browser = await launch({'headless' : False})
    page = await browser.newPage()
    #在非headless模式下调整窗口size
    await page.setViewport({'width' : 1200, 'height' : 800})
    await page.setUserAgent(random.choice(USER_AGENTS))
    await page.goto('https://xueqiu.com')
    await page.click('#app > nav > div.Header_container_2v5 > div.Header_nav__rt_2Om > div > div')
    page.mouse
    await page.click('body > div:nth-child(12) > div.index_dialog_PKc > div > div > div.Loginmodal_modal__login__main_3sO > div.Loginmodal_modal__login__3rd-party_4tM > ul > li:nth-child(3) > a > i')
    page.mouse
    #await page.goto('https://api.weibo.com/oauth2/authorize?client_id=2887826189&redirect_uri=https://xueqiu.com/service/weiboconnect&scope=email')
    
    await page.type('#userId', '18245386342')
    #await page.type('/html/body/label', '263293fg')


    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

