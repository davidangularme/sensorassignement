from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource
import os
import statistics

app = Flask(__name__, static_folder='web/build/web')
api = Api(app)

# In-memory data store for the grades
grades = {}

class GradeSubmission(Resource):
    def post(self):
        data = request.get_json()
        student_id = data['student_id']
        subject = data['subject']
        grade = data['grade']
        
        if not (0 <= grade <= 100):
            return {"message": "Grade must be between 0 and 100"}, 400
        
        if student_id not in grades:
            grades[student_id] = {}
        
        grades[student_id][subject] = grade
        return {"message": "Grade submitted successfully"}, 201

class SubjectGrades(Resource):
    def get(self, subject_name):
        subject_grades = [grades[student][subject_name] for student in grades if subject_name in grades[student]]
        
        if not subject_grades:
            return {"message": "No grades found for this subject"}, 404
        
        num_students = len(subject_grades)
        avg_grade = sum(subject_grades) / num_students
        median_grade = statistics.median(subject_grades)
        
        return {
            "subject": subject_name,
            "num_students": num_students,
            "average_grade": avg_grade,
            "median_grade": median_grade
        }, 200

class StudentGrades(Resource):
    def get(self, student_id):
        if student_id not in grades:
            return {"message": "No grades found for this student"}, 404
        
        student_grades = grades[student_id]
        avg_grade = sum(student_grades.values()) / len(student_grades)
        
        return {
            "student_id": student_id,
            "grades": student_grades,
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
    app.run(debug=True, host='127.0.0.1', port=28000)
