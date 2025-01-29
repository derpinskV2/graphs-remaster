from core.models import CustomModel
from django.db import models


class Event(CustomModel):
    pass


class Log(models.Model):
    user = models.ForeignKey(
        "core.CustomUser", on_delete=models.CASCADE, blank=True, null=True, verbose_name="user", editable=False
    )
    request_data = models.JSONField("request_data", null=True, editable=False)
    response_data = models.JSONField("response_data", null=True, editable=False)

    user_agent = models.CharField("user_agent", max_length=255, blank=True, editable=False)
    ip_address = models.GenericIPAddressField("ip_address", editable=False)
    path = models.CharField("path", max_length=255, blank=True, editable=False)
    status_code = models.PositiveIntegerField("status_code", editable=False)
    http_method = models.CharField("http_method", max_length=10, blank=True, editable=False)
    query_params = models.JSONField("query_params", null=True, editable=False)
    timestamp = models.DateTimeField("timestamp", auto_now_add=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ["-timestamp"]

    def __str__(self):
        return self.path
