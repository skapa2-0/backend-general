from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from epersona.models import Conversation, Insight, Message, Persona, Source
from epersona.serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    InsightSerializer,
    MessageSerializer,
    PersonaSerializer,
    SourceSerializer,
)


class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'is_active']
    search_fields = ['name', 'role']

    def get_queryset(self):
        return Persona.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'type']
    search_fields = ['title']

    def get_queryset(self):
        return Conversation.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        ).prefetch_related('personas')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationListSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['conversation', 'role']

    def get_queryset(self):
        return Message.objects.filter(
            conversation__project__organisation_id=self.request.user.organisation_id,
        ).select_related('persona')


class SourceViewSet(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'type', 'status']

    def get_queryset(self):
        return Source.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )


class InsightViewSet(viewsets.ModelViewSet):
    serializer_class = InsightSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'type', 'impact', 'conversation']
    ordering_fields = ['mentions', 'created_at']

    def get_queryset(self):
        return Insight.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )
