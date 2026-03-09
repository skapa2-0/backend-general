from rest_framework import serializers

from userstory.models import Epic, UserStory


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = [
            'id', 'project', 'title', 'description', 'as_a', 'i_want',
            'so_that', 'acceptance_criteria', 'priority', 'story_points',
            'status', 'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EpicSerializer(serializers.ModelSerializer):
    story_count = serializers.IntegerField(source='user_stories.count', read_only=True)

    class Meta:
        model = Epic
        fields = ['id', 'project', 'title', 'description', 'user_stories', 'story_count', 'created_at']
        read_only_fields = ['id', 'created_at']
