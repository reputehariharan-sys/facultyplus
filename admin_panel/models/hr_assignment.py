from django.db import models


class HRAssignment(models.Model):
    hr_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='hr_assignments')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='hr_assignments')
    college = models.ForeignKey('College', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='hr_assignments_assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-assigned_at']
        unique_together = ('hr_user', 'institution')
        verbose_name = 'HR Assignment'
        verbose_name_plural = 'HR Assignments'
    
    def __str__(self):
        return f"{self.hr_user.username} - {self.institution.institution_name}"
