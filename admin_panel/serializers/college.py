from rest_framework import serializers
from admin_panel.models import College


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
