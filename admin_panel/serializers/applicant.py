from rest_framework import serializers
from admin_panel.models import Applicant, Education, Experience


class EducationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'applicant', 'qualification', 'specialization', 'institution_name',
                  'year_of_passing', 'percentage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExperienceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'applicant', 'organization_name', 'designation', 'start_date',
                  'end_date', 'is_current', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = [
            'id', 'full_name', 'email', 'mobile_number', 'date_of_birth',
            'gender', 'current_location', 'profile_completion_percentage',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicantDetailSerializer(serializers.ModelSerializer):
    education = EducationDetailSerializer(many=True, read_only=True)
    experience = ExperienceDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Applicant
        fields = [
            'id', 'full_name', 'email', 'mobile_number', 'date_of_birth',
            'gender', 'current_location', 'resume_url', 'profile_completion_percentage',
            'is_active',
            # Education fields
            'education_qualification', 'education_specialization', 'education_institution_name',
            'education_year_of_passing', 'education_percentage',
            # Experience fields
            'experience_organization_name', 'experience_designation', 'experience_start_date',
            'experience_end_date', 'experience_is_current',
            # Relations
            'education', 'experience',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicantCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Applicant
        fields = [
            'full_name', 'email', 'mobile_number', 'password', 'date_of_birth',
            'gender', 'current_location', 'resume_url',
            # Education fields
            'education_qualification', 'education_specialization', 'education_institution_name',
            'education_year_of_passing', 'education_percentage',
            # Experience fields
            'experience_organization_name', 'experience_designation', 'experience_start_date',
            'experience_end_date', 'experience_is_current'
        ]
