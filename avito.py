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
driver_flats = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                 options=options,capabilities=caps)
driver_flats.get(
    'https://www.avito.ru/taganrog/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&s=104&user=1')

print(5)
driver_houses = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                 options=options,capabilities=caps)
print(6)
driver_houses.get(
    'https://www.avito.ru/taganrog/kvartiry/prodam-ASgBAgICAUSSA8YQ?f=ASgBAQICAUSSA8YQAUCQvg0Ulq41&s=104')
print(7)


async def houses_source():
    driver_houses.refresh()
    return driver_houses.page_source


async def flats_source():
    driver_flats.refresh()
    return driver_flats.page_source


# Инициализируем драйвер браузера
async def parse(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    temp = soup.find('div', {'data-marker': 'item'})
    info = {'id': int(temp.attrs["data-item-id"]),
            'url': 'https://www.avito.ru' + temp.find('a', {'itemprop': 'url'}).attrs['href'],
            'name': temp.find('h3', {'itemprop': 'name'}).text.replace('\xa0', ' '),
            'price': temp.find('span', {'data-marker': 'item-price'}).text.replace('\xa0', ' '),
            'price_per_meter': temp.find('span', {
                "class": 'price-noaccent-X6dOy price-normalizedPrice-PplY9 text-text-LurtD text-size-s-BxGpL'}).text.replace(
                '\xa0', ' '), 'address': temp.find('div', {'data-marker': 'item-address'}).text,
            'time': temp.find('div', {'data-marker': 'item-date'}).text,
            'description': temp.find('div', {'class': 'iva-item-descriptionStep-C0ty1'}).text}

    return info


async def main():
    print(555)
    temp1 = await houses_source()
    temp2 = await flats_source()
    print('g')

    print(await parse(temp1, 5))
    print(await parse(temp2, 5))
    await asyncio.sleep(5)
    await main()


if __name__ == '__main__':
    urls = [f'https://www.avito.ru/taganrog/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&p={i}&s=104' for i in
            range(1, 21)]
    asyncio.run(main())
