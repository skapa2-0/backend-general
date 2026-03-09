from rest_framework import serializers

from core.models import Organisation, Project, UserProfile


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id', 'name', 'slug', 'clerk_org_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    organisation_name = serializers.CharField(
        source='organisation.name', read_only=True, default=None,
    )

    class Meta:
        model = UserProfile
        fields = [
            'id', 'clerk_user_id', 'organisation', 'organisation_name',
            'role', 'email', 'name', 'created_at',
        ]
        read_only_fields = ['id', 'clerk_user_id', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.name', read_only=True, default=None,
    )

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'organisation',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
