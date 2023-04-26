from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().FIREFOX
caps["marionette"] = False
options = webdriver.FirefoxOptions()
options.add_argument('user-agent=Mozilla 5.0 (X11; Ubuntu)')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.headless = True
options.page_load_strategy = 'eager'
driver_houses = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                  options=options)
driver_houses.get(
    'https://dom.mirkvartir.ru/listing/?locationIds=MK_Town%7C129113&by=6&types=6&onlyUser=true')
driver_flats = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                 options=options)
driver_flats.get(
    'https://www.mirkvartir.ru/listing/?locationIds=MK_Town%7C129113&by=6&onlyUser=true')


async def houses_source():
    driver_houses.refresh()
    return driver_houses.page_source


async def flats_source():
    driver_flats.refresh()
    return driver_flats.page_source


async def parse(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    temp = soup.find('div', class_='OffersListItem_infoContainer__1xyCn')
    info = {'id': int(temp.find('a', class_='OffersListItem_offerTitle__3GQ_0')['href'].split('/')[-2]),
            'url': temp.find('a', class_='OffersListItem_offerTitle__3GQ_0')['href'],
            'name': temp.find('a', {'class': 'OffersListItem_offerTitle__3GQ_0'}).text,
            'price': temp.find('span', {'class': 'OfferPrice_price__1jdEj'}).text.replace('\u2009', ' ').replace('\xa0',
                                                                                                                 ' '),
            'price_per_meter': temp.find('span', {'class': 'OfferPrice_priceSub__2BKUo'}).text.replace('\u2009',
                                                                                                       ' ').replace(
                '\xa0', ' '), 'address': temp.find('div', class_='OfferAddress_address__2O-MU').text,
            'time': temp.find('div', class_='OffersListItem_pubDate__2t_Yj').text,
            'description': temp.find('div', {'class': 'OffersListItem_infoText__1jjI7'}).text}

    return info


async def main():
    print(555)
    temp1 = await houses_source()
    temp2 = await flats_source()
    print('g')

    print(await parse(temp1))
    print(await parse(temp2))
    await asyncio.sleep(5)
    await main()


if __name__ == '__main__':
    asyncio.run(main())
