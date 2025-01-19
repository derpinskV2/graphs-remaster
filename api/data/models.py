from django.db import models

from core.models import CustomModel


class CSVFile(CustomModel):
    user = models.ForeignKey("core.CustomUser", on_delete=models.CASCADE)
    file = models.FileField(upload_to="csv_files")
    processed = models.BooleanField(default=False)
    file_hash = models.CharField(max_length=64)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file.name

    class Meta:
        unique_together = ("user", "file_hash")


class CSVData(CustomModel):
    csv_file = models.ForeignKey("data.CSVFile", on_delete=models.CASCADE)
    user = models.ForeignKey("core.CustomUser", on_delete=models.CASCADE)
    bg = models.FloatField(blank=True, null=True)
    bg_input = models.FloatField(blank=True, null=True)
    carb_input = models.FloatField(blank=True, null=True)
    carb_ratio = models.FloatField(blank=True, null=True)
    insulin_delivered = models.FloatField(blank=True, null=True)
    total_insulin = models.FloatField(blank=True, null=True)
    total_basal = models.FloatField(blank=True, null=True)
    bolus = models.FloatField(blank=True, null=True)
    event = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "CSV Data"
