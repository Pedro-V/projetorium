from django.contrib import admin
from .models import Aluno, Professor, Departamento, Disciplina

admin.site.register([Aluno, Professor, Departamento, Disciplina])
