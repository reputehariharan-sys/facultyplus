# FacultyPlus Setup Guide

## Project Structure

```
facultyplus/
├── facultyplus/              # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings (configured)
│   ├── urls.py              # URL routing (configured)
│   ├── wsgi.py
│   └── asgi.py
├── admin_panel/             # Main app
│   ├── models/              # Data models (modular)
│   │   ├── __init__.py
│   │   ├── user.py          # User with role-based access
│   │   ├── institution.py
│   │   ├── college.py
│   │   ├── department.py
│   │   ├── job.py           # Job with approval workflow
│   │   ├── application.py   # Application with status tracking
│   │   ├── applicant.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   ├── hr_assignment.py
│   │   └── activity_log.py  # Audit trail
│   ├── serializers/         # DRF serializers (modular)
│   │   ├── __init__.py
│   │   ├── user.py          # User serializers with auth
│   │   ├── job.py           # Job serializers with workflow
│   │   ├── application.py   # Application serializers
│   │   ├── activity_log.py  # Activity log serializer
│   │   ├── institution.py
│   │   ├── college.py
│   │   ├── department.py
│   │   ├── applicant.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   └── hr_assignment.py
│   ├── viewsets/            # DRF viewsets (modular)
│   │   ├── __init__.py
│   │   ├── user.py          # User management with roles
│   │   ├── job.py           # Job management with workflow
│   │   ├── application.py   # Application management
│   │   ├── activity_log.py  # Activity log viewset
│   │   ├── institution.py
│   │   ├── college.py
│   │   ├── department.py
│   │   ├── applicant.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   └── hr_assignment.py
│   ├── permissions.py       # Role-based permissions (NEW)
│   ├── auth_views.py        # Authentication views (NEW)
│   ├── management/          # Management commands
│   │   ├── commands/
│   │   │   └── auto_close_expired_jobs.py  # Job deadline auto-close
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── urls.py
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS)
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── manage.py
├── db.sqlite3              # SQLite database
└── API_DOCUMENTATION.md    # Complete API docs (NEW)
```

## Installation Steps

### 1. Install Python & Dependencies

```bash
# Install Python 3.8+
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database

```bash
# Run migrations
python manage.py migrate

# Create super admin user
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: secure_password
```

### 3. Create Initial Data (Optional)

```bash
# Create Institution
python manage.py shell
>>> from admin_panel.models import Institution
>>> Institution.objects.create(
...     name="Tech University",
...     state="Tamil Nadu",
...     address="Chennai"
... )
```

### 4. Run Development Server

```bash
python manage.py runserver
# Server runs at http://localhost:8000
```

## Key Components

### 1. Authentication (Token-Based)

- **Endpoint**: `POST /api/auth/login/`
- **Response**: User data + Token
- **All endpoints** require `Authorization: Token <token>` header (except public endpoints)

```python
# In auth_views.py
class CustomTokenAuthView(TokenAuthentication):
    - Tracks login IP and timestamp
    - Creates token on first login
    - Logs user activity
```

### 2. Role-Based Access Control

**Five Role Hierarchy:**

1. **super_admin** - Full system access
   - Manage all institutions, users, jobs
   - View all activity logs
   - Approve job workflows

2. **institution_admin** - Institution-level access
   - Manage users in institution
   - View jobs in institution
   - View activity logs in institution

3. **hr** - Human Resources
   - Approve and publish jobs
   - Manage applications
   - Change application status
   - View jobs in assigned colleges

4. **hod** - Head of Department
   - Create job postings (draft status)
   - View applications for their jobs
   - Assigned to departments

5. **applicant** - Public users
   - Apply for published jobs
   - View own applications
   - Update own profile

**Permission Classes** (in permissions.py):
- `IsSuperAdmin` - Only Super Admin
- `IsHR` - Only HR users
- `IsHOD` - Only HOD users
- `IsApplicant` - Only Applicant users
- `CanAccessDepartment` - Access control by department
- `CanCreateOrApproveJob` - Job creation/approval rights

### 3. Job Workflow

**Status Flow:**
```
draft (HOD creates)
  ↓
pending_approval (auto when submitted for approval)
  ↓
published (HR approves)
  ↓
closed (when applicant selected OR deadline passed)
```

**Key Features:**
- HOD creates jobs in draft status
- HR approves and publishes
- Auto-close on deadline with management command
- Auto-close when applicant selected
- Soft-delete to archived

**Endpoints:**
```
POST   /api/jobs/                    # Create (HOD)
POST   /api/jobs/{id}/approve_job/   # Approve (HR)
POST   /api/jobs/{id}/mark_selected/ # Mark selected (HR)
GET    /api/jobs/published_jobs/     # View published (public)
GET    /api/jobs/{id}/applications/  # View applications (HR/HOD)
```

### 4. Application Workflow

**Status Flow:**
```
submitted
  ↓
under_review
  ↓
interviewing
  ↓
shortlisted → selected
           ↓
          rejected
