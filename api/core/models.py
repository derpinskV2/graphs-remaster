from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from core.querysets import UserQuerySet


class CustomModel(models.Model):
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def active_users(self):
        return self.get_queryset().active_users()

    def inactive_users(self):
        return self.get_queryset().inactive_users()

    def admins(self):
        return self.get_queryset().admins()

    def last_login_24_hours(self):
        return self.get_queryset().last_login_24_hours()

    def last_login_7_days(self):
        return self.get_queryset().last_login_7_days()

    def last_login_30_days(self):
        return self.get_queryset().last_login_30_days()

    def create_user(self, email, password=None, **kwargs):
        if not email or not kwargs.get("role"):
            raise ValueError("Email and Role is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")
        user = self.create_user(email, password, **extra_fields)
        user.save()

        return user


class CustomUser(CustomModel, AbstractUser):
    ADMIN = "admin"
    USER = "user"
    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (USER, "User"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)

    username = None
    first_name = models.CharField("First name", max_length=70, blank=True)
    last_name = models.CharField("Last name", max_length=70, blank=True)
    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField("is active", default=False)
    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]
