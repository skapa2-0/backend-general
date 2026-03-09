from django.urls import include, path
from rest_framework.routers import DefaultRouter

from analyseterrain.views import FieldObservationViewSet, FieldStudyViewSet

router = DefaultRouter()
router.register(r'studies', FieldStudyViewSet, basename='fieldstudy')
router.register(r'observations', FieldObservationViewSet, basename='fieldobservation')

urlpatterns = [
    path('', include(router.urls)),
]
