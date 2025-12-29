from django.db import models


class Experience(models.Model):
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE, related_name='experience')
    organization_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'
    
    def __str__(self):
        return f"{self.applicant.full_name} - {self.designation}"
