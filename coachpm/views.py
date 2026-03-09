from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from coachpm.models import CoachSession, PMRecommendation
from coachpm.serializers import (
    CoachSessionDetailSerializer,
    CoachSessionListSerializer,
    PMRecommendationSerializer,
)


class CoachSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project']
    search_fields = ['title', 'topic']

    def get_queryset(self):
        return CoachSession.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoachSessionDetailSerializer
        return CoachSessionListSerializer


class PMRecommendationViewSet(viewsets.ModelViewSet):
    serializer_class = PMRecommendationSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['session', 'priority', 'category']

    def get_queryset(self):
        return PMRecommendation.objects.filter(
            session__project__organisation_id=self.request.user.organisation_id,
        )
