from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import Experience
from admin_panel.serializers import ExperienceSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['start_date']
    ordering = ['-start_date']
    
    @action(detail=False, methods=['get'])
    def by_applicant(self, request):
        from rest_framework import status
        applicant_id = request.query_params.get('applicant_id')
        if applicant_id:
            experience = Experience.objects.filter(applicant_id=applicant_id)
            serializer = ExperienceSerializer(experience, many=True)
            return Response(serializer.data)
        return Response({'error': 'Applicant ID required'}, status=status.HTTP_400_BAD_REQUEST)
