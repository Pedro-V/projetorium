from django.urls import path, include
from django.views.generic import RedirectView

from accounts.views import *

urlpatterns = [
    path("", RedirectView.as_view(url='login/')),
    path("", include('django.contrib.auth.urls')),
    path("cadastro/aluno", CadastrarAluno.as_view(), name="cadastrar_aluno"),
    path("cadastro/professor", CadastrarProfessor.as_view(), name="cadastrar_professor"),
]
