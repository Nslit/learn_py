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


sql_query('SELECT * FROM books')
