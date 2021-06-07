from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import sqlite3
from sqlite3 import Error


def sql_query(SQL):

    try:
        con = sqlite3.connect('labirint.db')
        print("Connection is established")

        cursor = con.cursor()
        cursor.execute(SQL)
        con.commit()
        print('SQL query: successful ')

        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Error:
        print(Error)


def create_search_url(search):
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
            genre = ''
            author = ''
            author_id = int()
            versionist = ''
            publisher = ''
            publisher_id = int()
            year = int()
            price = int()
            print(book_id, title)


def main():
    links = link_parser('Эрих Ремарк')
    book_parser(links)


main()
