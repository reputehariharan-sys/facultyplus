from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.utils import timezone
from admin_panel.models import User, ActivityLog, Applicant
from admin_panel.serializers import UserDetailSerializer, UserProfileSerializer, ChangePasswordSerializer
import logging

logger = logging.getLogger(__name__)


class CustomTokenAuth(ObtainAuthToken):
    """
    Custom token authentication view
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.status == 'inactive':
            return Response(
                {'error': 'User account is inactive'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, created = Token.objects.get_or_create(user=user)
        
        # Log the login action
        ip_address = self.get_client_ip(request)
        user.last_login_ip = ip_address
        user.last_action = 'login'
        user.last_action_time = timezone.now()
        user.save()
        
        ActivityLog.objects.create(
            user=user,
            action='login',
            description=f'{user.username} logged in from {ip_address}',
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'token': token.key,
            'user': UserDetailSerializer(user).data,
            'message': f'Welcome {user.get_full_name() or user.username}!'
        })
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout view
    POST /api/auth/logout/
    """
    user = request.user
    ip_address = request.META.get('REMOTE_ADDR', '')
    
    # Log the logout action
    ActivityLog.objects.create(
        user=user,
        action='logout',
        description=f'{user.username} logged out',
        ip_address=ip_address,
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Delete token
    try:
        user.auth_token.delete()
    except:
        pass
    
    return Response(
        {'message': 'Logged out successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    GET /api/auth/profile/
    """
    return Response(UserProfileSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password
    POST /api/auth/change-password/
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(old_password):
        return Response(
            {'error': 'Old password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_password)
    user.save()
    
    # Log password change
    ActivityLog.objects.create(
        user=user,
        action='update',
        description='User changed password',
        ip_address=request.META.get('REMOTE_ADDR', '')
    )
    
    return Response({'message': 'Password changed successfully'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_applicant(request):
    """
    Register a new applicant account
    POST /api/auth/register/
    """
    from admin_panel.serializers import UserCreateSerializer
    
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(role='applicant')
        token, created = Token.objects.get_or_create(user=user)
        
        ActivityLog.objects.create(
            user=user,
            action='create',
            description='New applicant registered',
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        return Response({
            'token': token.key,
            'user': UserDetailSerializer(user).data,
            'message': 'Registration successful!'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
