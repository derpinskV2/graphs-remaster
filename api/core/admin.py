from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_login",
        "is_visible",
        "role",
        "email",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "last_login",
        "is_superuser",
        "is_staff",
        "is_visible",
        "created_at",
        "updated_at",
        "is_active",
        "date_joined",
    )
    raw_id_fields = ("groups", "user_permissions")
    date_hierarchy = "created_at"
