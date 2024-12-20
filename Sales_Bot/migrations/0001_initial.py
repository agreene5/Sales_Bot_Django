# Generated by Django 5.1.4 on 2024-12-19 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Preference",
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
                ("items_likes", models.CharField(max_length=1000)),
                ("items_dislikes", models.CharField(max_length=1000)),
            ],
        ),
    ]