# Generated by Django 4.2.5 on 2024-03-04 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('matricula', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10)),
                ('nome', models.CharField(max_length=100)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membros', models.ManyToManyField(to='app.aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('matricula', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
                ('departamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.departamento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('descricao', models.CharField(max_length=800)),
                ('data_criacao', models.DateField(auto_now_add=True)),
                ('tags', models.CharField(default='', max_length=800)),
                ('publico', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('CO', 'Concluido'), ('CA', 'Cancelado'), ('SU', 'Suspenso'), ('EP', 'Em progresso')], default='EP', max_length=2)),
                ('grupo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=12)),
                ('ano', models.IntegerField(default=2024)),
                ('periodo', models.IntegerField(default=1)),
                ('alunos', models.ManyToManyField(to='app.aluno')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.disciplina')),
                ('professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Proposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('descricao', models.CharField(max_length=800)),
                ('tags', models.CharField(default='', max_length=800)),
                ('data_proposta', models.DateField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.aluno')),
                ('projeto_promovido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.projeto')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.turma')),
            ],
        ),
        migrations.AddField(
            model_name='projeto',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.turma'),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.CharField(max_length=800)),
                ('aprovado', models.BooleanField(default=False)),
                ('proposta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.proposta')),
            ],
        ),
        migrations.AddField(
            model_name='aluno',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.curso'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.UniqueConstraint(fields=('codigo', 'disciplina', 'ano', 'periodo'), name='unique_turma'),
        ),
        migrations.AddConstraint(
            model_name='disciplina',
            constraint=models.UniqueConstraint(fields=('codigo', 'departamento'), name='unique_disciplina'),
        ),
    ]
