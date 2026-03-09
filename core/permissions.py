from rest_framework.permissions import BasePermission

from core.models import UserProfile


class IsOrganisationMember(BasePermission):
    """Allow access only to members of the same organisation as the resource."""

    def has_permission(self, request, view):
        return (
            request.user
            and isinstance(request.user, UserProfile)
            and request.user.organisation_id is not None
        )

    def has_object_permission(self, request, view, obj):
        org = getattr(obj, 'organisation', None)
        if org is None:
            org = getattr(obj, 'project', None)
            if org is not None:
                org = getattr(org, 'organisation', None)
        if org is None:
            return False
        return request.user.organisation_id == org.id


class IsOrganisationAdmin(BasePermission):
    """Allow access only to organisation admins."""

    def has_permission(self, request, view):
        return (
            request.user
            and isinstance(request.user, UserProfile)
            and request.user.role == UserProfile.Role.ADMIN
        )
