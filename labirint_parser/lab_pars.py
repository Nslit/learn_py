from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import sqlite3
from sqlite3 import Error


def sql_query(SQL):  # обработка запроса к бд

    try:
        con = sqlite3.connect('labirint.db')  # создание или подключение к бд
        print("Connection is established")

        cursor = con.cursor()  # создание курсора
        cursor.execute(SQL)  # отправка запроса к бд
        con.commit()  # сохранение результата
        print('SQL query: successful ')

        rows = cursor.fetchall()  # возврат и вывод ответа от бд
        for row in rows:
            print(row)

    except Error:
        print(Error)


def create_search_url(search):  # создание ссылки по запросу
    url = "https://www.labirint.ru/search/" + quote(search) + "/"
    return url


def soup_getter(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def link_parser(url, URL):
    print(f'Начало парсинга страницы: {url}')
    soup = soup_getter(url)
    items = soup.find_all('div', class_='product need-watch')

    for item in items:
        link = 'https://www.labirint.ru' + item.find('a', class_='cover').get('href')
        if int(item.get('data-available-status')):
            book_parser(link)

    if soup.find('a', class_='pagination-next__text'):
        new_url = URL + soup.find('a', class_='pagination-next__text').get('href')
        link_parser(new_url, URL)


def parser(search):
    url = create_search_url(search)
    link_parser(url, url)


def book_parser(link):
    def numbers_in_string(href):
        answer = ''
        for i in href:
            if i.isdigit():
                answer += i
        return answer

    def author_getter(authors):
        if len(authors) >= 1:
            if authors[0].get('data-event-label') == 'author':
                author = authors[0].get_text()
                author_id = int(numbers_in_string(authors[0].get('href')))
                return author, author_id
        return None, None

    def translator_getter(authors):
        if len(authors) >= 2:
            if authors[1].get('data-event-label') == 'translator':
                return authors[1].get_text()
        return None

    def price_getter():
        price = item.find('span', class_='buying-pricenew-val-number')
        if price:
            price = item.find('span', class_='buying-pricenew-val-number').get_text()
        else:
            price = item.find('span', class_='buying-price-val-number').get_text()
        return int(price)

    print(f'Начало парсинга ссылки: {link}')
    soup = soup_getter(link)
    items = soup.find_all('div', id='product-info')

    for item in items:

        book_id = int(item.get('data-product-id'))
        title = item.get('data-name')
        genre = item.get('data-first-genre-name')
        all_authors = item.find_all('a', class_="analytics-click-js")
        author, author_id = author_getter(all_authors)
        translator = translator_getter(all_authors)
        publisher = item.get('data-pubhouse')
        publisher_id = int(numbers_in_string(item.find('div', class_="publisher").find('a').get('href')))
        year = int(numbers_in_string(item.find('div', class_="publisher").get_text()))
        price = price_getter()

        print(book_id, title, genre, author, author_id, translator, publisher, publisher_id, year, price, sep='\n')


parser('Эрих Ремарк')
