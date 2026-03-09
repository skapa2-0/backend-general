from django.contrib import admin

from audit.models import (
    Audit,
    AuditComposant,
    AuditCritere,
    AuditEcran,
    AuditHeuristique,
    AuditMaturity,
    AuditProcessus,
    AuditRecommandation,
)


class AuditCritereInline(admin.TabularInline):
    model = AuditCritere
    extra = 0


class AuditEcranInline(admin.TabularInline):
    model = AuditEcran
    extra = 0


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'score_global', 'created_at']
    list_filter = ['status', 'source_type']
    search_fields = ['name']
    inlines = [AuditCritereInline, AuditEcranInline]


@admin.register(AuditCritere)
class AuditCritereAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'type', 'score', 'audit']
    list_filter = ['type']
    search_fields = ['name', 'code']


@admin.register(AuditHeuristique)
class AuditHeuristiqueAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'score', 'critere']
    search_fields = ['name', 'code']


@admin.register(AuditEcran)
class AuditEcranAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'score', 'audit']
    search_fields = ['name', 'path']


@admin.register(AuditProcessus)
class AuditProcessusAdmin(admin.ModelAdmin):
    list_display = ['name', 'score', 'audit']
    search_fields = ['name']


@admin.register(AuditRecommandation)
class AuditRecommandationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'priority', 'effort', 'status', 'audit']
    list_filter = ['type', 'priority', 'status']
    search_fields = ['title', 'description']


@admin.register(AuditComposant)
class AuditComposantAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'severity', 'occurrences', 'audit']
    list_filter = ['severity']
    search_fields = ['name']


@admin.register(AuditMaturity)
class AuditMaturityAdmin(admin.ModelAdmin):
    list_display = ['audit', 'ux_level', 'rgaa_level', 'eco_level', 'designsys_level']
