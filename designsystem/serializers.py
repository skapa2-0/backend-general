from rest_framework import serializers

from designsystem.models import DesignSystemAudit, DSComponent


class DSComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSComponent
        fields = ['id', 'audit', 'name', 'type', 'status', 'issues']
        read_only_fields = ['id']


class DesignSystemAuditListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignSystemAudit
        fields = [
            'id', 'project', 'name', 'source_url', 'status',
            'score', 'components_analyzed', 'issues_found', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DesignSystemAuditDetailSerializer(DesignSystemAuditListSerializer):
    components = DSComponentSerializer(many=True, read_only=True)

    class Meta(DesignSystemAuditListSerializer.Meta):
        fields = DesignSystemAuditListSerializer.Meta.fields + ['components']
