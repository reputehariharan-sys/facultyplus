"""
Job ViewSet for job posting management with role-based permissions.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from admin_panel.models import Job, ActivityLog
from admin_panel.serializers import (
    JobListSerializer, JobDetailSerializer, JobCreateUpdateSerializer,
    JobApprovalSerializer, JobSelectionSerializer, ApplicationListSerializer
)
from admin_panel.permissions import (
    IsSuperAdmin, IsHOD, IsHR, CanCreateOrApproveJob, CanAccessDepartment
)


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for job management with role-based access control.
    - HOD: Can create jobs (draft), view owned jobs
    - HR: Can approve/publish jobs, view jobs in assigned colleges
    - Super Admin: Can view all jobs
    - Public: Can view published jobs (read-only)
    """
    queryset = Job.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_status', 'institution', 'college', 'department', 'priority']
    search_fields = ['job_title', 'job_description', 'qualification']
    ordering_fields = ['created_at', 'last_date', 'priority', 'job_status']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        elif self.action == 'retrieve':
            return JobDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return JobCreateUpdateSerializer
        elif self.action == 'approve_job':
            return JobApprovalSerializer
        elif self.action == 'mark_selected':
            return JobSelectionSerializer
        return JobDetailSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            # Anyone can list published jobs, HOD/HR/Admin can see their jobs
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'retrieve':
            # Anyone can view published jobs, auth users can view their jobs
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['create']:
            # Only HOD can create jobs
            permission_classes = [IsAuthenticated, IsHOD]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only job creator or admin can edit/delete
            permission_classes = [IsAuthenticated]
        elif self.action == 'approve_job':
            # Only HR or Super Admin can approve
            permission_classes = [IsAuthenticated, IsHR]
        elif self.action == 'mark_selected':
            # Only HR or admin can mark selected
            permission_classes = [IsAuthenticated, IsHR]
        elif self.action in ['applications', 'view_applicants']:
            # HOD and HR can view applications for their jobs
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter jobs based on user role."""
        user = self.request.user
        queryset = Job.objects.all().order_by('-created_at')
        
        if user.is_authenticated:
            # Super Admin sees all
            if user.role == 'super_admin':
                return queryset
            # Institution Admin sees all in their institution
            elif user.role == 'institution_admin':
                return queryset.filter(institution=user.institution)
            # HR sees jobs in their assigned colleges
            elif user.role == 'hr':
                return queryset.filter(college__in=user.assigned_colleges.all())
            # HOD sees jobs in their assigned departments
            elif user.role == 'hod':
                return queryset.filter(department__in=user.assigned_departments.all())
            # Applicants see published jobs only
            elif user.role == 'applicant':
                return queryset.filter(job_status='published')
        else:
            # Unauthenticated users see published jobs only
            return queryset.filter(job_status='published')
    
    def perform_create(self, serializer):
        """Create a job with HOD as creator."""
        job = serializer.save(created_by=self.request.user, job_status='draft')
        # Log activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='create',
            content_type_id=38,  # Job content type
            object_id=job.id,
            description=f'Created job: {job.job_title}',
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
    
    def perform_update(self, serializer):
        """Update job."""
        job = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action='update',
            content_type_id=38,  # Job content type
            object_id=job.id,
            description=f'Updated job: {job.job_title}',
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
    def approve_job(self, request, pk=None):
        """Approve and publish a job (HR only)."""
        job = self.get_object()
        
        if job.job_status != 'pending_approval':
            return Response(
                {'error': 'Job must be in pending_approval status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.job_status = 'published'
        job.approved_by = request.user
        job.published_at = timezone.now()
        job.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='approve',
            content_type_id=38,  # Job content type
            object_id=job.id,
            description=f'Approved and published job: {job.job_title}',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        serializer = self.get_serializer(job)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsHR])
    def mark_selected(self, request, pk=None):
        """Mark an applicant as selected for a job (HR only)."""
        job = self.get_object()
        applicant_id = request.data.get('selected_applicant')
        
        if not applicant_id:
            return Response(
                {'error': 'selected_applicant is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.selected_applicant_id = applicant_id
        job.job_status = 'closed'
        job.closed_at = timezone.now()
        job.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='update',
            content_type_id=38,  # Job content type
            object_id=job.id,
            details=f'Marked applicant as selected for job: {job.job_title}',
            ip_address=self.get_client_ip(),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        serializer = self.get_serializer(job)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for a job."""
        job = self.get_object()
        applications = job.applications.all().order_by('-applied_date')
        page = self.paginate_queryset(applications)
        if page is not None:
            serializer = ApplicationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def published_jobs(self, request):
        """Get all published jobs."""
        jobs = self.get_queryset().filter(job_status='published')
        page = self.paginate_queryset(jobs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_approval(self, request):
        """Get jobs pending approval (HR only)."""
        if request.user.role != 'hr':
            return Response(
                {'error': 'Only HR can view pending approvals'},
                status=status.HTTP_403_FORBIDDEN
            )
        jobs = self.get_queryset().filter(job_status='pending_approval')
        page = self.paginate_queryset(jobs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)


from django.utils import timezone
