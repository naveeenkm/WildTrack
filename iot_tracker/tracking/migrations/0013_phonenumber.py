# Generated by Django 5.1.2 on 2024-12-03 08:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracking", "0012_delete_animalposition"),
    ]

    operations = [
        migrations.CreateModel(
            name="PhoneNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=15,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
            ],
        ),
    ]
