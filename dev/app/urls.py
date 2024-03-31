from django.urls import path, include
from app.views import *

urlpatterns = [
    path("perfil/", perfil, name='perfil'),
    path('cadastro_turma', CadastroTurma.as_view(), name='cadastro_turma'),
    path('turmas/', ListaTurmas.as_view(), name='turmas'),
    path('turma/<int:id_turma>/', DetalheTurma.as_view(), name='detalhe_turma'),
    path('turma/<int:id_turma>/escolher_projeto', EscolherProjeto.as_view(), name='escolher_projeto'),
    path('turma/<int:id_turma>/propor_projeto', ProporProjeto.as_view(), name='propor_projeto'),
    path('turma/<int:id_turma>/propostas', ListarPropostas.as_view(), name='propostas'),
    path('turma/<int:id_turma>/propostas/<int:id_proposta>', DetalheProposta.as_view(), name='detalhe_proposta'),
    path('turma/<int:id_turma>/participantes', ParticipantesTurma.as_view(), name='participantes_turma'),
    path('turma/<int:id_turma>/ofertar_projeto', OfertarProjeto.as_view(), name='ofertar_projeto'),
    path('turma/<int:id_turma>/addicionar_aluno/', AdicionarAluno.as_view(), name='adicionar_aluno'),
    path('consulta/', ConsultaProjeto.as_view(), name='consulta_projeto'),
    path('consulta/?nome=<str:nome>&tag=<str:tag>&turma=<str:turma>&data=<str:data>', ResultadoProjeto.as_view(), name='resultado_projeto'),
    path('projetos/', ListarProjetos.as_view(), name='projetos'),
    path('projeto/<int:id_proj>/', ProjetoDetalhe.as_view(), name='projeto'),
    path('projeto/<int:id_proj>/adicionar_membro', AdicionarMembro.as_view(), name='adicionar_membro'),
    path('projeto/<int:id_proj>/editar', EditarProjeto.as_view(), name='editar_projeto'),
]
