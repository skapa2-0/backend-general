from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from analyseterrain.models import FieldObservation, FieldStudy
from analyseterrain.serializers import (
    FieldObservationSerializer,
    FieldStudyDetailSerializer,
    FieldStudyListSerializer,
)


class FieldStudyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'methodology', 'status']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return FieldStudy.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FieldStudyDetailSerializer
        return FieldStudyListSerializer


class FieldObservationViewSet(viewsets.ModelViewSet):
    serializer_class = FieldObservationSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['study', 'sentiment', 'category']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return FieldObservation.objects.filter(
            study__project__organisation_id=self.request.user.organisation_id,
        )
