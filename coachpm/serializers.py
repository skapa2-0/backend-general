from rest_framework import serializers

from coachpm.models import CoachSession, PMRecommendation


class PMRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMRecommendation
        fields = ['id', 'session', 'title', 'description', 'category', 'priority', 'created_at']
        read_only_fields = ['id', 'created_at']


class CoachSessionListSerializer(serializers.ModelSerializer):
    recommendation_count = serializers.IntegerField(source='recommendations.count', read_only=True)

    class Meta:
        model = CoachSession
        fields = [
            'id', 'project', 'title', 'topic', 'messages',
            'recommendation_count', 'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CoachSessionDetailSerializer(CoachSessionListSerializer):
    recommendations = PMRecommendationSerializer(many=True, read_only=True)

    class Meta(CoachSessionListSerializer.Meta):
        fields = CoachSessionListSerializer.Meta.fields + ['recommendations']
