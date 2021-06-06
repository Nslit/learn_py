from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://stepik.org/media/attachments/lesson/209723/3.html").read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')