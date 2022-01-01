from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from user.models import User


class UserAdmin(BaseUserAdmin):
    """Admin class for user"""
    model = User
    ordering = ("-joined_on",)
    list_filter = ("email", "is_active", "user_type")
    list_display = ("id", "email", "first_name", "last_name", "user_type", "is_active", "joined_on")
    search_fields = ("email", "user_type", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        ("Personal info", {"fields": ("user_type", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_superuser",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "user_type", "password"),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# admin.site.register(models.UserProfile)
