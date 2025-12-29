from rest_framework import serializers
from admin_panel.models import Education


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'applicant', 'qualification', 'specialization', 'institution_name',
                  'year_of_passing', 'percentage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
