from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'bank', 'branch')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_type', 'bank', 'branch')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'bank', 'branch')}),
    )