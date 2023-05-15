# Generated by Django 4.2 on 2023-05-02 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resorts", "0017_resorts_is_rejected"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResortReviews",
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
                ("review_heading", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("rating", models.FloatField()),
                ("created_date", models.DateTimeField(auto_now=True)),
                (
                    "resort",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resorts.resorts",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResortBooking",
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
                ("booking_id", models.CharField(max_length=20)),
                ("check_in", models.DateField()),
                ("check_out", models.DateField()),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("phone_number", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("address", models.TextField()),
                ("booking_total", models.FloatField()),
                ("payment_method", models.CharField(max_length=30)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Checked In", "Checked In"),
                            ("Checked Out", "Checked Out"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="New",
                        max_length=20,
                    ),
                ),
                ("occupancy", models.IntegerField()),
                ("booking_date", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "booked_resort",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resorts.resorts",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdventureReviews",
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
                ("review_heading", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("rating", models.FloatField()),
                ("created_date", models.DateTimeField(auto_now=True)),
                (
                    "adventure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resorts.adventures",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdventureBooking",
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
                ("booking_id", models.CharField(max_length=20)),
                ("first_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("address", models.TextField()),
                ("age", models.IntegerField()),
                ("activity_date", models.DateField()),
                ("phone_number", models.CharField(max_length=15)),
                ("weight", models.IntegerField()),
                ("guardian_name", models.CharField(max_length=50)),
                ("guardian_phone", models.CharField(max_length=50)),
                ("booking_total", models.FloatField()),
                ("medical_condition", models.BooleanField(default=False)),
                ("payment_method", models.CharField(max_length=30)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Checked In", "Checked In"),
                            ("Checked Out", "Checked Out"),
                            ("Pending", "Pending"),
                        ],
                        default="New",
                        max_length=20,
                    ),
                ),
                ("booking_date", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "booked_activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resorts.adventures",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
