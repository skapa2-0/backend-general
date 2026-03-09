from django.urls import include, path
from rest_framework.routers import DefaultRouter

from coachpm.views import CoachSessionViewSet, PMRecommendationViewSet

router = DefaultRouter()
router.register(r'sessions', CoachSessionViewSet, basename='coachsession')
router.register(r'recommendations', PMRecommendationViewSet, basename='pmrecommendation')

urlpatterns = [
    path('', include(router.urls)),
]
