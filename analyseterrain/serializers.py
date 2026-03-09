from rest_framework import serializers

from analyseterrain.models import FieldObservation, FieldStudy


class FieldObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldObservation
        fields = ['id', 'study', 'title', 'description', 'category', 'sentiment', 'tags', 'created_at']
        read_only_fields = ['id', 'created_at']


class FieldStudyListSerializer(serializers.ModelSerializer):
    observation_count = serializers.IntegerField(source='observations.count', read_only=True)

    class Meta:
        model = FieldStudy
        fields = [
            'id', 'project', 'name', 'description', 'methodology',
            'status', 'participants_count', 'observation_count',
            'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FieldStudyDetailSerializer(FieldStudyListSerializer):
    observations = FieldObservationSerializer(many=True, read_only=True)

    class Meta(FieldStudyListSerializer.Meta):
        fields = FieldStudyListSerializer.Meta.fields + ['observations']
