from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import HRAssignment
from admin_panel.serializers import HRAssignmentSerializer
from admin_panel.filters import HRAssignmentFilter


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
        from rest_framework import status
        institution_id = request.query_params.get('institution_id')
        if institution_id:
            assignments = HRAssignment.objects.filter(institution_id=institution_id)
            serializer = HRAssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
        return Response({'error': 'Institution ID required'}, status=status.HTTP_400_BAD_REQUEST)
