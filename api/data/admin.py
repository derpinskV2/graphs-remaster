from django.contrib import admin

from .models import CSVFile, CSVData


@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_visible",
        "created_at",
        "updated_at",
        "file",
        "processed",
        "processed_at",
    )
    list_filter = (
        "is_visible",
        "created_at",
        "updated_at",
        "processed",
        "processed_at",
    )
    date_hierarchy = "created_at"


@admin.register(CSVData)
class CSVDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "bg",
        "bg_input",
        "carb_input",
        "insulin_delivered",
        "total_insulin",
        "bolus",
        "event",
        "serial_number",
    )
    list_filter = ("is_visible", "created_at", "updated_at", "serial_number", "user")
    date_hierarchy = "created_at"
