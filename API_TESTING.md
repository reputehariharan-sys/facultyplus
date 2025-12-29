"""
API Testing Guide for FacultyPlus
"""

# 1. INSTITUTION ENDPOINTS

# Create Institution
POST /api/institutions/
{
    "institution_name": "XYZ University",
    "institution_code": "XYZ001",
    "institution_email": "admin@xyz.edu",
    "institution_phone": "+91-9876543210",
    "address": "123, University Road, City",
    "status": "active"
}

# Get All Institutions
GET /api/institutions/

# Filter Institutions
GET /api/institutions/?status=active&search=university

# Get Institution Details
GET /api/institutions/1/

# Get Colleges in Institution
GET /api/institutions/1/colleges/

# Get Departments in Institution
GET /api/institutions/1/departments/

# Get Jobs in Institution
GET /api/institutions/1/jobs/


# 2. COLLEGE ENDPOINTS

# Create College
POST /api/colleges/
{
    "college_name": "Engineering College",
    "college_code": "ENG001",
    "institution": 1,
    "status": "active"
}

# Get All Colleges
GET /api/colleges/

# Filter Colleges
GET /api/colleges/?institution=1&status=active

# Get College Details
GET /api/colleges/1/

# Get Departments in College
GET /api/colleges/1/departments/

# Get Jobs in College
GET /api/colleges/1/jobs/


# 3. DEPARTMENT ENDPOINTS

# Create Department
POST /api/departments/
{
    "department_name": "Computer Science",
    "department_code": "CS001",
    "college": 1,
    "institution": 1,
    "status": "active"
}

# Get All Departments
GET /api/departments/

# Filter Departments
GET /api/departments/?college=1&status=active

# Get Department Details
GET /api/departments/1/

# Get Jobs in Department
GET /api/departments/1/jobs/


# 4. JOB ENDPOINTS

# Create Job
POST /api/jobs/
{
    "job_title": "Senior Software Engineer",
    "job_description": "Looking for experienced software engineers...",
    "institution": 1,
    "college": 1,
    "department": 1,
    "job_type": "full_time",
    "experience_required": "5+ years",
    "qualification": "B.Tech in CS",
    "last_date": "2024-12-31",
    "job_status": "open"
}

# Get All Jobs
GET /api/jobs/

# Get Open Jobs
GET /api/jobs/open_jobs/

# Filter Jobs
GET /api/jobs/?job_status=open&job_type=full_time&college=1

# Get Job Details
GET /api/jobs/1/

# Get Applications for Job
GET /api/jobs/1/applications/

# Change Job Status
POST /api/jobs/1/change_status/
{
    "job_status": "closed"
}


# 5. USER ENDPOINTS

# Create User (Institution Admin)
POST /api/users/
{
    "username": "admin1",
    "email": "admin1@example.com",
    "phone": "+91-9876543210",
    "role": "admin",
    "password": "securepass123",
    "institution": 1,
    "status": "active"
}

# Create User (HR)
POST /api/users/
{
    "username": "hr1",
    "email": "hr1@example.com",
    "phone": "+91-9876543210",
    "role": "hr",
    "password": "securepass123",
    "institution": 1,
    "status": "active"
}

# Get All Users
GET /api/users/

# Filter Users by Role
GET /api/users/by_role/?role=hr

# Filter Users
GET /api/users/?role=admin&status=active

# Get User Details
GET /api/users/1/

# Change User Status
POST /api/users/1/change_status/
{
    "status": "inactive"
}


# 6. HR ASSIGNMENT ENDPOINTS

# Create HR Assignment
POST /api/hr-assignments/
{
    "hr_user": 2,
    "institution": 1,
    "college": 1,
    "department": 1,
    "assigned_by": 1
}

# Get All HR Assignments
GET /api/hr-assignments/

# Get HR Assignments by Institution
GET /api/hr-assignments/by_institution/?institution_id=1

# Filter HR Assignments
GET /api/hr-assignments/?institution=1&college=1

# Get Assignment Details
GET /api/hr-assignments/1/


# 7. APPLICANT ENDPOINTS

# Create Applicant
POST /api/applicants/
{
    "full_name": "John Doe",
    "email": "john@example.com",
    "mobile_number": "+91-9876543210",
    "password": "pass123",
    "date_of_birth": "1995-05-15",
    "gender": "male",
    "current_location": "New Delhi",
    "resume_url": "https://example.com/resume.pdf"
}

# Get All Applicants
GET /api/applicants/

# Search Applicants
GET /api/applicants/?search=john&is_active=true

# Get Applicant Details (with education and experience)
GET /api/applicants/1/

# Get Applicant's Applications
GET /api/applicants/1/applications/

# Toggle Applicant Status
POST /api/applicants/1/toggle_status/


# 8. EDUCATION ENDPOINTS

# Add Education
POST /api/education/
{
    "applicant": 1,
    "qualification": "B.Tech",
    "specialization": "Computer Science",
    "institution_name": "IIT Delhi",
    "year_of_passing": 2018,
    "percentage": 8.5
}

# Get All Education Records
GET /api/education/

# Get Education by Applicant
GET /api/education/by_applicant/?applicant_id=1

# Get Education Details
GET /api/education/1/


# 9. EXPERIENCE ENDPOINTS

# Add Experience
POST /api/experience/
{
    "applicant": 1,
    "organization_name": "Google",
    "designation": "Software Engineer",
    "start_date": "2018-06-01",
    "end_date": "2021-12-31",
    "is_current": false
}

# Get All Experience Records
GET /api/experience/

# Get Experience by Applicant
GET /api/experience/by_applicant/?applicant_id=1

# Get Experience Details
GET /api/experience/1/


# 10. APPLICATION ENDPOINTS

# Create Application
POST /api/applications/
{
    "job": 1,
    "applicant": 1,
    "applicant_name": "John Doe",
    "applicant_email": "john@example.com",
    "applicant_phone": "+91-9876543210",
    "resume_url": "https://example.com/resume.pdf"
}

# Get All Applications
GET /api/applications/

# Get Applications by Job
GET /api/applications/by_job/?job_id=1

# Get Applications by Applicant
GET /api/applications/by_applicant/?applicant_id=1

# Filter Applications
GET /api/applications/?status=submitted&job=1

# Get Application Details
GET /api/applications/1/

# Change Application Status
POST /api/applications/1/change_status/
{
    "status": "shortlisted"
}

# Get Application Statistics
GET /api/applications/statistics/


# FILTERING AND SEARCH EXAMPLES

# Filter by multiple fields
GET /api/jobs/?job_status=open&job_type=full_time&college=1&ordering=-created_at

# Search with filter
GET /api/applicants/?search=john&is_active=true&ordering=full_name

# Date range filtering
GET /api/jobs/?last_date__gte=2024-01-01&last_date__lte=2024-12-31

# Pagination
GET /api/institutions/?page=1

# Order results
GET /api/applicants/?ordering=created_at  # ascending
GET /api/applicants/?ordering=-created_at  # descending
