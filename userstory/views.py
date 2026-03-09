from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from userstory.models import Epic, UserStory
from userstory.serializers import EpicSerializer, UserStorySerializer


class UserStoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserStorySerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'priority', 'status']
    search_fields = ['title', 'description', 'as_a']

    def get_queryset(self):
        return UserStory.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        )


class EpicViewSet(viewsets.ModelViewSet):
    serializer_class = EpicSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Epic.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        ).prefetch_related('user_stories')
