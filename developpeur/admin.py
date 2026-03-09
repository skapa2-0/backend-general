from django.contrib import admin

from developpeur.models import CodeGeneration, CodeIssue, CodeProject, PageConfig


class PageConfigInline(admin.TabularInline):
    model = PageConfig
    extra = 0


@admin.register(CodeProject)
class CodeProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'created_by', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'description']
    inlines = [PageConfigInline]


@admin.register(PageConfig)
class PageConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'code_project', 'order']
    search_fields = ['name', 'path']


@admin.register(CodeGeneration)
class CodeGenerationAdmin(admin.ModelAdmin):
    list_display = ['file_path', 'language', 'status', 'code_project', 'created_at']
    list_filter = ['status', 'language']
    search_fields = ['file_path']


@admin.register(CodeIssue)
class CodeIssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'status', 'assigned_group', 'code_project', 'created_at']
    list_filter = ['type', 'status', 'assigned_group']
    search_fields = ['title', 'description']
