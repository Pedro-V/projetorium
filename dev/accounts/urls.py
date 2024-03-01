from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("cadastro/aluno", CadastrarAluno.as_view(), name="cadastrar_aluno"),
    path("cadastro/professor", CadastrarProfessor.as_view(), name="cadastrar_professor"),
]