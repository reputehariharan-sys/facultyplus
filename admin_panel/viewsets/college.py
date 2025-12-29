from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import College
from admin_panel.serializers import CollegeSerializer
from admin_panel.filters import CollegeFilter


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
        from admin_panel.serializers import DepartmentSerializer
        college = self.get_object()
        departments = college.departments.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        from admin_panel.serializers import JobSerializer
        college = self.get_object()
        jobs = college.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
