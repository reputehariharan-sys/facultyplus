# FacultyPlus - Django Project

A comprehensive Django REST Framework project for managing faculty recruitment, job postings, and applications across institutions, colleges, and departments.

## Project Structure

```
facultyplus/
├── facultyplus/              # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── admin_panel/              # Main application
│   ├── models.py            # Database models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # ViewSets
│   ├── filters.py           # Filter backends
│   ├── urls.py              # URL routing
│   └── admin.py             # Django admin configuration
├── manage.py
└── requirements.txt
```

## Features

### Admin Panel Module

#### User Management
- Institution Admin
- HR Staff
- HOD (Head of Department)
- Applicants

#### Institution Management
- Create, update, and view institutions
- Track colleges and departments per institution
- Monitor active job postings

#### College Management
- Manage colleges within institutions
- View departments and jobs per college

#### Department Management
- Organize departments within colleges
- Track job openings per department

#### Job Management
- Create and manage job postings
- Track job applications
- Manage job status (Open, Closed, On Hold)

#### HR Assignment
- Assign HR staff to institutions, colleges, or departments
- Track assignment history

#### Applicant Management
- Applicant profile management
- Education history
- Work experience
- Resume management

#### Application Management
- Track job applications
- Application status workflow
- Applicant communication

## Models

### User
- Custom user model with roles (Admin, HR, HOD, Applicant)
- Email authentication
- Status tracking
- Assigned colleges and departments

### Institution
- Institution details
- Code and contact information
- Status management
- Track metrics (colleges, departments, jobs)

### College
- College information
- Linked to institution
- Department tracking
- Job management

### Department
- Department details
- Linked to college and institution
- Job tracking

### Job
- Job posting details
- Job type (Full-time, Part-time, Contract)
- Experience and qualification requirements
- Status management (Open, Closed, On Hold)
- Application tracking

### HRAssignment
- HR staff assignments
- Institutional hierarchy support
- Assignment tracking

### Applicant
- Applicant profile information
- Education and experience details
- Resume management
- Profile completion percentage

### Education
- Educational qualifications
- Linked to applicants
- GPA/percentage tracking

### Experience
- Work experience
- Linked to applicants
- Current position tracking

### Application
- Job applications
- Status workflow (Submitted, Under Review, Shortlisted, Rejected, Accepted)
- Applicant contact details

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd facultyplus
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional - a default one is created automatically)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/by_role/?role=admin` - Filter by role
- `POST /api/users/{id}/change_status/` - Change user status

### Institutions
- `GET /api/institutions/` - List all institutions
- `POST /api/institutions/` - Create institution
- `GET /api/institutions/{id}/` - Get institution details
- `GET /api/institutions/{id}/colleges/` - Get colleges in institution
- `GET /api/institutions/{id}/departments/` - Get departments
- `GET /api/institutions/{id}/jobs/` - Get job postings

### Colleges
- `GET /api/colleges/` - List all colleges
- `POST /api/colleges/` - Create college
- `GET /api/colleges/{id}/departments/` - Get departments in college
- `GET /api/colleges/{id}/jobs/` - Get jobs in college

### Departments
- `GET /api/departments/` - List all departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/jobs/` - Get jobs in department

### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create job posting
- `GET /api/jobs/open_jobs/` - Get open job postings
- `GET /api/jobs/{id}/applications/` - Get applications for job
- `POST /api/jobs/{id}/change_status/` - Change job status

### Applications
- `GET /api/applications/` - List all applications
- `POST /api/applications/` - Create application
- `GET /api/applications/{id}/` - Get application details
- `POST /api/applications/{id}/change_status/` - Change application status
- `GET /api/applications/by_job/?job_id=1` - Get applications by job
- `GET /api/applications/by_applicant/?applicant_id=1` - Get applications by applicant
- `GET /api/applications/statistics/` - Get application statistics

### Applicants
- `GET /api/applicants/` - List all applicants
- `POST /api/applicants/` - Create applicant
- `GET /api/applicants/{id}/` - Get applicant details with education and experience
- `GET /api/applicants/{id}/applications/` - Get applicant's applications
- `POST /api/applicants/{id}/toggle_status/` - Toggle applicant status

## Filtering & Search

All endpoints support:
- **Filtering**: Using `?field=value` parameters
- **Search**: Using `?search=query` for full-text search
- **Ordering**: Using `?ordering=field` to sort results
- **Pagination**: Results are paginated (10 items per page by default)

### Examples
```bash
# Filter users by role
GET /api/users/?role=hr&ordering=created_at

# Search institutions
GET /api/institutions/?search=university&status=active

# Filter jobs by status
GET /api/jobs/?job_status=open&job_type=full_time

# Filter applications by status
GET /api/applications/?status=shortlisted&ordering=-applied_date
```

## Admin Interface

Access the Django admin panel at:
```
http://localhost:8000/admin/
```

Default credentials:
- Username: `admin`
- Password: `admin123`

## Default Superuser

A default superuser is automatically created during migrations:
- Username: `admin`
- Email: `admin@facultyplus.com`
- Password: `admin123`

**Important**: Change the password immediately in production!

## Technology Stack

- **Framework**: Django 4.2.0
- **API**: Django REST Framework 3.14.0
- **Filtering**: django-filter 23.1
- **CORS**: django-cors-headers 4.0.0
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Loading Sample Data
Create a fixture file and load it:
```bash
python manage.py loaddata fixture_name
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please contact the development team.
