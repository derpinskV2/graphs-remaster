from django.contrib import admin

from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "request_data",
        "response_data",
        "user_agent",
        "ip_address",
        "path",
        "status_code",
        "http_method",
        "query_params",
        "timestamp",
    )
    list_filter = ("user", "timestamp")
