"""
User ViewSet for user management with role-based access control.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from admin_panel.models import User, ActivityLog
from admin_panel.serializers import (
    UserListSerializer, UserDetailSerializer, UserCreateUpdateSerializer,
    UserProfileSerializer
)
from admin_panel.permissions import IsSuperAdmin, IsInstitutionAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management with role-based permissions.
    - Super Admin: Can manage all users
    - Institution Admin: Can manage users in their institution
    - Regular users: Can only view/edit their own profile
    """
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'status', 'institution', 'gender']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'current_location']
    ordering_fields = ['date_joined', 'username', 'last_login']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateUpdateSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action in ['update', 'partial_update']:
            return UserCreateUpdateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserDetailSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter users based on user role."""
        user = self.request.user
        queryset = User.objects.all().order_by('-date_joined')
        
        if not user.is_authenticated:
            return queryset.none()
        
        if user.role == 'super_admin':
            return queryset
        elif user.role == 'institution_admin':
            return queryset.filter(institution=user.institution)
        else:
            # Regular users can only see themselves
            return queryset.filter(id=user.id)
    
    def perform_create(self, serializer):
        """Create a new user."""
        user = serializer.save()
        ActivityLog.objects.create(
            user=user,
            action='create',
            content_type_id=40,  # User content type
            object_id=user.id,
            description=f'User account created: {user.username}',
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
    
    def get_client_ip(self):
        """Get client IP address from request."""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_role(self, request):
        """Get users filtered by role (Admin only)."""
        if request.user.role not in ['super_admin', 'institution_admin']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        role = request.query_params.get('role')
        if not role:
            return Response(
                {'error': 'role parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        users = self.get_queryset().filter(role=role)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsSuperAdmin])
    def change_status(self, request, pk=None):
        """Change user status (Super Admin only)."""
        user = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = dict(User._meta.get_field('status').choices).keys()
        if new_status not in valid_statuses:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.status = new_status
        user.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='update',
            content_type_id=40,
            object_id=user.id,
            description=f'Changed user status to {new_status}',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(self.get_serializer(user).data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsSuperAdmin])
    def super_admins(self, request):
        """Get all super admin users."""
        users = User.objects.filter(role='super_admin')
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsInstitutionAdmin])
    def institution_users(self, request):
        """Get users in current user's institution."""
        users = User.objects.filter(institution=request.user.institution)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
