from django.urls import include, path
from rest_framework.routers import DefaultRouter

from userstory.views import EpicViewSet, UserStoryViewSet

router = DefaultRouter()
router.register(r'stories', UserStoryViewSet, basename='userstory')
router.register(r'epics', EpicViewSet, basename='epic')

urlpatterns = [
    path('', include(router.urls)),
]
