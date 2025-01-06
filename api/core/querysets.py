from datetime import timedelta

from django.db import models
from django.utils import timezone


class UserQuerySet(models.QuerySet):
    def _search(self, *args, **kwargs):
        raise NotImplementedError

    def visible(self):
        return self.filter(is_visible=True)

    def active_users(self):
        return self.filter(is_active=True)

    def inactive_users(self):
        return self.filter(is_active=False)

    def admins(self):
        return self.filter(role="admin")

    def last_login_24_hours(self):
        return self.filter(last_login__gte=timezone.now() - timedelta(days=1))

    def last_login_7_days(self):
        return self.filter(last_login__gte=timezone.now() - timedelta(days=7))

    def last_login_30_days(self):
        return self.filter(last_login__gte=timezone.now() - timedelta(days=30))
