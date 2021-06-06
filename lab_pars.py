from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote


def create_search_url(search):
    url = "https://www.labirint.ru/search/" + quote(search) + "/"
    return url


def link_getter(url, URL):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    items = soup.find_all('div', class_='product need-watch')

    for item in items:
        links.append('https://www.labirint.ru' + item.find('a', class_='cover').get('href'))

    if soup.find('a', class_='pagination-next__text'):
        new_url = URL + soup.find('a', class_='pagination-next__text').get('href')
        links += link_getter(new_url, URL)

    return links


def link_parser(search):
    url = create_search_url(search)
    links = link_getter(url, url)
    return  links


def good_parser(links):
    print('Начало парсинга')
    for url in links:
        print(f'ссылка {url}')
        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', id='product-info')
        for item in items:
            print(item.get('data-name'))


def main():
    links = link_parser('Эрих Ремарк')
    good_parser(links)


main()
