from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/student_grades'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    search_name = request.args.get('search_name', '')
    filter_status = request.args.get('filter_status', '')

    if request.method == 'POST':
        student_name = request.form['student_name']
        subject_key = request.form['subject_key']
        grade = request.form['grade']

        query = text("INSERT INTO mst_student (student_name, subject_key, grade) VALUES (:student_name, :subject_key, :grade)")
        db.session.execute(query, {"student_name": student_name, "subject_key": subject_key, "grade": grade})
        db.session.commit()
        
        message = "Data committed to the database"

    # Join mst_student and mst_subject to get the subject name along with student data
    if filter_status.lower() in ['pass', 'fail']:
        query = text("""
            SELECT s.student_name, su.subject_name, s.grade, s.remarks
            FROM mst_student s
            JOIN mst_subject su ON s.subject_key = su.subject_key
            WHERE s.remarks = :filter_status
        """)
        students = db.session.execute(query, {"filter_status": filter_status.upper()}).fetchall()
    elif search_name:
        query = text("""
            SELECT s.student_name, su.subject_name, s.grade, s.remarks
            FROM mst_student s
            JOIN mst_subject su ON s.subject_key = su.subject_key
            WHERE s.student_name LIKE :search_name
        """)
        students = db.session.execute(query, {"search_name": f"%{search_name}%"}).fetchall()
    else:
        query = text("""
            SELECT s.student_name, su.subject_name, s.grade, s.remarks
            FROM mst_student s
            JOIN mst_subject su ON s.subject_key = su.subject_key
        """)
        students = db.session.execute(query).fetchall()

    return render_template('index.html', message=message, students=students, search_name=search_name, filter_status=filter_status)

if __name__ == '__main__':
    app.run(debug=True)
