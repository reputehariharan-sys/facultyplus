from django.db import models


class Education(models.Model):
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE, related_name='education')
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    institution_name = models.CharField(max_length=255)
    year_of_passing = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year_of_passing']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'
    
    def __str__(self):
        return f"{self.applicant.full_name} - {self.qualification}"
