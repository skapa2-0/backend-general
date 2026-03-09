from django.contrib import admin

from analyseterrain.models import FieldObservation, FieldStudy


class FieldObservationInline(admin.TabularInline):
    model = FieldObservation
    extra = 0


@admin.register(FieldStudy)
class FieldStudyAdmin(admin.ModelAdmin):
    list_display = ['name', 'methodology', 'status', 'participants_count', 'project', 'created_at']
    list_filter = ['methodology', 'status']
    search_fields = ['name', 'description']
    inlines = [FieldObservationInline]


@admin.register(FieldObservation)
class FieldObservationAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'sentiment', 'study', 'created_at']
    list_filter = ['sentiment', 'category']
    search_fields = ['title', 'description']
