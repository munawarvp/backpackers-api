# Generated by Django 4.2 on 2023-04-16 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resorts", "0011_destinations"),
    ]

    operations = [
        migrations.AddField(
            model_name="destinations",
            name="location",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
