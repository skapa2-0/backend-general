from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Organisation, Project, UserProfile
from core.permissions import IsOrganisationAdmin, IsOrganisationMember
from core.serializers import (
    OrganisationSerializer,
    ProjectSerializer,
    UserProfileSerializer,
)


class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
    permission_classes = [IsOrganisationMember]

    def get_queryset(self):
        user = self.request.user
        if user.organisation_id:
            return Organisation.objects.filter(id=user.organisation_id)
        return Organisation.objects.none()


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOrganisationMember]

    def get_queryset(self):
        user = self.request.user
        if user.organisation_id:
            return UserProfile.objects.filter(organisation_id=user.organisation_id)
        return UserProfile.objects.none()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['organisation']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']

    def get_queryset(self):
        user = self.request.user
        if user.organisation_id:
            return Project.objects.filter(organisation_id=user.organisation_id)
        return Project.objects.none()

    def get_permissions(self):
        if self.action in ('destroy',):
            return [IsOrganisationAdmin()]
        return super().get_permissions()
