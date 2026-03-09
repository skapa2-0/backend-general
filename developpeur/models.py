from django.db import models

from core.models import Project, UserProfile


class CodeProject(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        GENERATING = 'generating', 'Generating'
        REVIEW = 'review', 'Review'
        DEPLOYED = 'deployed', 'Deployed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='code_projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tech_stack = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='code_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class PageConfig(models.Model):
    code_project = models.ForeignKey(CodeProject, on_delete=models.CASCADE, related_name='pages')
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=2048)
    description = models.TextField(blank=True)
    components = models.JSONField(default=list)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} ({self.path})'


class CodeGeneration(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        GENERATED = 'generated', 'Generated'
        VALIDATED = 'validated', 'Validated'
        REJECTED = 'rejected', 'Rejected'

    code_project = models.ForeignKey(CodeProject, on_delete=models.CASCADE, related_name='generations')
    page = models.ForeignKey(PageConfig, on_delete=models.SET_NULL, null=True, blank=True, related_name='generations')
    file_path = models.CharField(max_length=2048)
    content = models.TextField()
    language = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    validated_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_generations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['file_path']

    def __str__(self):
        return f'{self.file_path} ({self.status})'


class CodeIssue(models.Model):
    class Type(models.TextChoices):
        BUG = 'bug', 'Bug'
        FEATURE = 'feature', 'Feature'
        IMPROVEMENT = 'improvement', 'Improvement'

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'

    class AssignedGroup(models.TextChoices):
        OBSERVER = 'observer', 'Observer'
        DEVELOPER = 'developer', 'Developer'
        VALIDATOR = 'validator', 'Validator'

    code_project = models.ForeignKey(CodeProject, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    assigned_group = models.CharField(max_length=20, choices=AssignedGroup.choices, default=AssignedGroup.DEVELOPER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.type}] {self.title}'
