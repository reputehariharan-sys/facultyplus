from django.db import models
from django.utils import timezone


class Application(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('interviewing', 'Interviewing'),
        ('shortlisted', 'Shortlisted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    applicant_phone = models.CharField(max_length=15)
    resume_url = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    
    # Status Workflow
    status = models.CharField(max_length=30, choices=APPLICATION_STATUS_CHOICES, default='submitted')
    status_changed_at = models.DateTimeField(null=True, blank=True)
    status_changed_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='status_changes')
    
    # Remarks/Feedback
    remarks = models.TextField(blank=True, null=True)
    
    # Timestamps
    applied_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Email notification tracking
    submission_email_sent = models.BooleanField(default=False)
    interview_email_sent = models.BooleanField(default=False)
    rejection_email_sent = models.BooleanField(default=False)
    selection_email_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ('job', 'applicant')
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', 'status']),
            models.Index(fields=['status', 'applied_date']),
        ]
    
    def __str__(self):
        return f"{self.applicant_name} - {self.job.job_title}"
    
    def update_status(self, new_status, changed_by=None, remarks=''):
        """Update application status and log the change"""
        if new_status not in dict(self.APPLICATION_STATUS_CHOICES):
            raise ValueError(f"Invalid status: {new_status}")
        
        self.status = new_status
        self.status_changed_at = timezone.now()
        self.status_changed_by = changed_by
        if remarks:
            self.remarks = remarks
        self.save()
    
    def move_to_under_review(self, changed_by=None):
        """Move application to Under Review"""
        self.update_status('under_review', changed_by)
    
    def move_to_interviewing(self, changed_by=None):
        """Move application to Interviewing"""
        self.update_status('interviewing', changed_by)
    
    def move_to_shortlisted(self, changed_by=None):
        """Move application to Shortlisted"""
        self.update_status('shortlisted', changed_by)
    
    def mark_selected(self, changed_by=None):
        """Mark application as selected and close the job"""
        self.update_status('selected', changed_by)
        # Auto-close the job
        self.job.close_job_with_selection(self.applicant)
    
    def mark_rejected(self, changed_by=None, remarks=''):
        """Mark application as rejected"""
        self.update_status('rejected', changed_by, remarks)

