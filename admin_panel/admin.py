from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Institution, College, Department, Job,
    HRAssignment, Applicant, Education, Experience, Application
)


# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('role', 'institution', 'status')}),
    )
    list_display = ('username', 'email', 'role', 'status', 'is_staff')
    list_filter = ('role', 'status', 'is_staff')


# Institution Admin
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'institution_code', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('institution_name', 'institution_code', 'institution_email')
    ordering = ('-created_at',)


# College Admin
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('college_name', 'college_code', 'institution', 'status', 'created_at')
    list_filter = ('status', 'institution', 'created_at')
    search_fields = ('college_name', 'college_code')
    ordering = ('-created_at',)


# Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'college', 'status', 'created_at')
    list_filter = ('status', 'college', 'created_at')
    search_fields = ('department_name', 'department_code')
    ordering = ('-created_at',)


# Job Admin
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'college', 'job_type', 'job_status', 'last_date', 'created_at')
    list_filter = ('job_status', 'job_type', 'college', 'created_at')
    search_fields = ('job_title', 'job_description')
    ordering = ('-created_at',)


# HR Assignment Admin
@admin.register(HRAssignment)
class HRAssignmentAdmin(admin.ModelAdmin):
    list_display = ('hr_user', 'institution', 'college', 'department', 'assigned_at')
    list_filter = ('institution', 'assigned_at')
    search_fields = ('hr_user__username', 'institution__institution_name')
    ordering = ('-assigned_at',)


# Applicant Admin
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile_number', 'is_active', 'created_at')
    list_filter = ('is_active', 'gender', 'created_at')
    search_fields = ('full_name', 'email', 'mobile_number')
    ordering = ('-created_at',)


# Education Admin
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'qualification', 'institution_name', 'year_of_passing')
    list_filter = ('year_of_passing', 'created_at')
    search_fields = ('applicant__full_name', 'institution_name')
    ordering = ('-year_of_passing',)


# Experience Admin
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'organization_name', 'designation', 'is_current', 'start_date')
    list_filter = ('is_current', 'start_date')
    search_fields = ('applicant__full_name', 'organization_name', 'designation')
    ordering = ('-start_date',)


# Application Admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'status', 'applied_date', 'created_at')
    list_filter = ('status', 'job', 'applied_date')
    search_fields = ('applicant_name', 'applicant_email', 'job__job_title')
    ordering = ('-applied_date',)
