from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime


inquiry = 'эрих ремарк'
url = "https://www.labirint.ru/search/" + quote(inquiry) + "/?stype=0&page=4"
html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

items = soup.find_all('div', class_='product need-watch')
if soup.find('a', class_='pagination-next__text'):
    new_link = soup.find('a', class_='pagination-next__text').get('href')
    print(new_link)
else:
    print('последняя страница')
books = []
for item in items:
    books.append({
        'book_id': item.get('data-product-id'),
        'pubhouse': item.get('data-pubhouse'),
        'title': item.find('span', class_='product-title').get_text(),
        'price': item.find('span', class_='price-val').get_text(strip=True)[:-1],
        'link': 'https://www.labirint.ru' + item.find('a', class_='cover').get('href')

    })
print(*books, sep='\n')
