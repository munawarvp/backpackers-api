# Generated by Django 4.2 on 2023-05-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0004_coupon_couponassign"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="expiration_date",
            field=models.DateField(),
        ),
    ]