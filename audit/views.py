from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from audit.models import (
    Audit,
    AuditComposant,
    AuditCritere,
    AuditEcran,
    AuditHeuristique,
    AuditMaturity,
    AuditProcessus,
    AuditRecommandation,
)
from audit.serializers import (
    AuditComposantSerializer,
    AuditCritereSerializer,
    AuditDetailSerializer,
    AuditEcranSerializer,
    AuditHeuristiqueSerializer,
    AuditListSerializer,
    AuditMaturitySerializer,
    AuditProcessusSerializer,
    AuditRecommandationSerializer,
)


class AuditViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'status', 'source_type']
    search_fields = ['name']
    ordering_fields = ['created_at', 'score_global', 'status']

    def get_queryset(self):
        return Audit.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        ).select_related('created_by', 'project')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuditDetailSerializer
        return AuditListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AuditCritereViewSet(viewsets.ModelViewSet):
    serializer_class = AuditCritereSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit', 'type']

    def get_queryset(self):
        return AuditCritere.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        ).prefetch_related('heuristiques')


class AuditHeuristiqueViewSet(viewsets.ModelViewSet):
    serializer_class = AuditHeuristiqueSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['critere', 'critere__audit']

    def get_queryset(self):
        return AuditHeuristique.objects.filter(
            critere__audit__project__organisation_id=self.request.user.organisation_id,
        )


class AuditEcranViewSet(viewsets.ModelViewSet):
    serializer_class = AuditEcranSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit']

    def get_queryset(self):
        return AuditEcran.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        )


class AuditProcessusViewSet(viewsets.ModelViewSet):
    serializer_class = AuditProcessusSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit']

    def get_queryset(self):
        return AuditProcessus.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        )


class AuditRecommandationViewSet(viewsets.ModelViewSet):
    serializer_class = AuditRecommandationSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit', 'type', 'priority', 'status']
    ordering_fields = ['priority', 'effort', 'status']

    def get_queryset(self):
        return AuditRecommandation.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        )


class AuditComposantViewSet(viewsets.ModelViewSet):
    serializer_class = AuditComposantSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit', 'severity']

    def get_queryset(self):
        return AuditComposant.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        )


class AuditMaturityViewSet(viewsets.ModelViewSet):
    serializer_class = AuditMaturitySerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['audit']

    def get_queryset(self):
        return AuditMaturity.objects.filter(
            audit__project__organisation_id=self.request.user.organisation_id,
        )
