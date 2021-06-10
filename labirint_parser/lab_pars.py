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


def soup_getter(url):  # Создание соупа по url
    html = urlopen(url).read().decode('utf-8')  # Получение html по url
    soup = BeautifulSoup(html, 'html.parser')  # создание соупа из html
    return soup


def link_parser(url, URL):  # Функция для прохода по ссылкам страницы и по следующим страницам, если они есть
    print(f'Начало парсинга страницы: {url}')
    soup = soup_getter(url)  # создание соупа
    items = soup.find_all('div', class_='product need-watch')  # получение списка карточек товара

    for item in items:  # проход по всем карточкам
        link = 'https://www.labirint.ru' + item.find('a', class_='cover').get('href')
        # получение ссылки на товар из карточки
        if int(item.get('data-available-status')):  # проверка на наличие товара
            book_parser(link)  # парсинг товара

    if soup.find('a', class_='pagination-next__text'):  # проверка, есть ли ещё страницы с товаром по запросу
        new_url = URL + soup.find('a', class_='pagination-next__text').get('href')  # генерации новой страницы
        link_parser(new_url, URL)  # рекурсивный вызов этой функции для новой страницы


def parser(search):  # объединение функции создания ссылки по запросу и парсера, главная функция
    url = create_search_url(search)
    link_parser(url, url)


def book_parser(link):
    def numbers_in_string(href):  # Получение цифр из строки
        answer = ''
        for i in href:
            if i.isdigit():
                answer += i
        return answer

    def author_getter(authors):  # поучение автора книги, если он есть
        if len(authors) >= 1:  # проверка на колво авторов, переводчиков и тд
            if authors[0].get('data-event-label') == 'author':  # проверка, есть ли среди авторов автор
                author = authors[0].get_text()  # получение ФИО автора
                author_id = int(numbers_in_string(authors[0].get('href')))  # получение id автора
                return author, author_id
        return None, None

    def translator_getter(authors):  # получени переводчка(аналогично ф-и для автора)
        if len(authors) >= 2:
            if authors[1].get('data-event-label') == 'translator':
                return authors[1].get_text()
        return None

    def price_getter():  # получение цены книги
        price = item.find('span', class_='buying-pricenew-val-number')  # получение тега со скидочной ценой
        if price:
            price = item.find('span', class_='buying-pricenew-val-number').get_text()
            # получения значения цены по скидке, если она есть
        else:
            price = item.find('span', class_='buying-price-val-number').get_text()
            # получение цены без скидки, если нет скидки
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


parser('Эрих Ремарк')  # запук программы
