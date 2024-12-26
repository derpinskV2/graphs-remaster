from django.db import models

from core.models import CustomModel


class CSVFile(CustomModel):
    file = models.FileField(upload_to="csv_files")
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file.name


class CSVData(CustomModel):
    bg = models.FloatField()
    bg_input = models.FloatField(blank=True, null=True)
    carb_input = models.FloatField(blank=True, null=True)
    insulin_delivered = models.FloatField(blank=True, null=True)
    total_insulin = models.FloatField(blank=True, null=True)

    bolus = models.FloatField(blank=True, null=True)
    event = models.CharField(max_length=255, blank=True, null=True)

    serial_number = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "CSV Data"
