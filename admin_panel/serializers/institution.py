from rest_framework import serializers
from admin_panel.models import Institution


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
