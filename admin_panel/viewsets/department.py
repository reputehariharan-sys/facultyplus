from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import Department
from admin_panel.serializers import DepartmentSerializer
from admin_panel.filters import DepartmentFilter


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
        from admin_panel.serializers import JobSerializer
        department = self.get_object()
        jobs = department.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
