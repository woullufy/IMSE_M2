from flask import Flask, render_template, request, redirect
import mysql.connector
import uuid

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="flaskuser",
        password="flaskpass",
        database="language_school"
    )

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT s.*, m.mentor_id FROM student s LEFT JOIN mentor m ON s.mentor = m.mentor_id")
    students = cursor.fetchall()

    cursor.execute("SELECT mentor_id FROM mentor")
    mentors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students, mentors=mentors)


@app.route('/add', methods=['POST'])
def add_student():
    student_id = str(uuid.uuid4())
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    age = int(request.form['age'])
    mentor_id = request.form.get('mentor') or None


    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO student (student_id, first_name, last_name, email, age, mentor) VALUES (%s, %s, %s, %s, %s, %s)",
        (student_id, first_name, last_name, email, age, mentor_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
