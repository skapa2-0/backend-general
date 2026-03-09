from rest_framework import serializers

from epersona.models import Conversation, Insight, Message, Persona, Source


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            'id', 'project', 'name', 'role', 'context',
            'demographics', 'behaviors', 'goals', 'frustrations',
            'created_by', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    persona_name = serializers.CharField(source='persona.name', read_only=True, default=None)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'role', 'persona', 'persona_name', 'content', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    persona_names = serializers.SerializerMethodField()
    message_count = serializers.IntegerField(source='messages.count', read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id', 'project', 'title', 'type', 'personas', 'persona_names',
            'message_count', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_persona_names(self, obj):
        return list(obj.personas.values_list('name', flat=True))

    def create(self, validated_data):
        personas = validated_data.pop('personas', [])
        validated_data['created_by'] = self.context['request'].user
        conversation = Conversation.objects.create(**validated_data)
        if personas:
            conversation.personas.set(personas)
        return conversation


class ConversationDetailSerializer(ConversationListSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationListSerializer.Meta):
        fields = ConversationListSerializer.Meta.fields + ['messages']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = [
            'id', 'project', 'name', 'type', 'file_path', 'url',
            'status', 'metadata', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = [
            'id', 'project', 'conversation', 'type', 'title',
            'description', 'impact', 'mentions', 'source_references', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
