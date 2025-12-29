# FacultyPlus API Documentation

## Overview
FacultyPlus is a comprehensive job management system for educational institutions with role-based access control, token authentication, and activity logging.

## Architecture

### Role Hierarchy
1. **Super Admin** - Manages entire system
2. **Institution Admin** - Manages single institution
3. **HR** - Manages job approvals and applications in assigned colleges
4. **HOD** - Creates job postings in assigned departments
5. **Applicant** - Public users who apply for jobs

## Authentication

### Token-Based Authentication
All API endpoints (except registration) require Token authentication.

**Login Endpoint:**
```
POST /api/auth/login/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "token": "your_token_here",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "email": "user@example.com",
    "role": "hod",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Include Token in All Requests:**
```
Authorization: Token your_token_here
```

### User Registration (Applicant)
```
POST /api/auth/register/
Content-Type: application/json

{
  "username": "applicant@example.com",
  "email": "applicant@example.com",
  "password": "securepassword",
  "password_confirm": "securepassword",
  "first_name": "Jane",
  "last_name": "Applicant",
  "phone": "+91-9876543210"
}

Response:
{
  "id": 100,
  "token": "token_here",
  "user": { ... }
}
```

### Other Auth Endpoints
```
GET  /api/auth/profile/        - Get current user profile
POST /api/auth/logout/         - Logout user
POST /api/auth/change-password/ - Change password
```

## Job Management Workflow

### Job Status Flow
```
draft → pending_approval → published → closed
         ↓
       archived (soft delete)
```

### Creating a Job (HOD)
```
POST /api/jobs/
Content-Type: application/json
Authorization: Token <token>

{
  "job_title": "Assistant Professor",
  "job_description": "Looking for an experienced professor...",
  "college": 1,
  "department": 1,
  "job_type": "full_time",
  "experience_required": 5,
  "qualification": "M.Tech/M.Sc",
  "salary_from": 50000,
  "salary_to": 70000,
  "last_date": "2024-12-31",
  "priority": "high"
}

Response:
{
  "id": 1,
  "job_title": "Assistant Professor",
  "job_status": "draft",  // Initially in draft status
  "created_by": 5,
  "created_at": "2024-01-15T10:00:00Z",
  ...
}
```

### Approving a Job (HR)
```
POST /api/jobs/1/approve_job/
Authorization: Token <hr_token>

Response:
{
  "id": 1,
  "job_status": "published",
  "approved_by": 3,
  "published_at": "2024-01-16T10:00:00Z"
}
```

### Public Job Listing
```
GET /api/jobs/published_jobs/
// No authentication required, returns only published jobs

GET /api/jobs/  
// With auth: Returns jobs based on user role
// Without auth: Returns only published jobs
```

## Application Management

### Apply for Job (Public Applicant)
```
POST /api/applications/
Content-Type: application/json
Authorization: Token <applicant_token>

{
  "job": 1,
  "applicant": 5,
  "resume_url": "https://example.com/resume.pdf"
}

Response:
{
  "id": 1,
  "job": 1,
  "applicant": 5,
  "status": "submitted",  // Initial status
  "applied_date": "2024-01-17T10:00:00Z"
}
```

### Application Status Workflow
```
submitted → under_review → interviewing → shortlisted → selected
                                                      → rejected
```

### Changing Application Status (HR)
```
POST /api/applications/1/update_status/
Content-Type: application/json
Authorization: Token <hr_token>

{
  "status": "under_review",
  "remarks": "Excellent profile"
}

Response: Updated application
```

### Quick Status Update Actions (HR)
```
POST /api/applications/1/move_to_interview/
POST /api/applications/1/mark_shortlisted/
POST /api/applications/1/mark_selected/
POST /api/applications/1/mark_rejected/
  "remarks": "Not meeting requirements"
```

### Mark Applicant as Selected (Auto-closes Job)
```
POST /api/jobs/1/mark_selected/
Authorization: Token <hr_token>

{
  "selected_applicant": 5
}

Response:
{
  "job_status": "closed",
  "selected_applicant": 5,
  "closed_at": "2024-01-20T10:00:00Z"
}
```

### View Applications for a Job (HR/HOD)
```
GET /api/jobs/1/applications/
Authorization: Token <token>

Response: List of applications for job 1
```

### View My Applications (Applicant)
```
GET /api/applications/my_applications/
Authorization: Token <applicant_token>

Response: List of applicant's applications
```

## User Management

### Get Users by Role (Admin)
```
GET /api/users/by_role/?role=hod
Authorization: Token <admin_token>

Response: List of all HODs
```

### Get Current User Profile
```
GET /api/users/me/
Authorization: Token <token>

Response: Current user details
```

### Change User Status (Super Admin)
```
POST /api/users/1/change_status/
Authorization: Token <super_admin_token>

{
  "status": "inactive"
}
```

## Activity Logging

All significant actions are logged for audit trail:
- User login/logout
- Job creation/approval
- Application status changes
- User management changes
- File downloads

### View Activity Logs (Super Admin)
```
GET /api/activity-logs/
Authorization: Token <super_admin_token>

Query Parameters:
- user=<user_id>
- action=login|logout|create|update|approve
- created_at=<date>

Response: List of activity logs with user, action, timestamp, IP address
```

### View My Activities
```
GET /api/activity-logs/my_activities/
Authorization: Token <token>

Response: Current user's activity logs
```

## Permission Classes

### IsSuperAdmin
- Only Super Admin can access

### IsInstitutionAdmin
- Super Admin or Institution Admin

### IsHR
- Only HR users

### IsHOD
- Only HOD users

### IsApplicant
- Only Applicant users

### CanCreateOrApproveJob
- HOD can create, HR/Admin can approve

### CanManageApplications
- HR/HOD can manage applications

### CanAccessDepartment
- Only users with access to that department

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "detail": "Field X is required"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Key Features

### Auto Job Closure
- Jobs automatically close when deadline passes (scheduled task)
- Jobs close when an applicant is selected
- Both trigger automatic status update to 'closed'

### Soft Delete
- Jobs and applications are archived, not hard deleted
- Maintains audit trail and data integrity

### Email Notifications
- Application submission confirmation
- Interview stage notification
- Rejection/Selection emails
- Configurable per application

### Activity Tracking
- All user actions logged
- IP address tracking
- User agent logging
- Timestamp tracking

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create super admin
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Admin Interface
Access Django admin at `/admin/` with super admin credentials.

## Configuration

### Email Backend (settings.py)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Logging
Logs are stored in:
- `logs/facultyplus.log` - General logs
- `logs/activity.log` - Activity logs

## Testing the API

### Using cURL
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "hod@example.com", "password": "password"}'

# Create job (HOD)
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token" \
  -d '{"job_title": "Prof", ...}'
```

### Using Postman
1. Set up Bearer Token auth with your token
2. Import API endpoints
3. Test workflow: Create Job → Approve → Apply → Update Status

## Support & Documentation
For more details, refer to individual endpoint documentation or contact the development team.
