from django.urls import include, path
from rest_framework.routers import DefaultRouter

from designsystem.views import DesignSystemAuditViewSet, DSComponentViewSet

router = DefaultRouter()
router.register(r'audits', DesignSystemAuditViewSet, basename='dsaudit')
router.register(r'components', DSComponentViewSet, basename='dscomponent')

urlpatterns = [
    path('', include(router.urls)),
]
