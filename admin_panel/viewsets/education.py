from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import Education
from admin_panel.serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['year_of_passing', 'percentage']
    ordering = ['-year_of_passing']
    
    @action(detail=False, methods=['get'])
    def by_applicant(self, request):
        from rest_framework import status
        applicant_id = request.query_params.get('applicant_id')
        if applicant_id:
            education = Education.objects.filter(applicant_id=applicant_id)
            serializer = EducationSerializer(education, many=True)
            return Response(serializer.data)
        return Response({'error': 'Applicant ID required'}, status=status.HTTP_400_BAD_REQUEST)