```

**Email Notifications:**
- Application submission
- Interview stage notification
- Rejection email
- Selection email
- Tracks which emails have been sent

**Endpoints:**
```
POST   /api/applications/                          # Apply (Applicant)
POST   /api/applications/{id}/update_status/       # Change status (HR)
POST   /api/applications/{id}/mark_selected/       # Mark selected (HR)
POST   /api/applications/{id}/mark_rejected/       # Mark rejected (HR)
GET    /api/applications/my_applications/          # View my applications (Applicant)
GET    /api/applications/by_job/?job_id=1          # View by job (HR/HOD)
```

### 5. Activity Logging

**Logged Actions:**
- User login/logout
- Job creation/approval/closure
- Application status changes
- User management changes
- System auto-actions

**Tracked Data:**
- User who performed action
- Action type (create/update/delete/approve/login/logout/apply)
- Resource affected (using generic FK)
- IP address
- User agent
- Timestamp

**Endpoints:**
```
GET    /api/activity-logs/                 # View all (Super Admin)
GET    /api/activity-logs/my_activities/   # View own activities
GET    /api/activity-logs/user_activities/ # View user's activities (Admin)
```

## Management Commands

### Auto-Close Expired Jobs

Automatically closes jobs when deadline passes:

```bash
# Run once
python manage.py auto_close_expired_jobs

# Run daily via cron job
0 2 * * * cd /path/to/facultyplus && python manage.py auto_close_expired_jobs
```

This command:
- Finds published jobs with passed deadlines
- Closes them automatically
- Logs the action in activity logs
- Maintains data integrity

## Configuration

### Email Backend (Optional)

Add to settings.py for email notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-password'
DEFAULT_FROM_EMAIL = 'noreply@facultyplus.com'
```

### Database Configuration

Default uses SQLite. To use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'facultyplus',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### CORS Configuration

Currently allows localhost. For production:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Testing the System

### 1. Create Super Admin
```bash
python manage.py createsuperuser
```

### 2. Create Users via Admin or API
```bash
POST /api/users/
{
  "username": "hod@college.com",
  "password": "secure123",
  "role": "hod",
  "institution": 1
}
```

### 3. Test Complete Workflow

**HOD Flow:**
```bash
# 1. Login
POST /api/auth/login/
{
  "username": "hod@college.com",
  "password": "secure123"
}

# 2. Create job (goes to draft)
POST /api/jobs/
{
  "job_title": "Professor",
  "college": 1,
  "department": 1,
  "last_date": "2024-12-31"
}

# 3. Check job status → draft
GET /api/jobs/1/
```

**HR Flow:**
```bash
# 1. Login as HR
POST /api/auth/login/
{
  "username": "hr@college.com",
  "password": "secure123"
}

# 2. View pending approvals
GET /api/jobs/pending_approval/

# 3. Approve and publish job
POST /api/jobs/1/approve_job/

# 4. Job now published
GET /api/jobs/1/ → status: published
```

**Applicant Flow:**
```bash
# 1. Register as applicant
POST /api/auth/register/
{
  "username": "student@email.com",
  "password": "secure123",
  "email": "student@email.com"
}

# 2. View published jobs
GET /api/jobs/published_jobs/

# 3. Apply for job
POST /api/applications/
{
  "job": 1,
  "applicant": 5,
  "resume_url": "..."
}

# 4. Check my applications
GET /api/applications/my_applications/
```

**HR Review Applications:**
```bash
# 1. View applications for job
GET /api/jobs/1/applications/

# 2. Update status to under_review
POST /api/applications/1/update_status/
{
  "status": "under_review"
}

# 3. Move to interview
POST /api/applications/1/move_to_interview/

# 4. Mark selected (auto-closes job)
POST /api/applications/1/mark_selected/
# OR
POST /api/jobs/1/mark_selected/
{
  "selected_applicant": 5
}
```

## Admin Interface

Access at: `http://localhost:8000/admin/`

Create new entities and manage data through Django admin:
- Users
- Institutions
- Colleges
- Departments
- Jobs
- Applications
- Activity Logs

## Logging

Logs stored in:
- `logs/facultyplus.log` - General application logs
- `logs/activity.log` - User activity and action logs

View logs:
```bash
tail -f logs/facultyplus.log
tail -f logs/activity.log
```

## Troubleshooting

### No module named 'rest_framework'
```bash
pip install djangorestframework
```

### Missing admin_panel app
Add to INSTALLED_APPS in settings.py:
```python
'admin_panel.apps.AdminPanelConfig',
```

### Token not working
```bash
# Ensure token auth is configured in settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

### Permission denied errors
Check user role and assigned colleges/departments match job location.

## Next Steps

1. **Frontend Integration**: Connect React/Vue frontend to API
2. **Email Notifications**: Configure email backend and send emails on status changes
3. **Cron Jobs**: Set up automated job deadline closure
4. **Monitoring**: Set up logging and error monitoring
5. **Testing**: Write unit and integration tests
6. **Deployment**: Deploy to production server (Heroku, AWS, etc.)

## Support

For issues or questions, refer to:
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Django REST Framework: https://www.django-rest-framework.org/
- Django Documentation: https://docs.djangoproject.com/

---

**Last Updated**: 2024
**Project**: FacultyPlus - Educational Job Management System
