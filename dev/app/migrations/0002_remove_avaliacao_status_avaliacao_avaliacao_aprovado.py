# Generated by Django 4.2.7 on 2024-03-02 22:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="avaliacao",
            name="status_avaliacao",
        ),
        migrations.AddField(
            model_name="avaliacao",
            name="aprovado",
            field=models.BooleanField(default=False),
        ),
    ]