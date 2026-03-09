from rest_framework import serializers

from developpeur.models import CodeGeneration, CodeIssue, CodeProject, PageConfig


class PageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageConfig
        fields = ['id', 'code_project', 'name', 'path', 'description', 'components', 'order']
        read_only_fields = ['id']


class CodeGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeGeneration
        fields = [
            'id', 'code_project', 'page', 'file_path', 'content',
            'language', 'status', 'validated_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class CodeIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeIssue
        fields = [
            'id', 'code_project', 'title', 'description',
            'type', 'status', 'assigned_group', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class CodeProjectListSerializer(serializers.ModelSerializer):
    page_count = serializers.IntegerField(source='pages.count', read_only=True)

    class Meta:
        model = CodeProject
        fields = [
            'id', 'project', 'name', 'description', 'tech_stack',
            'status', 'page_count', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CodeProjectDetailSerializer(CodeProjectListSerializer):
    pages = PageConfigSerializer(many=True, read_only=True)
    generations = CodeGenerationSerializer(many=True, read_only=True)
    issues = CodeIssueSerializer(many=True, read_only=True)

    class Meta(CodeProjectListSerializer.Meta):
        fields = CodeProjectListSerializer.Meta.fields + ['pages', 'generations', 'issues']
