from django.urls import include, path
from rest_framework.routers import DefaultRouter

from developpeur.views import (
    CodeGenerationViewSet,
    CodeIssueViewSet,
    CodeProjectViewSet,
    PageConfigViewSet,
)

router = DefaultRouter()
router.register(r'projects', CodeProjectViewSet, basename='codeproject')
router.register(r'pages', PageConfigViewSet, basename='pageconfig')
router.register(r'generations', CodeGenerationViewSet, basename='codegeneration')
router.register(r'issues', CodeIssueViewSet, basename='codeissue')

urlpatterns = [
    path('', include(router.urls)),
]
