import requests
from bs4 import BeautifulSoup as BS4
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}


def get_html(url):
    # print(f'url - {url}')
    r = requests.get(url, headers=HEADERS)
    soup = BS4(r.text, 'lxml')

    return soup


# Собираем ссылкина все брэнды
def find_all_hrefs_brend():
    url = 'https://aromabaza.ru/collection/brend'

    soup = get_html(url)
    conts = soup.find('div', class_='categories-subcollections').find('div', class_='row').find_all('a',
                                                                                                    class_='category-inner')

    ALL_brends = {}
    number = 1
    for cont in conts:
        data_brend = {}

        name_brend = cont.find("div", class_="category-caption").text.strip()
        href_brend = f'https://aromabaza.ru{cont.get("href")}'

        data_brend = {
            'name': name_brend,
            'href': href_brend
        }

        ALL_brends[number] = data_brend

        number += 1

    return ALL_brends


# Создаем сообщение со всеми брендами
def create_mes_all_brebds(ALL_brends):
    MES = 'Ключ: Бренд\n\n'

    for brend in ALL_brends:
        MES += f"{brend} - {ALL_brends[brend]['name']}\n"

    MES += '0: ВСЕ КАТЕГОРИИ (ПРЕДУПРЕЖДЕНИЕ: Достаточно долго)\n'

    return MES


# Собираем все данные по выбранным категориям
def find_all_info(kategorii, ALL_brends, now_time, NF):
    namefile = f'{NF}_{now_time}'
    # print(ALL_brends)

    for kategoriya in kategorii:
        brend = ALL_brends[int(kategoriya)]['name']
        href = ALL_brends[int(kategoriya)]['href']

        print(f'{brend} - {href}')

        soup = get_html(href)

        try:
            conts = soup.find('div', class_='categories-subcollections').find('div', class_='row').find_all('a', class_='category-inner')
            print(len(conts))
        except:
            conts_2 = soup.find('div', class_='products-list is-collection row').find_all('div',
                                                                                                class_='product-card')

            try:
                pagin = soup.find('ul', class_='pagination').find_all('li')
            except:
                if 'В данном разделе пока нет товаров. Мы работаем над этим.' == soup.find('div',
                                                                                                 class_='products-list is-collection row').text.strip():
                    # print(soup_cat_2.find('div', class_='products-list is-collection row').text.strip())
                    continue
                else:
                    pagin = []

            if len(pagin) != 0:
                pagin = int(pagin[-2].text.strip())
                find_all_info_one_page(conts_2, ALL_brends[int(kategoriya)]['name'], '', namefile)
                for i in range(2, pagin + 1):
                    soup_t = get_html(f'{href}?page=2')
                    conts_t = soup_t.find('div', class_='products-list is-collection row').find_all('div',
                                                                                                    class_='product-card')

                    find_all_info_one_page(conts_t, ALL_brends[int(kategoriya)]['name'], '', namefile)

            else:
                # Собираем информаию с одной страницы
                find_all_info_one_page(conts_2, ALL_brends[int(kategoriya)]['name'], '', namefile)
                pagin = 0

            '''
            Собрать все ссылки на товар и записать
            '''

            print(f'LEN_CONT - {len(conts_2)} = LEN_PAGIN - {pagin}')
            continue


        for cont in conts:
            name_cat_2 = cont.find('div', class_='category-caption').text.strip()
            href_cat_2 = f"https://aromabaza.ru{cont.get('href')}"
            print(f'{name_cat_2} - {href_cat_2}')

            soup_cat_2 = get_html(href_cat_2)

            conts_2 = soup_cat_2.find('div', class_='products-list is-collection row').find_all('div', class_='product-card')

            try:
                pagin = soup_cat_2.find('ul', class_='pagination').find_all('li')
            except:
                if 'В данном разделе пока нет товаров. Мы работаем над этим.' == soup_cat_2.find('div', class_='products-list is-collection row').text.strip():
                    # print(soup_cat_2.find('div', class_='products-list is-collection row').text.strip())
                    continue
                else:
                    pagin = []

            if len(pagin) != 0:
                pagin = int(pagin[-2].text.strip())
                find_all_info_one_page(conts_2, ALL_brends[int(kategoriya)]['name'], name_cat_2, namefile)
                for i in range(2, pagin+1):
                    soup_t = get_html(f'{href_cat_2}?page=2')
                    conts_t = soup_t.find('div', class_='products-list is-collection row').find_all('div', class_='product-card')

                    find_all_info_one_page(conts_t, ALL_brends[int(kategoriya)]['name'], name_cat_2, namefile)

            else:
                # Собираем информаию с одной страницы
                find_all_info_one_page(conts_2, ALL_brends[int(kategoriya)]['name'], name_cat_2, namefile)
                pagin = 0



            '''
            Собрать все ссылки на товар и записать
            '''

            print(f'LEN_CONT - {len(conts_2)} = LEN_PAGIN - {pagin}')

        print()
        print('='*50)
        print()
        # for cont in conts:


# Собираем информаию с одной страницы
def find_all_info_one_page(conts, brend, cat_2, namefile):
    DATA = []

    for cont in conts:
        href = f"https://aromabaza.ru{cont.find('a', class_='product-link').get('href')}"

        soup = get_html(href)

        name = soup.find('h1', class_='page-headding').text.strip()
        description = soup.find('div', class_='product-introtext on-page editor').text.strip()

        prices = soup.find('div', class_='product-prices on-page')#.text.strip()
        old_price = prices.find('div', class_='old-price').text.strip().split('\xa0')[0]
        new_price = prices.find('div', class_='price').text.strip().split('\xa0')[0]
        # old_price = ''
        # new_price = ''

        IMG = soup.find('a', class_='image-wrapper').get('href')
        data = {
            'brend': brend.replace('é', 'e'),
            'cat_2': cat_2.replace('é', 'e'),
            'name': name.replace('é', 'e'),
            'description': description.replace('é', 'e'),
            'old_price': old_price.replace('.', ','),
            'new_price': new_price.replace('.', ','),
            'IMG': IMG,
            'href': href,
        }

        # print(data)
        # print()

        DATA.append(data)

    with open(f'{namefile}.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for d in DATA:
            writer.writerow(
                [
                    d['brend'], d['cat_2'], d['name'], d['old_price'],
                    d['new_price'], d['description'], d['IMG'], d['href']
                ])

def save_head(now_time, name):
    with open(f'{name}_{now_time}.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Категория 1', 'Категория 2', 'Наименование', 'Старая Цена',
             'Цена', 'Описание', 'Изображения', 'Ссылка на товар'])






