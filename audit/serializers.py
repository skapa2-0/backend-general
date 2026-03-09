from rest_framework import serializers

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


class AuditHeuristiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditHeuristique
        fields = [
            'id', 'critere', 'name', 'code', 'score',
            'definition', 'patterns_detectes', 'ecrans_concernes',
        ]
        read_only_fields = ['id']


class AuditCritereSerializer(serializers.ModelSerializer):
    heuristiques = AuditHeuristiqueSerializer(many=True, read_only=True)

    class Meta:
        model = AuditCritere
        fields = [
            'id', 'audit', 'type', 'name', 'code', 'score',
            'description', 'ecrans_impactes', 'processus_impactes',
            'recommendations_count', 'heuristiques',
        ]
        read_only_fields = ['id']


class AuditEcranSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditEcran
        fields = [
            'id', 'audit', 'path', 'name', 'score',
            'issues', 'composants', 'viewer_annotations',
        ]
        read_only_fields = ['id']


class AuditProcessusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditProcessus
        fields = ['id', 'audit', 'name', 'score', 'etapes', 'problemes']
        read_only_fields = ['id']


class AuditRecommandationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditRecommandation
        fields = [
            'id', 'audit', 'title', 'description', 'type', 'priority',
            'effort', 'gain_estime', 'critere', 'ecran',
            'jira_ticket_url', 'status',
        ]
        read_only_fields = ['id']


class AuditComposantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditComposant
        fields = ['id', 'audit', 'name', 'type', 'occurrences', 'problemes', 'severity']
        read_only_fields = ['id']


class AuditMaturitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditMaturity
        fields = ['id', 'audit', 'ux_level', 'rgaa_level', 'eco_level', 'designsys_level', 'roadmap']
        read_only_fields = ['id']


class AuditListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True, default=None)

    class Meta:
        model = Audit
        fields = [
            'id', 'project', 'name', 'source_url', 'source_type',
            'audit_types', 'status', 'score_global', 'score_ux',
            'score_rgaa', 'score_eco', 'score_designsys',
            'created_by', 'created_by_name', 'created_at', 'updated_at', 'completed_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'completed_at']


class AuditDetailSerializer(AuditListSerializer):
    criteres = AuditCritereSerializer(many=True, read_only=True)
    ecrans = AuditEcranSerializer(many=True, read_only=True)
    processus = AuditProcessusSerializer(many=True, read_only=True)
    recommandations = AuditRecommandationSerializer(many=True, read_only=True)
    composants = AuditComposantSerializer(many=True, read_only=True)
    maturity = AuditMaturitySerializer(read_only=True)

    class Meta(AuditListSerializer.Meta):
        fields = AuditListSerializer.Meta.fields + [
            'criteres', 'ecrans', 'processus',
            'recommandations', 'composants', 'maturity',
        ]
