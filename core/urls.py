from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import OrganisationViewSet, ProjectViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'organisations', OrganisationViewSet, basename='organisation')
router.register(r'users', UserProfileViewSet, basename='userprofile')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
