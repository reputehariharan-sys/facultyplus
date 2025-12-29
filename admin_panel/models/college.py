from django.db import models


class College(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    college_name = models.CharField(max_length=255)
    college_code = models.CharField(max_length=50)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='colleges')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('college_code', 'institution')
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
    
    def __str__(self):
        return f"{self.college_name} - {self.institution.institution_name}"
