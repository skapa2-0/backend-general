from django.contrib import admin

from epersona.models import Conversation, Insight, Message, Persona, Source


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'project', 'is_active', 'created_at']
    list_filter = ['is_active', 'project']
    search_fields = ['name', 'role']


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'project', 'created_by', 'created_at']
    list_filter = ['type']
    search_fields = ['title']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['role', 'persona', 'conversation', 'created_at']
    list_filter = ['role']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'status', 'project', 'created_at']
    list_filter = ['type', 'status']
    search_fields = ['name']


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'impact', 'mentions', 'project', 'created_at']
    list_filter = ['type', 'impact']
    search_fields = ['title', 'description']
