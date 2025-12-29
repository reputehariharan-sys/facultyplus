from rest_framework import serializers
from admin_panel.models import HRAssignment


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
