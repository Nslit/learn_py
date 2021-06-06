import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

inquiry = "эрих ремарк"
URL = "https://www.labirint.ru/search/" + quote(inquiry) + "/?stype=0"


def get_html(url, params=None):
    r = requests.get(url)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product need-watch watched')
    print(items)
    books = []
    for item in items:
        books.append({
            'title': item.find('span', class_='product-title')
        })
    print(books)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
