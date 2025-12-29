"""
Activity Log ViewSet for audit trail management.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from admin_panel.models import ActivityLog
from admin_panel.serializers import ActivityLogSerializer
from admin_panel.permissions import IsSuperAdmin


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing activity logs.
    Only Super Admin can view all activity logs.
    """
    queryset = ActivityLog.objects.all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'action', 'created_at']
    search_fields = ['user__username', 'user__email', 'action']
    ordering_fields = ['created_at', 'action']
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activity logs."""
        activities = ActivityLog.objects.filter(user=request.user).order_by('-created_at')
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def user_activities(self, request):
        """Get activity logs for a specific user (Admin only)."""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        activities = ActivityLog.objects.filter(user_id=user_id).order_by('-created_at')
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
