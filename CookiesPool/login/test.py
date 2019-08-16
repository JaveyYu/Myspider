import asyncio
import time

from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from urllib.parse import urlparse

URLS = [
    'https://www.trustarc.com/'
]

start = time.time()

async def main():
    browser = await launch({'headless' : False})
    page = await browser.newPage()
    try:
        #await page.setRequestInterception(True)
        #page.on('request', callback)
        await page.goto('https://www.trustarc.com/', {'waitUntil': 'networkidle0'})
        if not await page.J('.truste_overlay'):
            await page.click('#teconsent > a')
        cookies_frame = page.frames[1]
        await page.close()
    except TimeoutError as e:
        print(f'Timeout for: {url}')

asyncio.get_event_loop().run_until_complete(main())

    

a = 2
try:
    b = a + 'c'
except:
    b = a+2

