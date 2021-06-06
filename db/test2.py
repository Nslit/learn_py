from mysql.connector import connect

connection = connect(host="localhost", user="root", password="root", database="my_shop",)  # создания объекта бд
# sql_code = "INSERT INTO users(name, pass) values(5523455, 85753545)"  # sql команда

cursor = connection.cursor()
# cursor.execute(sql_code)  # отправление sql кода на сервер бд
# connection.commit()  # сохранение действий

sql_code = "SELECT name, pass FROM users"

cursor.execute(sql_code)
result = cursor.fetchall()
for row in result:
    print(row)