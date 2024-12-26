# Generated by Django 5.1.4 on 2024-12-26 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sales_Bot", "0004_user_input"),
    ]

    operations = [
        migrations.CreateModel(
            name="Checkout",
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
                ("time_shopping", models.FloatField()),
                ("items_bought", models.IntegerField()),
                ("money_spent", models.IntegerField()),
            ],
        ),
    ]