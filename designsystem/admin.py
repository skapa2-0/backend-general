from django.contrib import admin

from designsystem.models import DesignSystemAudit, DSComponent


class DSComponentInline(admin.TabularInline):
    model = DSComponent
    extra = 0


@admin.register(DesignSystemAudit)
class DesignSystemAuditAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'score', 'components_analyzed', 'issues_found', 'created_at']
    list_filter = ['status']
    search_fields = ['name']
    inlines = [DSComponentInline]


@admin.register(DSComponent)
class DSComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'status', 'audit']
    list_filter = ['status']
    search_fields = ['name']
