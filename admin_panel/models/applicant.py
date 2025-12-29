from django.db import models


class Applicant(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255, blank=True, null=True)
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
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
    
    def __str__(self):
        return self.full_name
