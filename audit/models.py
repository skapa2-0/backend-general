from django.db import models

from core.models import Project, UserProfile


class Audit(models.Model):
    class SourceType(models.TextChoices):
        URL = 'url', 'URL'
        GITLAB = 'gitlab', 'GitLab'
        UPLOAD = 'upload', 'Upload'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RUNNING = 'running', 'Running'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='audits')
    name = models.CharField(max_length=255)
    source_url = models.URLField(max_length=2048, blank=True)
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.URL)
    audit_types = models.JSONField(default=list, help_text='List of audit types: rgaa, ux, eco, toneofvoice')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    score_global = models.FloatField(null=True, blank=True)
    score_ux = models.FloatField(null=True, blank=True)
    score_rgaa = models.FloatField(null=True, blank=True)
    score_eco = models.FloatField(null=True, blank=True)
    score_designsys = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='audits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.status})'


class AuditCritere(models.Model):
    class Type(models.TextChoices):
        BASTIEN_SCAPIN = 'bastien_scapin', 'Bastien & Scapin'
        RGAA = 'rgaa', 'RGAA'
        ECO = 'eco', 'Éco-conception'

    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='criteres')
    type = models.CharField(max_length=20, choices=Type.choices)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    score = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    ecrans_impactes = models.IntegerField(default=0)
    processus_impactes = models.IntegerField(default=0)
    recommendations_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['type', 'code']

    def __str__(self):
        return f'{self.code} - {self.name}'


class AuditHeuristique(models.Model):
    critere = models.ForeignKey(AuditCritere, on_delete=models.CASCADE, related_name='heuristiques')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    score = models.FloatField(null=True, blank=True)
    definition = models.TextField(blank=True)
    patterns_detectes = models.JSONField(default=list)
    ecrans_concernes = models.JSONField(default=list)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code} - {self.name}'


class AuditEcran(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='ecrans')
    path = models.CharField(max_length=2048)
    name = models.CharField(max_length=255)
    score = models.FloatField(null=True, blank=True)
    issues = models.JSONField(default=list)
    composants = models.JSONField(default=list)
    viewer_annotations = models.JSONField(default=list)

    class Meta:
        ordering = ['path']

    def __str__(self):
        return self.name


class AuditProcessus(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='processus')
    name = models.CharField(max_length=255)
    score = models.FloatField(null=True, blank=True)
    etapes = models.JSONField(default=list)
    problemes = models.JSONField(default=list)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Audit processus'

    def __str__(self):
        return self.name


class AuditRecommandation(models.Model):
    class Type(models.TextChoices):
        UX = 'ux', 'UX'
        RGAA = 'rgaa', 'RGAA'
        ECO = 'eco', 'Éco-conception'
        DESIGNSYS = 'designsys', 'Design System'

    class Priority(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    class Effort(models.TextChoices):
        XS = 'xs', 'XS'
        S = 's', 'S'
        M = 'm', 'M'
        L = 'l', 'L'
        XL = 'xl', 'XL'

    class RecoStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'
        DISMISSED = 'dismissed', 'Dismissed'

    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='recommandations')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    effort = models.CharField(max_length=5, choices=Effort.choices, default=Effort.M)
    gain_estime = models.FloatField(null=True, blank=True)
    critere = models.ForeignKey(AuditCritere, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommandations')
    ecran = models.ForeignKey(AuditEcran, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommandations')
    jira_ticket_url = models.URLField(max_length=2048, blank=True, null=True)
    status = models.CharField(max_length=20, choices=RecoStatus.choices, default=RecoStatus.OPEN)

    class Meta:
        ordering = ['priority', 'type']

    def __str__(self):
        return f'[{self.priority}] {self.title}'


class AuditComposant(models.Model):
    class Severity(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        MAJOR = 'major', 'Major'
        MINOR = 'minor', 'Minor'

    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='composants')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True)
    occurrences = models.IntegerField(default=0)
    problemes = models.JSONField(default=list)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MINOR)

    class Meta:
        ordering = ['severity', 'name']

    def __str__(self):
        return f'{self.name} ({self.severity})'


class AuditMaturity(models.Model):
    audit = models.OneToOneField(Audit, on_delete=models.CASCADE, related_name='maturity')
    ux_level = models.IntegerField(default=1)
    rgaa_level = models.IntegerField(default=1)
    eco_level = models.IntegerField(default=1)
    designsys_level = models.IntegerField(default=1)
    roadmap = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = 'Audit maturities'

    def __str__(self):
        return f'Maturity for {self.audit.name}'
