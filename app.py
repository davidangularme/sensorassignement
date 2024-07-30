from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os
import statistics
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, static_folder='web/build/web')
api = Api(app)

# Configure SQLAlchemy for database persistence
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///grades.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Grade model for database
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint('student_id', 'subject', name='uix_student_subject'),)

class GradeSubmission(Resource):
    def post(self):
        data = request.get_json()
        student_id = data['student_id']
        subject = data['subject']
        grade = data['grade']
        
        if not (0 <= grade <= 100):
            return {"message": "Grade must be between 0 and 100"}, 400
        
        try:
            # Use SQLAlchemy to insert or update the grade
            grade_entry = Grade.query.filter_by(student_id=student_id, subject=subject).first()
            if grade_entry:
                grade_entry.grade = grade
            else:
                grade_entry = Grade(student_id=student_id, subject=subject, grade=grade)
                db.session.add(grade_entry)
            db.session.commit()
            return {"message": "Grade submitted successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Error submitting grade"}, 500

class SubjectGrades(Resource):
    def get(self, subject_name):
        # Query the database for grades in the given subject
        subject_grades = Grade.query.filter_by(subject=subject_name).all()
        
        if not subject_grades:
            return {"message": "No grades found for this subject"}, 404
        
        grades_list = [grade.grade for grade in subject_grades]
        num_students = len(grades_list)
        avg_grade = sum(grades_list) / num_students
        median_grade = statistics.median(grades_list)
        
        return {
            "subject": subject_name,
            "num_students": num_students,
            "average_grade": avg_grade,
            "median_grade": median_grade
        }, 200

class StudentGrades(Resource):
    def get(self, student_id):
        # Query the database for grades of the given student
        student_grades = Grade.query.filter_by(student_id=student_id).all()
        
        if not student_grades:
            return {"message": "No grades found for this student"}, 404
        
        grades_dict = {grade.subject: grade.grade for grade in student_grades}
        avg_grade = sum(grades_dict.values()) / len(grades_dict)
        
        return {
            "student_id": student_id,
            "grades": grades_dict,
            "average_grade": avg_grade
        }, 200

# API Endpoints
api.add_resource(GradeSubmission, '/grades')
api.add_resource(SubjectGrades, '/grades/subject/<string:subject_name>')
api.add_resource(StudentGrades, '/grades/student/<string:student_id>')

# Serve Flutter Web App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 28000)))
