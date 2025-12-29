from django.db import models
from django.utils import timezone


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    JOB_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending HR Approval'),
        ('published', 'Published'),
        ('closed', 'Closed/Filled'),
        ('archived', 'Archived'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Fields
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='jobs')
    college = models.ForeignKey('College', on_delete=models.CASCADE, related_name='jobs')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    
    # Job Details
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_required = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    last_date = models.DateField()
    salary_range = models.CharField(max_length=255, blank=True, null=True)
    
    # Status & Workflow
    job_status = models.CharField(max_length=30, choices=JOB_STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Creator & Approver
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='jobs_created')
    approved_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs_approved')
    
    # Selected Applicant
    selected_applicant = models.ForeignKey('Applicant', on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_jobs')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        indexes = [
            models.Index(fields=['job_status', 'last_date']),
            models.Index(fields=['institution', 'college']),
        ]
    
    def __str__(self):
        return self.job_title
    
    def is_deadline_passed(self):
        """Check if job deadline has passed"""
        return timezone.now().date() > self.last_date
    
    def auto_close_if_deadline_passed(self):
        """Auto-close job if deadline has passed"""
        if self.is_deadline_passed() and self.job_status == 'published':
            self.job_status = 'closed'
            self.closed_at = timezone.now()
            self.save()
            return True
        return False
    
    def close_job_with_selection(self, applicant):
        """Close job when an applicant is selected"""
        self.job_status = 'closed'
        self.selected_applicant = applicant
        self.closed_at = timezone.now()
        self.save()
