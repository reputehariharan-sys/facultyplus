from rest_framework import serializers
from admin_panel.models import Department


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
