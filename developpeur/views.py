from rest_framework import viewsets

from core.permissions import IsOrganisationMember
from developpeur.models import CodeGeneration, CodeIssue, CodeProject, PageConfig
from developpeur.serializers import (
    CodeGenerationSerializer,
    CodeIssueSerializer,
    CodeProjectDetailSerializer,
    CodeProjectListSerializer,
    PageConfigSerializer,
)


class CodeProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['project', 'status']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return CodeProject.objects.filter(
            project__organisation_id=self.request.user.organisation_id,
        ).select_related('created_by')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CodeProjectDetailSerializer
        return CodeProjectListSerializer


class PageConfigViewSet(viewsets.ModelViewSet):
    serializer_class = PageConfigSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['code_project']

    def get_queryset(self):
        return PageConfig.objects.filter(
            code_project__project__organisation_id=self.request.user.organisation_id,
        )


class CodeGenerationViewSet(viewsets.ModelViewSet):
    serializer_class = CodeGenerationSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['code_project', 'page', 'status', 'language']

    def get_queryset(self):
        return CodeGeneration.objects.filter(
            code_project__project__organisation_id=self.request.user.organisation_id,
        )


class CodeIssueViewSet(viewsets.ModelViewSet):
    serializer_class = CodeIssueSerializer
    permission_classes = [IsOrganisationMember]
    filterset_fields = ['code_project', 'type', 'status', 'assigned_group']

    def get_queryset(self):
        return CodeIssue.objects.filter(
            code_project__project__organisation_id=self.request.user.organisation_id,
        )
