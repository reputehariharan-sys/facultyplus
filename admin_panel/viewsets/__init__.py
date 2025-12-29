from .user import UserViewSet
from .institution import InstitutionViewSet
from .college import CollegeViewSet
from .department import DepartmentViewSet
from .job import JobViewSet
from .hr_assignment import HRAssignmentViewSet
from .education import EducationViewSet
from .experience import ExperienceViewSet
from .applicant import ApplicantViewSet
from .application import ApplicationViewSet
from admin_panel.viewsets.activity_log import ActivityLogViewSet

__all__ = [
    'UserViewSet',
    'InstitutionViewSet',
    'CollegeViewSet',
    'DepartmentViewSet',
    'JobViewSet',
    'HRAssignmentViewSet',
    'EducationViewSet',
    'ExperienceViewSet',
    'ApplicantViewSet',
    'ApplicationViewSet',
    'ActivityLogViewSet',
]
