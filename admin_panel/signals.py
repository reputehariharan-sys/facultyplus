from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """Create a default superuser if none exists"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@facultyplus.com',
            password='admin123',
            role='admin'
        )
