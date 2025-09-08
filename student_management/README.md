## Installation & Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. PostgreSQL Setup
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE student_management_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE student_management_db TO your_username;
\q
```

### 3. Django Setup
```bash
# Run migrations to create tables
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 4. Access the Application
- Main application: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Features Implemented

### ✅ Student Management
- Add, view, edit, delete students
- Name and email validation
- Search functionality
- Pagination

### ✅ Course Management  
- Add, view, edit, delete courses
- Credit validation (1-6)
- Search functionality
- Enrollment tracking

### ✅ Enrollment Management
- Enroll students in courses
- Update grades
- Remove enrollments
- Prevent duplicate enrollments
- Filter by student, course, grade

### ✅ Reporting
- Dashboard with statistics
- Student transcript with GPA
- Popular courses report
- Grade distribution

### ✅ Additional Features
- Input validation and error handling
- Responsive design
- Success/error messages
- Automatic database table creation
- Admin interface integration
- Search and pagination
- Data integrity constraints

## Database Schema
The application automatically creates these tables:
- **Students**: id, name, email, created_at, updated_at
- **Courses**: id, title, credits, created_at, updated_at  
- **Enrollments**: id, student_id, course_id, grade, enrollment_date, updated_at

All tables include proper foreign key relationships and constraints.