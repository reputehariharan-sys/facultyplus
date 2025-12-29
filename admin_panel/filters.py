import django_filters
from .models import (
    User, Institution, College, Department, Job,
    HRAssignment, Applicant, Application
)


# User Filter (including applicant fields)
class UserFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    role = django_filters.CharFilter(lookup_expr='iexact')
    gender = django_filters.CharFilter(lookup_expr='iexact')
    created_at = django_filters.DateFromToRangeFilter()
    date_of_birth = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = User
        fields = ['status', 'role', 'institution', 'gender', 'created_at', 'date_of_birth']


# Institution Filter
class InstitutionFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Institution
        fields = ['status', 'created_at']


# College Filter
class CollegeFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    institution = django_filters.CharFilter(lookup_expr='iexact')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = College
        fields = ['status', 'institution', 'created_at']


# Department Filter
class DepartmentFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    college = django_filters.CharFilter(lookup_expr='iexact')
    institution = django_filters.CharFilter(lookup_expr='iexact')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Department
        fields = ['status', 'college', 'institution', 'created_at']


# Job Filter
class JobFilter(django_filters.FilterSet):
    job_status = django_filters.CharFilter(lookup_expr='iexact')
    job_type = django_filters.CharFilter(lookup_expr='iexact')
    institution = django_filters.CharFilter(lookup_expr='iexact')
    college = django_filters.CharFilter(lookup_expr='iexact')
    department = django_filters.CharFilter(lookup_expr='iexact')
    last_date = django_filters.DateFromToRangeFilter()
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Job
        fields = ['job_status', 'job_type', 'institution', 'college', 'department', 'last_date', 'created_at']


# HR Assignment Filter
class HRAssignmentFilter(django_filters.FilterSet):
    institution = django_filters.CharFilter(lookup_expr='iexact')
    college = django_filters.CharFilter(lookup_expr='iexact')
    department = django_filters.CharFilter(lookup_expr='iexact')
    assigned_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = HRAssignment
        fields = ['institution', 'college', 'department', 'assigned_at']


# Applicant Filter
class ApplicantFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter()
    gender = django_filters.CharFilter(lookup_expr='iexact')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Applicant
        fields = ['is_active', 'gender', 'created_at']


# Application Filter
class ApplicationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    job = django_filters.CharFilter(lookup_expr='iexact')
    applicant = django_filters.CharFilter(lookup_expr='iexact')
    applied_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Application
        fields = ['status', 'job', 'applicant', 'applied_date']
