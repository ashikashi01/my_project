from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

app = Flask(__name__)

# Update with your PostgreSQL connection details
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql+psycopg2://root:dkjywi5DHoxReWEK7I3Lvxy8U3YMrpNH@'
    'dpg-cr422njtq21c73dsjp00-a:5432/students_ocbf'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Subject(db.Model):
    __tablename__ = 'mst_subject'

    subject_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(100), nullable=False)

class Student(db.Model):
    __tablename__ = 'mst_student'

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(100), nullable=False)
    subject_key = db.Column(db.Integer, db.ForeignKey('mst_subject.subject_key'), nullable=False)
    grade = db.Column(db.String(1), nullable=False)
    remarks = db.Column(db.String(10))

    subject = db.relationship('Subject', backref='students')

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
    app.run(debug=False, host='0.0.0.0')
