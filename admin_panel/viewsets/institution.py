from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import Institution
from admin_panel.serializers import InstitutionSerializer
from admin_panel.filters import InstitutionFilter


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
        from admin_panel.serializers import CollegeSerializer
        institution = self.get_object()
        colleges = institution.colleges.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        from admin_panel.serializers import DepartmentSerializer
        institution = self.get_object()
        departments = institution.departments.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        from admin_panel.serializers import JobSerializer
        institution = self.get_object()
        jobs = institution.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
