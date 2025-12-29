# FacultyPlus - Quick Reference Guide

## Architecture Overview

```
Client (React/Vue/Angular)
        ↓
REST API (Django REST Framework)
        ↓
ViewSets (api/views.py)
        ↓
Serializers (api/serializers.py)
        ↓
Models (api/models.py)
        ↓
Database (SQLite/PostgreSQL)
```

## Request/Response Flow

### Example: Creating a Job

1. **Client sends POST request**
   ```
   POST /api/jobs/
   Content-Type: application/json
   
   {
     "job_title": "Senior Engineer",
     "job_description": "...",
     "institution": 1,
     "college": 1,
     ...
   }
   ```

2. **JobViewSet.create() is called**
   - Validates incoming data

3. **JobSerializer validates data**
   - Checks all required fields
   - Validates field types and constraints

4. **Model saves to database**
   - Job record is created

5. **Server returns response**
   ```
   {
     "id": 1,
     "job_title": "Senior Engineer",
     "total_applications": 0,
     ...
   }
   ```

---

## Key Components

### 1. Models
Define database structure and relationships

```python
class Job(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    institution = models.ForeignKey(Institution, ...)
    # ...relationships and fields
```

### 2. Serializers
Convert models to/from JSON

```python
class JobSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.college_name', read_only=True)
    
    class Meta:
        model = Job
        fields = ['id', 'job_title', 'college_name', ...]
```

### 3. ViewSets
Handle API logic and endpoints

```python
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = JobFilter
```

### 4. Filters
Define filtering and search logic

```python
class JobFilter(django_filters.FilterSet):
    job_status = django_filters.CharFilter()
    job_type = django_filters.CharFilter()
    
    class Meta:
        model = Job
        fields = ['job_status', 'job_type', ...]
```

### 5. URLs/Routers
Map URLs to ViewSets

```python
router = DefaultRouter()
router.register(r'jobs', JobViewSet)
urlpatterns = [path('api/', include(router.urls))]
```

---

## Common Operations

### Create Record
```bash
POST /api/jobs/
{
  "job_title": "Engineer",
  "institution": 1,
  ...
}
```

### List Records
```bash
GET /api/jobs/
GET /api/jobs/?page=1  # Pagination
```

### Filter Records
```bash
GET /api/jobs/?job_status=open&job_type=full_time
GET /api/jobs/?search=engineer  # Search
GET /api/jobs/?ordering=created_at  # Sort
```

### Get Single Record
```bash
GET /api/jobs/1/
```

### Update Record
```bash
PUT /api/jobs/1/
{
  "job_title": "Senior Engineer",
  ...
}
```

### Partial Update
```bash
PATCH /api/jobs/1/
{
  "job_title": "Senior Engineer"
}
```

### Delete Record
```bash
DELETE /api/jobs/1/
```

### Custom Action
```bash
GET /api/jobs/open_jobs/  # List only open jobs
POST /api/jobs/1/change_status/  # Change job status
```

---

## Model Relationships

### One-to-Many
```
Institution (1) ─── (Many) College
         ↓
    institution = ForeignKey(Institution)
```

### Many-to-Many
```
User (Many) ─── (Many) College
     ↓
assigned_colleges = ManyToManyField(College)
```

### Related Names
```python
class College(models.Model):
    institution = ForeignKey(Institution, related_name='colleges')

# Access related colleges
institution.colleges.all()
```

---

## Filtering Syntax

### Exact Match
```
?status=active
?id=1
```

### Case-Insensitive
```
?status__iexact=ACTIVE
```

### Greater Than / Less Than
```
?id__gt=5
?id__lt=10
```

### Contains
```
?name__icontains=john
```

### Date Range
```
?created_at__gte=2024-01-01
?created_at__lte=2024-12-31
```

### In List
```
?id__in=1,2,3
```

---

## Pagination

Default: 10 items per page

```
GET /api/jobs/?page=1      # First 10 items
GET /api/jobs/?page=2      # Next 10 items
```

