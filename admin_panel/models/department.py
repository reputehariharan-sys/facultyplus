from django.db import models


class Department(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    department_name = models.CharField(max_length=255)
    department_code = models.CharField(max_length=50)
    college = models.ForeignKey('College', on_delete=models.CASCADE, related_name='departments')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='departments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('department_code', 'college')
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return f"{self.department_name} - {self.college.college_name}"
