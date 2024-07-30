# Student Grading Service

This is a simple student grading service that exposes a REST API for submitting and retrieving grades.

## Features

- Submit grades for different students in different subjects
- Retrieve grades by subject (including number of students, average grade, and median grade)
- Retrieve grades by student (including grades in all subjects and average grade)

## Requirements

- Python 3.9+
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:


2. Install the required packages:


3. Set up the database:
The application uses SQLAlchemy with SQLite by default. To use a different database, set the `DATABASE_URL` environment variable.

4. Run the application:


The server will start on `http://localhost:28000`.

## API Endpoints

- `POST /grades`: Submit a grade
- Request body: `{ "student_id": "string", "subject": "string", "grade": integer }`
- Response: `{ "message": "Grade submitted successfully" }`

- `GET /grades/subject/<subject_name>`: Retrieve grades for a subject
- Response: `{ "subject": "string", "num_students": integer, "average_grade": float, "median_grade": float }`

- `GET /grades/student/<student_id>`: Retrieve grades for a student
- Response: `{ "student_id": "string", "grades": { "subject": grade }, "average_grade": float }`

## Docker Deployment

1. Build the Docker image:


2. Run the Docker container:


The server will be accessible at `http://localhost:28000`.

## Notes

- The service is designed to be linearly scalable. Multiple instances can be spun up behind a load balancer.
- For production use, consider using a more robust database solution (e.g., PostgreSQL) and implement proper authentication and authorization mechanisms.
