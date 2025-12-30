"""
Management command to auto-close jobs with passed deadlines.
Run with: python manage.py auto_close_expired_jobs
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from admin_panel.models import Job, ActivityLog
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger('admin_panel')


class Command(BaseCommand):
    help = 'Automatically close jobs with passed deadlines'
    
    def handle(self, *args, **options):
        """
        Close all published jobs where deadline has passed
        and no applicant has been selected.
        """
        today = timezone.now().date()
        expired_jobs = Job.objects.filter(
            job_status='published',
            last_date__lt=today,
            selected_applicant__isnull=True
        )
        
        closed_count = 0
        for job in expired_jobs:
            job.auto_close_if_deadline_passed()
            closed_count += 1
            
            # Log this action
            ActivityLog.objects.create(
                user=None,  # System action
                action='update',
                content_type=ContentType.objects.get_for_model(Job),
                object_id=job.id,
                description=f'Auto-closed job due to deadline: {job.job_title}',
                ip_address='0.0.0.0',  # System action
                user_agent='auto_close_expired_jobs_command'
            )
            
            logger.info(f'Auto-closed job {job.id}: {job.job_title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully closed {closed_count} expired jobs'
            )
        )
