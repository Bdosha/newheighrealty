from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio

options = webdriver.FirefoxOptions()
options.add_argument('user-agent=Mozilla 5.0 (X11; Ubuntu)')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
#options.headless = True

driver_houses = webdriver.Firefox(executable_path='root/usr/local/bin/geckodriver',
                                  options=options)
driver_houses.get(
    'https://youla.ru/taganrog/nedvijimost/prodaja-doma?attributes[sort_field]=date_published&attributes[sobstvennik_ili_agent][0]=10705')
driver_flats = webdriver.Firefox(executable_path='root/usr/local/bin/geckodriver',
                                 options=options)
driver_flats.get(
    'https://youla.ru/taganrog/nedvijimost/prodaja-kvartiri?attributes[sort_field]=date_published&attributes[sobstvennik_ili_agent][0]=10705')


async def houses_source():
    driver_houses.refresh()
    await asyncio.sleep(5)
    return driver_houses.page_source


async def flats_source():
    driver_flats.refresh()
    await asyncio.sleep(5)
    return driver_flats.page_source


async def parse(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    temp = soup.find('span', class_='sc-llGDqb sc-gqgnwQ fEAASo hZGRky')

    info = {'id': temp.find('figure', class_='sc-hsZwpi fssEAr')['data-test-id'],
            'url': 'https://youla.ru' + temp.find('a', {'target': '_blank'})['href'],
            'name': temp.find('span', {'class': 'sc-cOxWqc sc-fxvcDT bOrVyP dreCvV'}).text,
            'price': temp.find('span', {'class': 'sc-dXqfbs iMealh'}).text.replace('\u205f', ' ') + ' Р',
            'address': 'Неизвестен', 'time': '', 'image': '', 'description': ''}

    return info


async def main():

    temp1 = await houses_source()
    temp2 = await flats_source()

    print(await parse(temp1, 5))
    print(await parse(temp2, 5))

    await asyncio.sleep(5)
    await main()


if __name__ == '__main__':
    asyncio.run(main())