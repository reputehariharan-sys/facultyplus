"""
Application ViewSet for managing job applications with role-based access.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from admin_panel.models import Application, ActivityLog
from django.contrib.contenttypes.models import ContentType
from admin_panel.serializers import (
    ApplicationListSerializer, ApplicationDetailSerializer, ApplicationCreateSerializer,
    ApplicationStatusUpdateSerializer
)
from admin_panel.permissions import IsHR, IsHOD, CanManageApplications


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for job application management with role-based permissions.
    - Applicant: Can create and view their own applications
    - HOD/HR: Can view applications for their jobs
    - Super Admin: Can view all applications
    """
    queryset = Application.objects.all().order_by('-applied_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job', 'status', 'applied_date']
    search_fields = ['applicant__user__email', 'applicant__user__first_name', 'job__job_title']
    ordering_fields = ['applied_date', 'status', 'status_changed_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApplicationDetailSerializer
        elif self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action in ['update_status', 'mark_under_review', 'move_to_interview', 'mark_shortlisted', 'mark_selected', 'mark_rejected']:
            return ApplicationStatusUpdateSerializer
        return ApplicationListSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update_status', 'mark_under_review', 'move_to_interview', 'mark_shortlisted', 'mark_selected', 'mark_rejected']:
            permission_classes = [IsAuthenticated, IsHR]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter applications based on user role."""
        user = self.request.user
        queryset = Application.objects.all().order_by('-applied_date')
        
        if user.is_authenticated:
            if user.role == 'super_admin':
                return queryset
            elif user.role == 'institution_admin':
                return queryset.filter(job__institution=user.institution)
            elif user.role == 'hr':
                # HR sees applications for jobs in their colleges
                return queryset.filter(job__college__in=user.assigned_colleges.all())
            elif user.role == 'hod':
                # HOD sees applications for jobs in their departments
                return queryset.filter(job__department__in=user.assigned_departments.all())
            elif user.role == 'applicant':
                # Applicants see only their own applications
                from admin_panel.models import Applicant
                try:
                    applicant = Applicant.objects.get(user=user)
                    return queryset.filter(applicant=applicant)
                except Applicant.DoesNotExist:
                    return queryset.none()
        return queryset.none()
    
    def perform_create(self, serializer):
        """Create an application."""
        application = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='apply',
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application.id,
            description=f'Applied for job: {application.job.job_title}',
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
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def update_status(self, request, pk=None):
        """Update application status with remarks."""
        application = self.get_object()
        serializer = self.get_serializer(application, data=request.data, partial=True)
        
        if serializer.is_valid():
            new_status = serializer.validated_data.get('status')
            remarks = serializer.validated_data.get('remarks', '')
            
            application.status = new_status
            application.status_changed_by = request.user
            application.status_changed_at = timezone.now()
            if remarks:
                application.remarks = remarks
            application.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='status_change',
                content_type=ContentType.objects.get_for_model(Application),
                object_id=application.id,
                description=f'Changed application status to {new_status}',
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response(self.get_serializer(application).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def mark_under_review(self, request, pk=None):
        """Mark application as under review."""
        application = self.get_object()
        application.status = 'under_review'
        application.status_changed_by = request.user
        application.status_changed_at = timezone.now()
        application.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='status_change',
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application.id,
            description='Marked application as under review',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(self.get_serializer(application).data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def move_to_interview(self, request, pk=None):
        """Move application to interview stage."""
        application = self.get_object()
        application.status = 'interviewing'
        application.status_changed_by = request.user
        application.status_changed_at = timezone.now()
        application.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='status_change',
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application.id,
            description='Moved application to interview stage',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(self.get_serializer(application).data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def mark_shortlisted(self, request, pk=None):
        """Mark application as shortlisted."""
        application = self.get_object()
        application.status = 'shortlisted'
        application.status_changed_by = request.user
        application.status_changed_at = timezone.now()
        application.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='status_change',
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application.id,
            description='Marked application as shortlisted',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(self.get_serializer(application).data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def mark_selected(self, request, pk=None):
        """Mark application as selected."""
        application = self.get_object()
        application.status = 'selected'
        application.status_changed_by = request.user
        application.status_changed_at = timezone.now()
        application.email_selection_sent = True
        application.save()
        
        # Update job with selected applicant
        application.job.selected_applicant = application.applicant
        application.job.job_status = 'closed'
        application.job.closed_at = timezone.now()
        application.job.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='status_change',
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application.id,
            description='Marked application as selected',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(self.get_serializer(application).data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def mark_rejected(self, request, pk=None):
        """Mark application as rejected."""
        application = self.get_object()
        remarks = request.data.get('remarks', '')
        
        application.status = 'rejected'
        application.status_changed_by = request.user
        application.status_changed_at = timezone.now()
        application.email_rejection_sent = True
        if remarks:
            application.remarks = remarks
        application.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='status_change',
            content_type=ContentType.objects.get_for_model(Application),
            object_id=application.id,
            description=f'Marked application as rejected. Remarks: {remarks}',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(self.get_serializer(application).data)
    
    @action(detail=False, methods=['get'])
    def by_job(self, request):
        """Get all applications for a job."""
        job_id = request.query_params.get('job_id')
        if not job_id:
            return Response(
                {'error': 'job_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        applications = self.get_queryset().filter(job_id=job_id)
        page = self.paginate_queryset(applications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """Get current user's applications (Applicant)."""
        from admin_panel.models import Applicant
        try:
            applicant = Applicant.objects.get(user=request.user)
            applications = Application.objects.filter(applicant=applicant).order_by('-applied_date')
            page = self.paginate_queryset(applications)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(applications, many=True)
            return Response(serializer.data)
        except Applicant.DoesNotExist:
            return Response(
                {'error': 'Applicant profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if applicant_id:
            applications = Application.objects.filter(applicant_id=applicant_id)
            serializer = ApplicationListSerializer(applications, many=True)
            return Response(serializer.data)
        return Response({'error': 'Applicant ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Application.objects.count()
        submitted = Application.objects.filter(status='submitted').count()
        shortlisted = Application.objects.filter(status='shortlisted').count()
        rejected = Application.objects.filter(status='rejected').count()
        accepted = Application.objects.filter(status='accepted').count()
        
        return Response({
            'total_applications': total,
            'submitted': submitted,
            'shortlisted': shortlisted,
            'rejected': rejected,
            'accepted': accepted,
        })
