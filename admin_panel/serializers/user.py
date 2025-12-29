"""
User serializers for authentication and user management.
"""
from rest_framework import serializers
from admin_panel.models import User
from django.contrib.auth.password_validation import validate_password


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users."""
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'role', 'role_display', 'institution', 'institution_name',
            'status', 'status_display', 'gender', 'gender_display',
            'current_location', 'date_of_birth', 'resume_url',
            'profile_completion_percentage', 'last_login', 'date_joined'
        ]
        read_only_fields = ['id', 'last_login', 'date_joined']


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user details with nested relationships and applicant fields."""
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    assigned_colleges = serializers.StringRelatedField(many=True, read_only=True)
    assigned_departments = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'role', 'role_display', 'institution', 'institution_name',
            'assigned_colleges', 'assigned_departments',
            'status', 'status_display', 'last_login', 'last_login_ip',
            'last_action', 'date_joined',
            # Applicant fields
            'date_of_birth', 'gender', 'gender_display', 'current_location',
            'resume_url', 'profile_completion_percentage',
            # Education fields
            'education_qualification', 'education_specialization', 'education_institution_name',
            'education_year_of_passing', 'education_percentage',
            # Experience fields
            'experience_organization_name', 'experience_designation', 'experience_start_date',
            'experience_end_date', 'experience_is_current'
        ]
        read_only_fields = ['id', 'last_login', 'last_login_ip', 'last_action', 'date_joined']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating users with applicant fields."""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        min_length=8
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'phone', 'role', 'institution', 'status',
            # Applicant fields
            'date_of_birth', 'gender', 'gender_display', 'current_location', 'resume_url',
            'profile_completion_percentage',
            # Education fields
            'education_qualification', 'education_specialization', 'education_institution_name',
            'education_year_of_passing', 'education_percentage',
            # Experience fields
            'experience_organization_name', 'experience_designation', 'experience_start_date',
            'experience_end_date', 'experience_is_current'
        ]
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match.'}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile with applicant fields."""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'role', 'role_display', 'status', 'status_display', 'last_login',
            # Applicant fields
            'date_of_birth', 'gender', 'gender_display', 'current_location', 'resume_url',
            'profile_completion_percentage',
            # Education fields
            'education_qualification', 'education_specialization', 'education_institution_name',
            'education_year_of_passing', 'education_percentage',
            # Experience fields
            'experience_organization_name', 'experience_designation', 'experience_start_date',
            'experience_end_date', 'experience_is_current'
        ]
        read_only_fields = ['id', 'username', 'last_login']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        min_length=8
    )
    new_password_confirm = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError(
                {'new_password': 'Password fields didn\'t match.'}
            )
        return attrs
