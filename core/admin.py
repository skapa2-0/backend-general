from django.contrib import admin

from core.models import Organisation, Project, UserProfile


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'clerk_org_id', 'created_at']
    search_fields = ['name', 'slug', 'clerk_org_id']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'organisation', 'role', 'created_at']
    list_filter = ['role', 'organisation']
    search_fields = ['name', 'email', 'clerk_user_id']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'organisation', 'created_by', 'created_at']
    list_filter = ['organisation']
    search_fields = ['name', 'description']
