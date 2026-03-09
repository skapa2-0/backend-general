from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from designsystem.models import DesignSystemAudit, DSComponent
from designsystem.serializers import (
    DesignSystemAuditDetailSerializer,
    DesignSystemAuditListSerializer,
    DSComponentSerializer,
)


class DesignSystemAuditViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'status']
    search_fields = ['name']

    def get_queryset(self):
        return DesignSystemAudit.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DesignSystemAuditDetailSerializer
        return DesignSystemAuditListSerializer


class DSComponentViewSet(viewsets.ModelViewSet):
    serializer_class = DSComponentSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit', 'status']
    search_fields = ['name']

    def get_queryset(self):
        return DSComponent.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        )
