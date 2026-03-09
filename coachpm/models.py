from django.db import models

from core.models import Project, UserProfile


class CoachSession(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='coach_sessions')
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, blank=True)
    messages = models.JSONField(default=list)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='coach_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PMRecommendation(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    session = models.ForeignKey(CoachSession, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', '-created_at']

    def __str__(self):
        return self.title
