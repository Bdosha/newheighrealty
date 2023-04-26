from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio


options = webdriver.FirefoxOptions()
options.add_argument('user-agent=Mozilla 5.0 (X11; Ubuntu)')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.headless = True

driver_houses = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                  options=options)

driver_houses.get(
    'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&sort=creation_date_desc&with_neighbors=0')
driver_flats = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                                 options=options)
driver_flats.get(
    'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&offer_type=flat&p=1&sort=creation_date_desc&with_neighbors=0')


async def houses_source():
    driver_houses.refresh()
    return driver_houses.page_source


async def flats_source():
    driver_flats.refresh()
    return driver_flats.page_source


async def parse(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    temp = soup.find('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
    info = {'id': int(temp.find('a', class_='_93444fe79c--link--eoxce')['href'].split('/')[-2]),
            'url': temp.find('a', class_='_93444fe79c--link--eoxce')['href'],
            'name': temp.find('span', {'data-mark': 'OfferTitle'}).text,
            'price': temp.find('span', {'data-mark': 'MainPrice'}).text.replace('\xa0', ' ')}

    try:
        info['price_per_meter'] = temp.find('p', {'data-mark': 'PriceInfo'}).text.replace('\xa0', ' ')
    except:
        pass
    info['address'] = temp.find('div', class_='_93444fe79c--labels--L8WyJ').text
    info['time'] = temp.find('div', class_='_93444fe79c--absolute--yut0v').text
    info['description'] = temp.find('div', {'data-name': 'Description'}).text


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
    urls = [
        'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&offer_type=flat&p=1&sort=creation_date_desc&with_neighbors=0',
        'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&offer_type=flat&p=2&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=2&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=3&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=4&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=5&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=6&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=7&sort=creation_date_desc&with_neighbors=0',
        f'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&location%5B0%5D=5008&object_type%5B0%5D=1&offer_type=suburban&p=8&sort=creation_date_desc&with_neighbors=0'
    ]
    # Инициализируем драйвер браузера

