from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class CustomUserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone", "role", "profile_image")},
        ),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "first_name", "role", "password1", "password2"),
        },
    )

    search_fields = ["first_name", "last_name", "email", "role"]
    list_display = [
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
        "date_joined",
    ]
    list_filter = ["role", "is_active"]
    ordering = ["email"]


admin.site.register(User, CustomUserAdmin)
