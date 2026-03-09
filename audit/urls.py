from django.urls import include, path
from rest_framework.routers import DefaultRouter

from audit.views import (
    AuditComposantViewSet,
    AuditCritereViewSet,
    AuditEcranViewSet,
    AuditHeuristiqueViewSet,
    AuditMaturityViewSet,
    AuditProcessusViewSet,
    AuditRecommandationViewSet,
    AuditViewSet,
)

router = DefaultRouter()
router.register(r'audits', AuditViewSet, basename='audit')
router.register(r'criteres', AuditCritereViewSet, basename='auditcritere')
router.register(r'heuristiques', AuditHeuristiqueViewSet, basename='auditheuristique')
router.register(r'ecrans', AuditEcranViewSet, basename='auditecran')
router.register(r'processus', AuditProcessusViewSet, basename='auditprocessus')
router.register(r'recommandations', AuditRecommandationViewSet, basename='auditrecommandation')
router.register(r'composants', AuditComposantViewSet, basename='auditcomposant')
router.register(r'maturity', AuditMaturityViewSet, basename='auditmaturity')

urlpatterns = [
    path('', include(router.urls)),
]
