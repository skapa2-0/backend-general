from django.contrib import admin

from userstory.models import Epic, UserStory


@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'story_points', 'project', 'created_at']
    list_filter = ['priority', 'status']
    search_fields = ['title', 'description']


@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['user_stories']
