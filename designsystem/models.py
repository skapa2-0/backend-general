from django.db import models

from core.models import Project


class DesignSystemAudit(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RUNNING = 'running', 'Running'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ds_audits')
    name = models.CharField(max_length=255)
    source_url = models.URLField(max_length=2048, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    score = models.FloatField(null=True, blank=True)
    components_analyzed = models.IntegerField(default=0)
    issues_found = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.status})'


class DSComponent(models.Model):
    class Status(models.TextChoices):
        COMPLIANT = 'compliant', 'Compliant'
        NON_COMPLIANT = 'non_compliant', 'Non-compliant'
        MISSING = 'missing', 'Missing'

    audit = models.ForeignKey(DesignSystemAudit, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMPLIANT)
    issues = models.JSONField(default=list)

    class Meta:
        ordering = ['status', 'name']

    def __str__(self):
        return f'{self.name} ({self.status})'