Response includes:
```json
{
  "count": 100,
  "next": "http://api/jobs/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Search Fields

Each ViewSet has defined search_fields:

### Users
```
GET /api/users/?search=john
# Searches: username, email, phone
```

### Jobs
```
GET /api/jobs/?search=engineer
# Searches: job_title, job_description
```

### Institutions
```
GET /api/institutions/?search=university
# Searches: institution_name, institution_code, institution_email
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - New resource created |
| 204 | No Content - Success, no response body |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Not authenticated |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error |

---

## Authentication

Currently uses Token Authentication. To add to requests:

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/users/
```

To get token:
```bash
POST /api/api-token-auth/
{
  "username": "admin",
  "password": "admin123"
}
```

---

## Django Admin

### Access
http://localhost:8000/admin/

### Add Record
1. Click model name
2. Click "Add" button
3. Fill form
4. Click "Save"

### Edit Record
1. Click model name
2. Click record in list
3. Modify fields
4. Click "Save"

### Delete Record
1. Click model name
2. Select checkbox(es)
3. Select "Delete selected"
4. Confirm deletion

### Bulk Actions
1. Select multiple records
2. Choose action from dropdown
3. Click "Go"

---

## Common Queries in Django Shell

```python
python manage.py shell

# Import models
from admin_panel.models import *

# Get all records
Institution.objects.all()

# Filter records
Institution.objects.filter(status='active')

# Get single record
Institution.objects.get(id=1)

# Count records
Institution.objects.count()

# Create record
Institution.objects.create(
    institution_name='XYZ University',
    institution_code='XYZ001',
    ...
)

# Update record
inst = Institution.objects.get(id=1)
inst.status = 'inactive'
inst.save()

# Delete record
Institution.objects.get(id=1).delete()

# Complex queries
Job.objects.filter(
    job_status='open',
    job_type='full_time',
    institution_id=1
).count()

# Related queries
institution = Institution.objects.get(id=1)
institution.colleges.all()
institution.jobs.all()

# Aggregation
from django.db.models import Count
Institution.objects.annotate(
    college_count=Count('colleges')
)
```

---

## Debugging Tips

### 1. Check Server Logs
Watch terminal where `runserver` is running for error messages

### 2. Use Django Debug Toolbar
Add django-debug-toolbar to settings.py for detailed SQL queries

### 3. Check Database
```bash
sqlite3 db.sqlite3
.tables                    # List all tables
SELECT * FROM admin_panel_institution;  # Query table
```

### 4. Test API Directly
```bash
# Using curl
curl -X GET http://localhost:8000/api/jobs/

# Using Postman - Import requests from API_TESTING.md

# Using Python requests
python
import requests
response = requests.get('http://localhost:8000/api/jobs/')
print(response.json())
```

---

## Performance Tips

1. **Use pagination** - Don't fetch all records
2. **Filter data** - Reduce result set size
3. **Use select_related** - For ForeignKey relationships
4. **Use prefetch_related** - For reverse relations
5. **Add indexes** - On frequently searched fields
6. **Cache results** - For expensive queries

---

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Use HTTPS in production
- [ ] Configure ALLOWED_HOSTS
- [ ] Set secure passwords
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Validate all inputs
- [ ] Use parameterized queries
- [ ] Keep dependencies updated

---

## Useful Links

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/ (browsable API)
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/

---

## Tips for Development

1. **Use Postman/Insomnia** - Test API endpoints
2. **Enable verbose logging** - See query details
3. **Use transactions** - For data consistency
4. **Write tests** - For each endpoint
5. **Document code** - Use docstrings
6. **Follow PEP 8** - Code style guide
7. **Use git** - Version control

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| 404 Error | Check URL spelling and routing |
| 400 Bad Request | Validate JSON and required fields |
| Database locked | Restart server, remove db lock |
| Migration errors | Check migration files and dependencies |
| Import errors | Install missing dependencies |
| CORS errors | Configure CORS_ALLOWED_ORIGINS |
| Static files not loading | Run `collectstatic` |

---

End of Quick Reference Guide
