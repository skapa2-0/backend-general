from django.db import models

from core.models import Project, UserProfile


class FieldStudy(models.Model):
    class Methodology(models.TextChoices):
        INTERVIEW = 'interview', 'Interview'
        SURVEY = 'survey', 'Survey'
        OBSERVATION = 'observation', 'Observation'
        DIARY = 'diary', 'Diary'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        ARCHIVED = 'archived', 'Archived'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='field_studies')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    methodology = models.CharField(max_length=20, choices=Methodology.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    participants_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='field_studies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Field studies'

    def __str__(self):
        return f'{self.name} ({self.methodology})'


class FieldObservation(models.Model):
    class Sentiment(models.TextChoices):
        POSITIVE = 'positive', 'Positive'
        NEGATIVE = 'negative', 'Negative'
        NEUTRAL = 'neutral', 'Neutral'

    study = models.ForeignKey(FieldStudy, on_delete=models.CASCADE, related_name='observations')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    sentiment = models.CharField(max_length=10, choices=Sentiment.choices, default=Sentiment.NEUTRAL)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.sentiment}] {self.title}'
