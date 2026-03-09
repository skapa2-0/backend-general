from django.db import models

from core.models import Project, UserProfile


class Persona(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='personas')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    context = models.TextField(blank=True)
    demographics = models.JSONField(default=dict)
    behaviors = models.JSONField(default=list)
    goals = models.JSONField(default=list)
    frustrations = models.JSONField(default=list)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='personas')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.role})'


class Conversation(models.Model):
    class Type(models.TextChoices):
        CHAT_LIBRE = 'chat_libre', 'Chat libre'
        DISCUSSION_STRUCTUREE = 'discussion_structuree', 'Discussion structurée'
        MULTI_PERSONA = 'multi_persona', 'Multi-persona'
        FOCUS_GROUP = 'focus_group', 'Focus group'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=30, choices=Type.choices, default=Type.CHAT_LIBRE)
    personas = models.ManyToManyField(Persona, blank=True, related_name='conversations')
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Message(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'
        PERSONA = 'persona', 'Persona'

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=Role.choices)
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.role}] {self.content[:60]}'


class Source(models.Model):
    class Type(models.TextChoices):
        CSV = 'csv', 'CSV'
        EXCEL = 'excel', 'Excel'
        PDF = 'pdf', 'PDF'
        URL = 'url', 'URL'
        JIRA = 'jira', 'Jira'
        ZENDESK = 'zendesk', 'Zendesk'
        NOTION = 'notion', 'Notion'
        GDRIVE = 'gdrive', 'Google Drive'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        READY = 'ready', 'Ready'
        FAILED = 'failed', 'Failed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sources')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=Type.choices)
    file_path = models.CharField(max_length=2048, blank=True, null=True)
    url = models.URLField(max_length=2048, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.type})'


class Insight(models.Model):
    class Type(models.TextChoices):
        IRRITANT = 'irritant', 'Irritant'
        OPPORTUNITY = 'opportunity', 'Opportunité'
        USE_CASE = 'use_case', "Cas d'usage"
        VERBATIM = 'verbatim', 'Verbatim'

    class Impact(models.TextChoices):
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='insights')
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True, related_name='insights')
    type = models.CharField(max_length=20, choices=Type.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    impact = models.CharField(max_length=10, choices=Impact.choices, default=Impact.MEDIUM)
    mentions = models.IntegerField(default=0)
    source_references = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-mentions', '-created_at']

    def __str__(self):
        return f'[{self.type}] {self.title}'
