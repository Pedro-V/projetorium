from django.urls import path, include
from app.views import *

urlpatterns = [
    path("perfil/", perfil, name='perfil'),
    path('cadastro_aluno_turma/', CadastroAlunoTurma.as_view(), name='cadastro_aluno_turma'),
    path('cadastro_turma', CadastroTurma.as_view(), name='cadastro_turma'),
    path('turmas/', ListaTurmas.as_view(), name='turmas'),
    path('turma/<int:id_turma>/', DetalheTurma.as_view(), name='detalhe_turma'),
    path('turma/<int:id_turma>/escolher_projeto', escolher_projeto, name='escolher_projeto'),
    path('turma/<int:id_turma>/propor_projeto', ProporProjeto.as_view(), name='propor_projeto'),
    path('turma/<int:id_turma>/propostas', ListarPropostas.as_view(), name='propostas'),
    path('turma/<int:id_turma>/propostas/<int:id_proposta>', DetalheProposta.as_view(), name='detalhe_proposta'),
    path('consulta/', ConsultaProjeto.as_view(), name='consulta_projeto'),
    path('consulta/?nome=<str:nome>', ResultadoProjeto.as_view(), name='resultado_projeto'),
    path('projetos/', projetos, name='projetos'),
]
