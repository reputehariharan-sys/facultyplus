# FacultyPlus Django Project - Setup Guide

## Quick Start Guide

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment support

### 2. Installation Steps

#### Step 1: Navigate to Project Directory
```bash
cd /home/inpathtamilan/facultyplus
```

#### Step 2: Create Virtual Environment
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run Migrations
```bash
python manage.py migrate
```

This will:
- Create the SQLite database (db.sqlite3)
- Create all necessary tables
- Automatically create default superuser (admin/admin123)

#### Step 5: Create Additional Superuser (Optional)
```bash
python manage.py createsuperuser
```

#### Step 6: Start Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

---

## Access Points

### Django Admin Panel
- **URL**: http://localhost:8000/admin/
- **Default Username**: admin
- **Default Password**: admin123

### API Root
- **URL**: http://localhost:8000/api/

### API Endpoints
- Users: http://localhost:8000/api/users/
- Institutions: http://localhost:8000/api/institutions/
- Colleges: http://localhost:8000/api/colleges/
- Departments: http://localhost:8000/api/departments/
- Jobs: http://localhost:8000/api/jobs/
- Applicants: http://localhost:8000/api/applicants/
- Applications: http://localhost:8000/api/applications/
- Education: http://localhost:8000/api/education/
- Experience: http://localhost:8000/api/experience/
- HR Assignments: http://localhost:8000/api/hr-assignments/

---

## Project Structure

```
facultyplus/
│
├── facultyplus/              # Project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
│
├── admin_panel/             # Main application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # App configuration
│   ├── filters.py          # DRF filter classes
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── signals.py          # Django signals
│   ├── urls.py             # App URL routing
│   └── views.py            # ViewSets and API views
│
├── manage.py               # Django management script
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── API_TESTING.md         # API endpoint examples
├── SETUP.md               # This file
└── .gitignore             # Git ignore rules
```

---

## Database Models

### User Model (Custom)
- Fields: username, email, phone, role, institution, status, assigned_colleges, assigned_departments
- Roles: admin (Institution Admin), hr, hod, applicant
- Status: active, inactive

### Institution Model
- Tracks institutions with their details
- Links colleges and departments

### College Model
- Belongs to institution
- Links departments and jobs

### Department Model
- Belongs to college and institution
- Links job postings

### Job Model
- Job postings with detailed information
- Tracks applications received
- Job status: open, closed, on_hold

### HRAssignment Model
- Assigns HR staff to institutions/colleges/departments

### Applicant Model
- Applicant profile information
- Linked to education and experience

### Education Model
- Educational qualifications
- Belongs to applicant

### Experience Model
- Work experience
- Belongs to applicant

### Application Model
- Job applications from applicants
- Status workflow: submitted → under_review → shortlisted/rejected → accepted/rejected

---

## API Usage Examples

### Create Institution
```bash
curl -X POST http://localhost:8000/api/institutions/ \
  -H "Content-Type: application/json" \
  -d '{
    "institution_name": "XYZ University",
    "institution_code": "XYZ001",
    "institution_email": "admin@xyz.edu",
    "institution_phone": "+91-9876543210",
    "address": "123 University Road, City",
    "status": "active"
  }'
```

### List Institutions with Filtering
```bash
curl http://localhost:8000/api/institutions/?status=active&search=university
```

### Create Job
```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Software Engineer",
    "job_description": "Looking for experienced engineers...",
    "institution": 1,
    "college": 1,
    "department": 1,
    "job_type": "full_time",
    "experience_required": "5+ years",
    "qualification": "B.Tech",
    "last_date": "2024-12-31",
    "job_status": "open"
  }'
```

### Create Applicant
```bash
curl -X POST http://localhost:8000/api/applicants/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "mobile_number": "+91-9876543210",
    "date_of_birth": "1995-05-15",
    "gender": "male",
    "current_location": "Delhi",
    "resume_url": "https://example.com/resume.pdf"
  }'
```

### Apply for Job
```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "job": 1,
    "applicant": 1,
    "applicant_name": "John Doe",
    "applicant_email": "john@example.com",
    "applicant_phone": "+91-9876543210"
  }'
```

---

## Features Implemented

### ✅ Models (10 models)
- User (Custom Auth)
- Institution
- College
- Department
- Job
- HRAssignment
- Applicant
- Education
- Experience
- Application

### ✅ ViewSets (10 ViewSets)
- UserViewSet with role-based filtering
- InstitutionViewSet with related data endpoints
- CollegeViewSet with department/job tracking
- DepartmentViewSet with job tracking
- JobViewSet with application tracking and status management
- HRAssignmentViewSet with institutional filtering
- EducationViewSet
- ExperienceViewSet
- ApplicantViewSet with profile management
- ApplicationViewSet with workflow management

### ✅ Serializers
- List and Detail serializers for complex models
- Create serializers for POST requests
- Nested serializers for related data
- Method fields for computed values

### ✅ Filters
- DjangoFilterBackend for filtering
- SearchFilter for full-text search
- OrderingFilter for result sorting
- Date range filtering
- Status filtering

### ✅ Custom Actions
- User role filtering
- Status change endpoints
- Related data endpoints
- Application statistics

### ✅ Admin Interface
- Full Django admin configuration
- List displays with filters
- Search functionality
- Inline editing

---

## Useful Commands

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Revert to previous migration
python manage.py migrate admin_panel 0001_initial
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username
```

### Server Management
```bash
# Run development server on specific port
python manage.py runserver 0.0.0.0:8000

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic
```

### Shell Commands
```bash
# Interactive Django shell
python manage.py shell

# Example queries in shell:
# from admin_panel.models import Institution
# Institution.objects.all()
# Institution.objects.filter(status='active')
# Institution.objects.create(institution_name='Test', ...)
```

---

## Configuration

### Settings File (facultyplus/settings.py)

#### Database
Currently configured for SQLite. To use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'facultyplus_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

Add your frontend URL if needed.

#### REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'PAGE_SIZE': 10,
}
```

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Issue: Database locked error
**Solution**: Delete db.sqlite3 and run migrations again
```bash
rm db.sqlite3
python manage.py migrate
```

### Issue: Port 8000 already in use
**Solution**: Use different port
```bash
python manage.py runserver 8001
```

### Issue: Admin panel not accessible
**Solution**: Ensure migrations are applied
```bash
python manage.py migrate
```

---

## Next Steps

1. **Change Admin Password**: Change from default admin123
2. **Configure Email**: Set up email backend in settings.py
3. **Setup Frontend**: Create React/Vue frontend to consume API
4. **Add Authentication**: Implement JWT tokens
5. **Add Tests**: Write unit tests for models and API
6. **Deploy**: Deploy to production server

---

## Production Deployment Checklist

- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup PostgreSQL or MySQL
- [ ] Configure static files serving
- [ ] Setup email backend
- [ ] Enable HTTPS
- [ ] Setup monitoring and logging
- [ ] Configure backups
- [ ] Setup CI/CD pipeline

---

## Support & Documentation

For more information:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [django-filter Documentation](https://django-filter.readthedocs.io/)

---

## License

This project is provided as-is for educational purposes.
