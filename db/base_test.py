from mysql.connector import connect, Error


try:
    with connect(
        host="localhost",
        user="root",
        password="root",
        database="my_shop",
    ) as connection:
        show_db_query = "INSERT INTO users(name, pass) values(123455, 8575335)"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            connection.commit()

except Error as e:
    print(e)