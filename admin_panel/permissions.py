from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from admin_panel.models import User, Institution, College, Department, Job


class IsSuperAdmin(permissions.BasePermission):
    """Only Super Admin can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'super_admin'


class IsInstitutionAdmin(permissions.BasePermission):
    """Only Institution Admin can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'institution_admin'


class IsHR(permissions.BasePermission):
    """Only HR can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'hr'


class IsHOD(permissions.BasePermission):
    """Only HOD can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'hod'


class IsApplicant(permissions.BasePermission):
    """Only Applicants can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'applicant'


class IsSuperAdminOrInstitutionAdmin(permissions.BasePermission):
    """Super Admin or Institution Admin can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['super_admin', 'institution_admin']


class IsHROrHOD(permissions.BasePermission):
    """HR or HOD can access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['hr', 'hod']


class CanAccessInstitution(permissions.BasePermission):
    """
    Super Admin: Can access any institution
    Institution Admin: Can access only their institution
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['super_admin', 'institution_admin', 'hr', 'hod']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role in ['institution_admin', 'hr', 'hod']:
            return request.user.institution == obj if hasattr(obj, 'institution') else request.user.institution_id == obj.id
        return False


class CanAccessCollege(permissions.BasePermission):
    """
    Super Admin: Can access any college
    Institution Admin: Can access colleges in their institution
    HR/HOD: Can access assigned colleges
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['super_admin', 'institution_admin', 'hr', 'hod']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'institution_admin':
            return request.user.institution == obj.institution
        if request.user.role in ['hr', 'hod']:
            return request.user.assigned_colleges.filter(id=obj.id).exists()
        return False


class CanAccessDepartment(permissions.BasePermission):
    """
    Super Admin: Can access any department
    Institution Admin: Can access departments in their institution
    HR/HOD: Can access assigned departments
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['super_admin', 'institution_admin', 'hr', 'hod']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'institution_admin':
            return request.user.institution == obj.institution
        if request.user.role in ['hr', 'hod']:
            return request.user.assigned_departments.filter(id=obj.id).exists() or \
                   request.user.assigned_colleges.filter(id=obj.college_id).exists()
        return False


class CanCreateOrApproveJob(permissions.BasePermission):
    """
    HOD: Can create job postings (draft status)
    HR: Can approve job postings and create/edit published jobs
    Institution Admin: Can approve and manage all jobs
    Super Admin: Can do anything
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['super_admin', 'institution_admin', 'hr', 'hod']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'institution_admin':
            return request.user.institution == obj.institution
        if request.user.role == 'hr':
            # HR can manage jobs in assigned colleges/departments
            if obj.department and request.user.assigned_departments.filter(id=obj.department_id).exists():
                return True
            if request.user.assigned_colleges.filter(id=obj.college_id).exists():
                return True
        if request.user.role == 'hod':
            # HOD can manage jobs they created
            return request.user == obj.created_by
        return False


class CanManageApplications(permissions.BasePermission):
    """
    HR: Can manage applications for jobs they created
    Institution Admin: Can manage all applications in their institution
    Super Admin: Can manage any application
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['super_admin', 'institution_admin', 'hr']
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if request.user.role == 'institution_admin':
            return request.user.institution == obj.job.institution
        if request.user.role == 'hr':
            return request.user == obj.job.created_by or \
                   request.user.assigned_departments.filter(id=obj.job.department_id).exists() or \
                   request.user.assigned_colleges.filter(id=obj.job.college_id).exists()
        return False
