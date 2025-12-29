# FacultyPlus - Modular Structure

## New Project Structure (Models, Serializers, ViewSets Separated)

```
admin_panel/
│
├── models/                          # Separate model files
│   ├── __init__.py
│   ├── user.py                     # User model
│   ├── institution.py              # Institution model
│   ├── college.py                  # College model
│   ├── department.py               # Department model
│   ├── job.py                      # Job model
│   ├── hr_assignment.py            # HRAssignment model
│   ├── applicant.py                # Applicant model (with education & experience fields)
│   ├── education.py                # Education model
│   ├── experience.py               # Experience model
│   └── application.py              # Application model
│
├── serializers/                     # Separate serializer files
│   ├── __init__.py
│   ├── user.py                     # User serializers
│   ├── institution.py              # Institution serializers
│   ├── college.py                  # College serializers
│   ├── department.py               # Department serializers
│   ├── job.py                      # Job serializers
│   ├── hr_assignment.py            # HRAssignment serializers
│   ├── applicant.py                # Applicant serializers (with education & experience)
│   ├── education.py                # Education serializers
│   ├── experience.py               # Experience serializers
│   ├── application.py              # Application serializers
│   └── __init__.py
│
├── viewsets/                        # Separate viewset files (in progress)
│   ├── __init__.py
│   ├── user.py                     # User viewsets
│   ├── institution.py              # Institution viewsets (coming)
│   ├── college.py                  # College viewsets (coming)
│   ├── department.py               # Department viewsets (coming)
│   ├── job.py                      # Job viewsets (coming)
│   ├── hr_assignment.py            # HRAssignment viewsets (coming)
│   ├── applicant.py                # Applicant viewsets (coming)
│   ├── education.py                # Education viewsets (coming)
│   ├── experience.py               # Experience viewsets (coming)
│   └── application.py              # Application viewsets (coming)
│
├── __init__.py
├── admin.py                        # Django admin
├── apps.py                         # App config
├── filters.py                      # Filter classes
├── signals.py                      # Django signals
└── urls.py                         # URL routing
```

## Applicant Model Update

The Applicant model now includes:

### Basic Fields
- full_name
- email
- mobile_number
- password
- date_of_birth
- gender
- current_location
- resume_url
- profile_completion_percentage
- is_active

### Education Fields (from Education model)
- education_qualification
- education_specialization
- education_institution_name
- education_year_of_passing
- education_percentage

### Experience Fields (from Experience model)
- experience_organization_name
- experience_designation
- experience_start_date
- experience_end_date
- experience_is_current

### Relations
- Still has related Education table via foreign key (for multiple education records)
- Still has related Experience table via foreign key (for multiple experience records)

## Benefits

✅ Education and Experience remain as separate tables for detailed history
✅ Applicant also stores the primary/current education & experience data
✅ Can query Education and Experience separately for multiple records
✅ Can access education/experience directly from Applicant model
✅ Clean, modular code structure
✅ Each model/serializer/viewset in its own file for better maintainability

---

**Continue with:**

Next, I'll create remaining viewset files:
- InstitutionViewSet
- CollegeViewSet
- DepartmentViewSet
- JobViewSet
- HRAssignmentViewSet
- ApplicantViewSet
- EducationViewSet
- ExperienceViewSet
- ApplicationViewSet

Would you like me to continue with the remaining viewsets?
