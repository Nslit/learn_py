# Использование BeautifulSoup, просуммировать все числа в таблице
# В теге <td><\td> находится любой другой тег, в котором число
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://stepik.org/media/attachments/lesson/209723/4.html").read().decode('utf-8')
# загрузка html страницы
soup = BeautifulSoup(html, 'html.parser')  # создание из html soup объекта
total = 0
for tag in soup.find_all('td'):  # проход по списку всех тегов <td>
    total += int(tag.get_text())  # tdg.get_text() возвращает только текст из тега

print(total)
