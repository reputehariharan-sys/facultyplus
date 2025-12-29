from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('institution_admin', 'Institution Admin'),
        ('hr', 'HR'),
        ('hod', 'Head of Department'),
        ('applicant', 'Public Applicant'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    # Core User Fields
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='applicant')
    institution = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    assigned_colleges = models.ManyToManyField('College', blank=True, related_name='assigned_hr')
    assigned_departments = models.ManyToManyField('Department', blank=True, related_name='assigned_hr')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_login_ip = models.CharField(max_length=50, blank=True, null=True)
    last_action = models.CharField(max_length=255, blank=True, null=True)
    last_action_time = models.DateTimeField(null=True, blank=True)
    
    # Applicant-specific Fields
    # Basic Information
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    profile_completion_percentage = models.IntegerField(default=0)
    
    # Education Fields
    education_qualification = models.CharField(max_length=255, blank=True, null=True)
    education_specialization = models.CharField(max_length=255, blank=True, null=True)
    education_institution_name = models.CharField(max_length=255, blank=True, null=True)
    education_year_of_passing = models.IntegerField(blank=True, null=True)
    education_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Experience Fields
    experience_organization_name = models.CharField(max_length=255, blank=True, null=True)
    experience_designation = models.CharField(max_length=255, blank=True, null=True)
    experience_start_date = models.DateField(blank=True, null=True)
    experience_end_date = models.DateField(blank=True, null=True)
    experience_is_current = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['role', 'status']),
            models.Index(fields=['institution']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Auto-create token on user creation
        if not hasattr(self, 'auth_token'):
            Token.objects.get_or_create(user=self)
