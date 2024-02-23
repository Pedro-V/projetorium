from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("perfil/", views.perfil, name='perfil'),
    path('cadastro/', views.cadastro_aluno, name='cadastro_aluno'),
    path('turmas/', views.turmas, name='turmas'),
    path('consulta_projeto/', views.consulta_projeto, name='consulta_projeto'),
    path('proposta/', views.avaliar_proposta, name='avaliar_proposta'),
    path('cadastrar_turma', views.cadastrar_turma, name='cadastrar_turma'),
    path('propostas/', views.propostas, name='propostas'),
]