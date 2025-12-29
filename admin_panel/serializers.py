from rest_framework import serializers
from .models import (
    User, Institution, College, Department, Job,
    HRAssignment, Applicant, Education, Experience, Application
)


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'institution',
                  'assigned_colleges', 'assigned_departments', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'institution', 'password', 'status']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Institution Serializer
class InstitutionSerializer(serializers.ModelSerializer):
    total_colleges = serializers.SerializerMethodField()
    total_departments = serializers.SerializerMethodField()
    total_jobs = serializers.SerializerMethodField()
    
    class Meta:
        model = Institution
        fields = ['id', 'institution_name', 'institution_code', 'institution_email',
                  'institution_phone', 'address', 'status', 'created_by', 'created_at',
                  'updated_at', 'total_colleges', 'total_departments', 'total_jobs']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_colleges(self, obj):
        return obj.colleges.filter(status='active').count()
    
    def get_total_departments(self, obj):
        return obj.departments.filter(status='active').count()
    
    def get_total_jobs(self, obj):
        return obj.jobs.filter(job_status='open').count()


# College Serializer
class CollegeSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source='institution.institution_name', read_only=True)
    total_departments = serializers.SerializerMethodField()
    total_jobs = serializers.SerializerMethodField()
    
    class Meta:
        model = College
        fields = ['id', 'college_name', 'college_code', 'institution', 'institution_name',
                  'status', 'created_by', 'created_at', 'updated_at', 'total_departments', 'total_jobs']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_departments(self, obj):
        return obj.departments.filter(status='active').count()
    
    def get_total_jobs(self, obj):
        return obj.jobs.filter(job_status='open').count()


# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.college_name', read_only=True)
    total_jobs = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_code', 'college', 'institution',
                  'college_name', 'status', 'created_by', 'created_at', 'updated_at', 'total_jobs']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_jobs(self, obj):
        return obj.jobs.filter(job_status='open').count()


# Job Serializer
class JobSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.college_name', read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True, allow_null=True)
    total_applications = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = ['id', 'job_title', 'job_description', 'institution', 'college', 'college_name',
                  'department', 'department_name', 'job_type', 'experience_required',
                  'qualification', 'last_date', 'created_by', 'job_status', 'created_at',
                  'updated_at', 'total_applications']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_applications(self, obj):
        return obj.applications.count()


# HR Assignment Serializer
class HRAssignmentSerializer(serializers.ModelSerializer):
    hr_user_name = serializers.CharField(source='hr_user.username', read_only=True)
    institution_name = serializers.CharField(source='institution.institution_name', read_only=True)
    college_name = serializers.CharField(source='college.college_name', read_only=True, allow_null=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True, allow_null=True)
    
    class Meta:
        model = HRAssignment
        fields = ['id', 'hr_user', 'hr_user_name', 'institution', 'institution_name',
                  'college', 'college_name', 'department', 'department_name',
                  'assigned_by', 'assigned_at', 'updated_at']
        read_only_fields = ['id', 'assigned_at', 'updated_at']


# Education Serializer
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'applicant', 'qualification', 'specialization', 'institution_name',
                  'year_of_passing', 'percentage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# Experience Serializer
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'applicant', 'organization_name', 'designation', 'start_date',
                  'end_date', 'is_current', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# Applicant Serializer
class ApplicantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['id', 'full_name', 'email', 'mobile_number', 'date_of_birth',
                  'gender', 'current_location', 'profile_completion_percentage',
                  'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicantDetailSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Applicant
        fields = ['id', 'full_name', 'email', 'mobile_number', 'date_of_birth',
                  'gender', 'current_location', 'resume_url', 'profile_completion_percentage',
                  'is_active', 'created_at', 'updated_at', 'education', 'experience']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicantCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Applicant
        fields = ['full_name', 'email', 'mobile_number', 'password', 'date_of_birth',
                  'gender', 'current_location', 'resume_url']


# Application Serializer
class ApplicationListSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.job_title', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'applicant', 'applicant_name', 'applicant_email',
                  'applicant_phone', 'status', 'applied_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'applied_date', 'created_at', 'updated_at']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    applicant_details = ApplicantDetailSerializer(source='applicant', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'job', 'job_details', 'applicant', 'applicant_details',
                  'applicant_name', 'applicant_email', 'applicant_phone', 'resume_url',
                  'status', 'applied_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'applied_date', 'created_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'applicant', 'applicant_name', 'applicant_email', 'applicant_phone', 'resume_url']
