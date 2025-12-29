from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.models import Applicant
from admin_panel.serializers import (
    ApplicantListSerializer, ApplicantDetailSerializer, ApplicantCreateSerializer
)
from admin_panel.filters import ApplicantFilter


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
        from admin_panel.serializers import ApplicationListSerializer
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
