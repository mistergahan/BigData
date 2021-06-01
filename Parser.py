#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv

#https://auto.ru/moskva/cars/gaz/all/
#URL = 'https://auto.ru/moskva/cars/mercedes/all/'
#http://www.online-decoder.com/ru
HEADERS = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15', 'Accept': '*/*'}
FILE = 'cars.csv'


def get_html(url, params=None):
   r = requests.get(url, headers=HEADERS, params=params)
   return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a',class_='Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_conent(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ListingItem-module__main')

    car = []
    for item in items:
        km = item.find('div', class_='ListingItem-module__kmAge')
        if km:
            km = km.get_text().replace('√В¬†', '')
            "km = km.get_text().replace('√В¬†√Р¬Ї√Р¬Љ', '')"
        car.append({
            'link': item.find('a', class_='Link ListingItemTitle-module__link').get('href'),
            'title': item.find('a', class_='Link ListingItemTitle-module__link').get_text(strip=True),
            'year': item.find('div', class_='ListingItem-module__year').get_text(strip=True),
            'km': item.find('div', class_='ListingItem-module__kmAge').get_text(strip=True),
            #'price': item.find('div', class_='ListingItemPrice-module__content').get_text(strip=True),
            #'pricee': item.find('div', 'span').get_text(strip=True),

        })

    return car


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Car Name', 'Link', 'Year', 'KMage'])
        for item in items:
            writer.writerow([item['title'], item['link'],  item['year'], item['km']])


def parse():
    URL = input('ВВЕДИТЕ URL: ')
    URL = URL.strip()
    html = get_html(URL)
    print('CallBack:', html.status_code)
    if html.status_code == 200:
        car = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы: {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            car.extend(get_conent(html.text))
        save_file(car, FILE)
        print(f'Получено {len(car)} авто')
    else:
        print('ERROR')


parse()