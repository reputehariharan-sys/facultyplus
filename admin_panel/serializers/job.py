"""
Job serializers for job posting management.
"""
from rest_framework import serializers
from admin_panel.models import Job, Application


class JobListSerializer(serializers.ModelSerializer):
    """Serializer for listing jobs."""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    college_name = serializers.CharField(source='college.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    job_status_display = serializers.CharField(source='get_job_status_display', read_only=True)
    total_applications = serializers.SerializerMethodField()
    is_deadline_passed = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'job_title', 'job_description', 'institution', 'college', 'college_name',
            'department', 'department_name', 'job_type', 'experience_required',
            'qualification', 'salary_range', 'last_date',
            'created_by', 'created_by_name', 'job_status', 'job_status_display',
            'priority', 'approved_by', 'published_at', 'closed_at',
            'total_applications', 'is_deadline_passed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'approved_by', 'published_at', 'closed_at']
    
    def get_total_applications(self, obj):
        return obj.applications.count()
    
    def get_is_deadline_passed(self, obj):
        return obj.is_deadline_passed()


class JobDetailSerializer(serializers.ModelSerializer):
    """Serializer for job details with full information."""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    college_name = serializers.CharField(source='college.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    selected_applicant_name = serializers.CharField(source='selected_applicant.get_full_name', read_only=True, allow_null=True)
    job_status_display = serializers.CharField(source='get_job_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    total_applications = serializers.SerializerMethodField()
    is_deadline_passed = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'job_title', 'job_description', 'institution', 'college', 'college_name',
            'department', 'department_name', 'job_type', 'experience_required',
            'qualification', 'salary_range', 'last_date',
            'created_by', 'created_by_name', 'created_by_email',
            'job_status', 'job_status_display', 'priority', 'priority_display',
            'approved_by', 'approved_by_name', 'selected_applicant', 'selected_applicant_name',
            'published_at', 'closed_at', 'total_applications', 'is_deadline_passed',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'approved_by',
            'published_at', 'closed_at', 'selected_applicant'
        ]
    
    def get_total_applications(self, obj):
        return obj.applications.count()
    
    def get_is_deadline_passed(self, obj):
        return obj.is_deadline_passed()


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating jobs."""
    
    class Meta:
        model = Job
        fields = [
            'job_title', 'job_description', 'college', 'department',
            'job_type', 'experience_required', 'qualification',
            'salary_range', 'last_date', 'priority'
        ]


class JobApprovalSerializer(serializers.ModelSerializer):
    """Serializer for job approval action."""
    
    class Meta:
        model = Job
        fields = ['id', 'job_status']
        read_only_fields = ['id']


class JobSelectionSerializer(serializers.ModelSerializer):
    """Serializer for marking applicant as selected."""
    
    class Meta:
        model = Job
        fields = ['id', 'selected_applicant']
        read_only_fields = ['id']
