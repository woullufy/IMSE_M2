# RUN pip install mysql-connector-python for docker
import mysql.connector
from mysql.connector import Error
from faker import Faker
# need to be installed in docker
from random import randint


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="LP-278Tg!",
            database="language_school"
        )
        print("Successful connection to database!")
        return conn
    except Error as e:
        print(f"The error '{e}' occurred")
    return None


def delete_data(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM group_membership")
        cursor.execute("DELETE FROM checked_assignments")
        cursor.execute("DELETE FROM assignment")
        cursor.execute("DELETE FROM student_group")
        cursor.execute("DELETE FROM course")
        cursor.execute("DELETE FROM student")
        cursor.execute("DELETE FROM tutor")
        cursor.execute("DELETE FROM mentor")
        cursor.execute("DELETE FROM employee")

        conn.commit()
        print("All data deleted from tables.")

    except Error as e:
        print(f"Error deleting data: {e}")

    finally:
        cursor.close()


def generate_data_tutor(x):
    faker = Faker()
    data = {}
    for i in range(0, x):
        data[i] = {}
        data[i]['id'] = i
        data[i]['first_name'] = faker.first_name()
        data[i]['second_name'] = faker.last_name()
        data[i]['language_speciality'] = faker.language_name()
        data[i]['years_of_experience'] = randint(0, 40)
    return data


def generate_data_student(x):
    faker = Faker()
    data = {}
    for i in range(0, x):
        data[i] = {}
        data[i]['id'] = i
        data[i]['first_name'] = faker.first_name()
        data[i]['second_name'] = faker.last_name()
        data[i]['email'] = faker.email()
        data[i]['age'] = randint(10, 60)
        # data[i]['mentor'] = randint()
    return data


def insert_data_tutor(conn, generated_data):
    cursor = conn.cursor()
    for employee in generated_data.values():
        employee_id = employee['id']
        first_name = employee['first_name']
        second_name = employee['second_name']

        query_employee = "INSERT INTO employee (employee_id, first_name, last_name) VALUES (%s, %s, %s)"
        cursor.execute(query_employee, (employee_id, first_name, second_name))

        language_speciality = employee['language_speciality']
        years_of_experience = employee['years_of_experience']

        query_tutor = "INSERT INTO tutor (tutor_id, language_speciality, years_of_experience) VALUES (%s, %s, %s)"
        cursor.execute(query_tutor, (employee_id, language_speciality, years_of_experience))

    conn.commit()
    cursor.close()
    print(f"Inserted {len(generated_data)} records into tutor and employee.")


def insert_data_student(conn, generated_data):
    cursor = conn.cursor()
    for student in generated_data.values():
        student_id = student['id']
        first_name = student['first_name']
        second_name = student['second_name']
        email = student['email']
        age = student['age']

        query = "INSERT INTO student (student_id, first_name, last_name, email, age) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (student_id, first_name, second_name, email, age))

    conn.commit()
    cursor.close()
    print(f"Inserted {len(generated_data)} records into student.")


# def insert_sample_data(conn, table_name, generated_data):
#     cursor = conn.cursor()
#     cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
#     schema = cursor.fetchall()
#     columns = [column[0] for column in schema]
#
#     columns_str = ', '.join(columns)
#     placeholders = ', '.join(['%s'] * len(columns))
#     query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
#
#     for record in generated_data.values():
#         values = tuple(record[col] for col in columns)
#         cursor.execute(query, values)
#
#     conn.commit()
#     cursor.close()
#     print(f"Inserted {len(generated_data)} records into {table_name}.")


connection = create_connection()
delete_data(connection)
tutor_data = generate_data_tutor(20)
student_data = generate_data_student(20)
insert_data_tutor(connection, tutor_data)
insert_data_student(connection, student_data)
# cursor.execute("SELECT * FROM student")
#
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# cursor.close()
connection.close()
