# Generated by Django 4.2.7 on 2024-03-02 23:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_rename_alunos_grupo_membros_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projeto",
            name="tags",
            field=models.CharField(default="", max_length=800),
        ),
        migrations.AlterField(
            model_name="proposta",
            name="tags",
            field=models.CharField(default="", max_length=800),
        ),
    ]
