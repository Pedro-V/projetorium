# Generated by Django 4.2.7 on 2024-03-31 22:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="projeto",
            name="versao",
            field=models.CharField(default="", max_length=20),
        ),
    ]
