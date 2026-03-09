from django.contrib import admin

from coachpm.models import CoachSession, PMRecommendation


class PMRecommendationInline(admin.TabularInline):
    model = PMRecommendation
    extra = 0


@admin.register(CoachSession)
class CoachSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'project', 'created_by', 'created_at']
    search_fields = ['title', 'topic']
    inlines = [PMRecommendationInline]


@admin.register(PMRecommendation)
class PMRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'session', 'created_at']
    list_filter = ['priority', 'category']
    search_fields = ['title', 'description']
