from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DataSharingConsent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "display_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "username", "display_name")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "display_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password", "password2"),
            },
        ),
    )


@admin.register(DataSharingConsent)
class DataSharingConsentAdmin(admin.ModelAdmin):
    list_display = ("user", "consent_version", "enabled", "changed_at")
    list_filter = ("enabled", "consent_version")
    search_fields = ("user__email", "user__username")
