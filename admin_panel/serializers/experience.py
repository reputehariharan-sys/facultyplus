from rest_framework import serializers
from admin_panel.models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'applicant', 'organization_name', 'designation', 'start_date',
                  'end_date', 'is_current', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
