# Generated by Django 4.1.5 on 2023-01-14 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cars", "0005_alter_car_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="owner",
            field=models.ForeignKey(
                default=42,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
