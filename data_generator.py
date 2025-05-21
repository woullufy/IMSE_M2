# RUN pip install mysql-connector-python for docker
import mysql.connector
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="LP-278Tg!",
    database="language_school"
)
cursor = connection.cursor()

cursor.execute("SELECT * FROM student")

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
connection.close()
