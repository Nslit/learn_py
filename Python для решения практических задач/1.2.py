from urllib.request import urlopen
import re

html = urlopen("https://stepik.org/media/attachments/lesson/209719/2.html ").read().decode('utf-8') # создание строки из html кода страницы

pattern = r'<code>(.*?)</code>' # шаблон, который ищет все элементы между <code> </code>
s = re.findall(pattern, html) # поиск слов которые находятся по шаблону
c = set()

for i in s: # поиск всех элементов, которые встречаются больше 1 раза
    if s.count(i) != 1:
        c.add(i)

print(*sorted(list(c))[1:4]) # вывод 3 элементов, которые являются словами