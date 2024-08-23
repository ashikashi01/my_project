from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql+psycopg2://root:dkjywi5DHoxReWEK7I3Lvxy8U3YMrpNH@'
    'dpg-cr422njtq21c73dsjp00-a:5432/students_ocbf'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

if __name__ == '__main__':
    app.run(debug=True)
