"""
URL configuration for facultyplus project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from admin_panel import auth_views
from admin_panel.viewsets import (
    UserViewSet, InstitutionViewSet, CollegeViewSet, DepartmentViewSet,
    JobViewSet, ApplicationViewSet, ApplicantViewSet, ActivityLogViewSet,
    EducationViewSet, ExperienceViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'institutions', InstitutionViewSet, basename='institution')
router.register(r'colleges', CollegeViewSet, basename='college')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')
# router.register(r'applicants', ApplicantViewSet, basename='applicant')
router.register(r'activity-logs', ActivityLogViewSet, basename='activity-log')
# router.register(r'educations', EducationViewSet, basename='education')
# router.register(r'experiences', ExperienceViewSet, basename='experience')

# Authentication URLs
from rest_framework_simplejwt.views import TokenRefreshView

auth_patterns = [
    # path('login/', auth_views.CustomTokenAuth.as_view(), name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('profile/', auth_views.user_profile, name='profile'),
    path('change-password/', auth_views.change_password, name='change-password'),
    path('register/', auth_views.register_applicant, name='register-applicant'),

    # JWT endpoints
    path('login/', auth_views.CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# OpenAPI/Swagger URLs
swagger_patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(auth_patterns)),
    path('api/', include(router.urls)),
    path('', include(swagger_patterns)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
