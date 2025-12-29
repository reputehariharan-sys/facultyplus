from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    User, Institution, College, Department, Job,
    HRAssignment, Applicant, Education, Experience, Application
)
from .serializers import (
    UserSerializer, UserCreateSerializer, InstitutionSerializer,
    CollegeSerializer, DepartmentSerializer, JobSerializer,
    HRAssignmentSerializer, EducationSerializer, ExperienceSerializer,
    ApplicantListSerializer, ApplicantDetailSerializer, ApplicantCreateSerializer,
    ApplicationListSerializer, ApplicationDetailSerializer, ApplicationCreateSerializer
)
from .filters import (
    UserFilter, InstitutionFilter, CollegeFilter, DepartmentFilter,
    JobFilter, HRAssignmentFilter, ApplicantFilter, ApplicationFilter
)


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'phone']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        role = request.query_params.get('role')
        if role:
            users = User.objects.filter(role=role)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'Role parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        user = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(User._meta.get_field('status').choices):
            user.status = new_status
            user.save()
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


# Institution ViewSet
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = InstitutionFilter
    search_fields = ['institution_name', 'institution_code', 'institution_email']
    ordering_fields = ['created_at', 'institution_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def colleges(self, request, pk=None):
        institution = self.get_object()
        colleges = institution.colleges.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        institution = self.get_object()
        departments = institution.departments.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        institution = self.get_object()
        jobs = institution.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# College ViewSet
class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CollegeFilter
    search_fields = ['college_name', 'college_code', 'institution__institution_name']
    ordering_fields = ['created_at', 'college_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        college = self.get_object()
        departments = college.departments.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        college = self.get_object()
        jobs = college.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# Department ViewSet
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DepartmentFilter
    search_fields = ['department_name', 'department_code', 'college__college_name']
    ordering_fields = ['created_at', 'department_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        department = self.get_object()
        jobs = department.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['job_title', 'job_description']
    ordering_fields = ['created_at', 'job_title', 'last_date']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        job = self.get_object()
        applications = job.applications.all()
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        job = self.get_object()
        new_status = request.data.get('job_status')
        if new_status in dict(Job._meta.get_field('job_status').choices):
            job.job_status = new_status
            job.save()
            return Response(JobSerializer(job).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def open_jobs(self, request):
        jobs = Job.objects.filter(job_status='open')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# HR Assignment ViewSet
class HRAssignmentViewSet(viewsets.ModelViewSet):
    queryset = HRAssignment.objects.all()
    serializer_class = HRAssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HRAssignmentFilter
    search_fields = ['hr_user__username', 'institution__institution_name']
    ordering_fields = ['assigned_at']
    ordering = ['-assigned_at']
    
    @action(detail=False, methods=['get'])
    def by_institution(self, request):
        institution_id = request.query_params.get('institution_id')
        if institution_id:
            assignments = HRAssignment.objects.filter(institution_id=institution_id)
            serializer = HRAssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
        return Response({'error': 'Institution ID required'}, status=status.HTTP_400_BAD_REQUEST)


# Education ViewSet
class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['year_of_passing', 'percentage']
    ordering = ['-year_of_passing']
    
    @action(detail=False, methods=['get'])
    def by_applicant(self, request):
        applicant_id = request.query_params.get('applicant_id')
        if applicant_id:
            education = Education.objects.filter(applicant_id=applicant_id)
            serializer = EducationSerializer(education, many=True)
            return Response(serializer.data)
        return Response({'error': 'Applicant ID required'}, status=status.HTTP_400_BAD_REQUEST)


# Experience ViewSet
class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['start_date']
    ordering = ['-start_date']
    
    @action(detail=False, methods=['get'])
    def by_applicant(self, request):
        applicant_id = request.query_params.get('applicant_id')
        if applicant_id:
            experience = Experience.objects.filter(applicant_id=applicant_id)
            serializer = ExperienceSerializer(experience, many=True)
            return Response(serializer.data)
        return Response({'error': 'Applicant ID required'}, status=status.HTTP_400_BAD_REQUEST)


# Applicant ViewSet
class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ApplicantFilter
    search_fields = ['full_name', 'email', 'mobile_number']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApplicantDetailSerializer
        elif self.action == 'create':
            return ApplicantCreateSerializer
        return ApplicantListSerializer
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        applicant = self.get_object()
        applications = applicant.applications.all()
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        applicant = self.get_object()
        applicant.is_active = not applicant.is_active
        applicant.save()
        return Response(ApplicantListSerializer(applicant).data)


# Application ViewSet
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ApplicationFilter
    search_fields = ['applicant_name', 'applicant_email', 'job__job_title']
    ordering_fields = ['applied_date', 'status']
    ordering = ['-applied_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApplicationDetailSerializer
        elif self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationListSerializer
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Application._meta.get_field('status').choices):
            application.status = new_status
            application.save()
            return Response(ApplicationListSerializer(application).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_job(self, request):
        job_id = request.query_params.get('job_id')
        if job_id:
            applications = Application.objects.filter(job_id=job_id)
            serializer = ApplicationListSerializer(applications, many=True)
            return Response(serializer.data)
        return Response({'error': 'Job ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_applicant(self, request):
        applicant_id = request.query_params.get('applicant_id')
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
