# Generated by Django 5.1.4 on 2025-01-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0005_csvfile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="csvdata",
            name="bg",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
