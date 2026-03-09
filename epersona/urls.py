from django.urls import include, path
from rest_framework.routers import DefaultRouter

from epersona.views import (
    ConversationViewSet,
    InsightViewSet,
    MessageViewSet,
    PersonaViewSet,
    SourceViewSet,
)

router = DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'sources', SourceViewSet, basename='source')
router.register(r'insights', InsightViewSet, basename='insight')

urlpatterns = [
    path('', include(router.urls)),
]
