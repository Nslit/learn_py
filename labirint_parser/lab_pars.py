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


def link_getter(url, URL):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    items = soup.find_all('div', class_='product need-watch')

    for item in items:
        link = 'https://www.labirint.ru' + item.find('a', class_='cover').get('href')
        if int(item.get('data-available-status')) and link not in links:
            links.append(link)

    if soup.find('a', class_='pagination-next__text'):
        new_url = URL + soup.find('a', class_='pagination-next__text').get('href')
        links += link_getter(new_url, URL)

    return links


def link_parser(search):
    url = create_search_url(search)
    links = link_getter(url, url)
    print(len(links))
    return links


def id_in_href(href):
    answer = ''
    for i in href:
        if i.isdigit():
            answer += i
    return answer


def book_parser(links):
    print('Начало парсинга')
    for url in links:
        print(f'ссылка {url}')
        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', id='product-info')
        for item in items:
            book_id = int(item.get('data-product-id'))
            title = item.get('data-name')
            genre = item.get('data-first-genre-name')
            authors = item.find_all('a', class_="analytics-click-js")
            if len(authors) >= 1:
                if authors[0].get('data-event-label') == 'author':
                    author = authors[0].get_text()
                    author_id = int(id_in_href(authors[0].get('href')))
                else:
                    author = None
                    author_id = None
            else:
                author = None
                author_id = None
            if len(authors) >= 2:
                if authors[1].get('data-event-label') == 'translator':
                    translator = authors[1].get_text()
                else:
                    translator = None
            else:
                translator = None
            publisher = item.get('data-pubhouse')
            publisher_id = int(id_in_href(item.find('div', class_="publisher").find('a').get('href')))
            year = int(id_in_href(item.find('div', class_="publisher").get_text()))
            price = item.find('span', class_='buying-pricenew-val-number')
            if price:
                price = item.find('span', class_='buying-pricenew-val-number').get_text()
            else:
                price = item.find('span', class_='buying-price-val-number').get_text()
            price = int(price)
            print(book_id, title, genre, author, author_id, translator, publisher, publisher_id, year, price, sep='\n')



def main():
    links = link_parser('Пушкин и Павловск')
    book_parser(links)


main()
