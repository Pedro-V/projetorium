from django.urls import path, include
from . import views

urlpatterns = [
    path("perfil/", views.perfil, name='perfil'),
    path('cadastro/', views.cadastro_aluno, name='cadastro_aluno'),
    path('turmas/', views.turmas, name='turmas'),
    path('turma/<int:id_turma>/', views.turma_detalhe, name='detalhe_turma'),
    path('turma/<int:id_turma>/escolher_projeto', views.escolher_projeto, name='escolher_projeto'),
    path('turma/<int:id_turma>/propor_projeto', views.propor_projeto, name='propor_projeto'),
    path('consulta_projeto/', views.consulta_projeto, name='consulta_projeto'),
    path('proposta/', views.avaliar_proposta, name='avaliar_proposta'),
    path('cadastrar_turma', views.cadastrar_turma, name='cadastrar_turma'),
    path('propostas/', views.propostas, name='propostas'),
    path('projetos/', views.projetos, name='projetos'),
]
