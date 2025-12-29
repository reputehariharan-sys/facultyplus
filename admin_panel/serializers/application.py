"""
Application serializers for job application management.
"""
from rest_framework import serializers
from admin_panel.models import Application, Job, Applicant


class ApplicationListSerializer(serializers.ModelSerializer):
    """Serializer for listing applications."""
    job_title = serializers.CharField(source='job.job_title', read_only=True)
    applicant_name = serializers.CharField(source='applicant.user.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_changed_by_name = serializers.CharField(source='status_changed_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'applicant', 'applicant_name',
            'status', 'status_display', 'applied_date', 'status_changed_at',
            'status_changed_by', 'status_changed_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'applied_date', 'status_changed_at', 'created_at', 'updated_at']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """Serializer for application details with full information."""
    job_title = serializers.CharField(source='job.job_title', read_only=True)
    job_department = serializers.CharField(source='job.department.name', read_only=True, allow_null=True)
    applicant_name = serializers.CharField(source='applicant.user.get_full_name', read_only=True)
    applicant_email = serializers.CharField(source='applicant.user.email', read_only=True)
    applicant_phone = serializers.CharField(source='applicant.user.phone', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_changed_by_name = serializers.CharField(source='status_changed_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'job_department', 'applicant', 'applicant_name',
            'applicant_email', 'applicant_phone', 'resume_url',
            'status', 'status_display', 'remarks', 'applied_date', 'status_changed_at',
            'status_changed_by', 'status_changed_by_name',
            'submission_email_sent', 'interview_email_sent', 'rejection_email_sent', 'selection_email_sent',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'applied_date', 'status_changed_at', 'status_changed_by',
            'submission_email_sent', 'interview_email_sent', 'rejection_email_sent',
            'selection_email_sent', 'created_at', 'updated_at'
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications."""
    
    class Meta:
        model = Application
        fields = ['job', 'applicant', 'resume_url']


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating application status."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'status', 'status_display', 'remarks']
        read_only_fields = ['id', 'status_display']
