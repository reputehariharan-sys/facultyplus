"""
Activity Log serializers for audit trail and logging.
"""
from rest_framework import serializers
from admin_panel.models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for activity logs."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'user_name', 'action', 'action_display',
            'content_type', 'object_id', 'description', 'ip_address',
            'user_agent', 'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'action', 'content_type', 'object_id',
            'description', 'ip_address', 'user_agent', 'created_at'
        ]
