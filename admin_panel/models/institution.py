from django.db import models


class Institution(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    institution_name = models.CharField(max_length=255)
    institution_code = models.CharField(max_length=50, unique=True)
    institution_email = models.EmailField()
    institution_phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='institutions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'
    
    def __str__(self):
        return self.institution_name
