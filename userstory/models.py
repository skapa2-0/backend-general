from django.db import models

from core.models import Project, UserProfile


class UserStory(models.Model):
    class Priority(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        READY = 'ready', 'Ready'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='user_stories')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    as_a = models.CharField(max_length=255, blank=True)
    i_want = models.TextField(blank=True)
    so_that = models.TextField(blank=True)
    acceptance_criteria = models.JSONField(default=list)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    story_points = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='user_stories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', '-created_at']
        verbose_name_plural = 'User stories'

    def __str__(self):
        return self.title


class Epic(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='epics')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user_stories = models.ManyToManyField(UserStory, blank=True, related_name='epics')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
