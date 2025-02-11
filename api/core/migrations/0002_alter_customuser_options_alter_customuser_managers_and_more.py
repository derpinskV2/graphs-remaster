# Generated by Django 5.1.4 on 2025-01-05 00:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"ordering": ["created_at"], "verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AlterModelManagers(
            name="customuser",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="username",
        ),
        migrations.AddField(
            model_name="customuser",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_visible",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="role",
            field=models.CharField(choices=[("admin", "Admin"), ("user", "User")], default="user", max_length=10),
        ),
        migrations.AddField(
            model_name="customuser",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="date_joined",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date joined"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(blank=True, max_length=70, verbose_name="First name"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="is active"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(blank=True, max_length=70, verbose_name="Last name"),
        ),
        migrations.AddIndex(
            model_name="customuser",
            index=models.Index(fields=["email"], name="core_custom_email_a5d01e_idx"),
        ),
        migrations.AddIndex(
            model_name="customuser",
            index=models.Index(fields=["role"], name="core_custom_role_77f64b_idx"),
        ),
    ]
