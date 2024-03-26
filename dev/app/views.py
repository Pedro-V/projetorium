from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from accounts.decorators import student_required, teacher_required
from django.utils.decorators import method_decorator

from app.signals import *
from app.models import *


def get_user(user, template_name=None):
    """
    Retorna o objeto que especifica o papel de user, e a versão específica 
    Nesse caso, o objeto será um Professor ou Aluno.
    """
    UserClass = Professor if user.is_teacher else Aluno
    specific_user = UserClass.objects.get(user=user)
    class_name = UserClass.__name__.lower()
    if template_name:
        return (specific_user, f'{class_name}/{template_name}')
    else:
        return specific_user

    
@login_required
def perfil(request):
    if request.method == 'GET':
        user, template_name = get_user(request.user, 'perfil.html')
        return render(request, template_name, { 'usuario': user })

class ConsultaProjeto(View):
    template_name = 'consulta_projeto.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        nome_filtro = request.POST['nome_proj']
        return redirect('resultado_projeto', nome=nome_filtro)

class ResultadoProjeto(View):
    template_name = 'resultado_projeto.html'

    def get(self, request, nome):
        projetos = Projeto.objects.filter(titulo__icontains=nome)
        return render(request, self.template_name, {'projetos': projetos})

class ListaTurmas(View):
    template_name = 'turmas.html'

    def get(self, request):
        user = get_user(request.user)
        return render(request, self.template_name, { 'turmas': user.turmas() })


class DetalheTurma(View):
    def get(self, request, id_turma):
        _, template_name = get_user(request.user, 'turma.html')
        turma = Turma.objects.get(id=id_turma)
        return render(request, template_name, { 'turma': turma })


class CadastroAlunoTurma(View):
    """
    Um professor cadastra um aluno numa turma.
    """
    template_name = 'professor/cad_aluno.html'

    def get(self, request):
        prof = get_user(request.user)
        turmas = prof.turmas();
        alunos = Aluno.objects.all()

        context = {
            "turmas": turmas,
            "alunos": alunos,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        id_turma = request.POST['turma']
        matricula = request.POST['aluno']

        turma = Turma.objects.get(id=id_turma)
        aluno = Aluno.objects.get(matricula=matricula)

        turma.alunos.add(aluno)

        return redirect('cadastro_aluno_turma')


class CadastroTurma(View):
    """
    Um professor cadastra uma nova turma.
    """
    template_name = 'professor/cad_turma.html'

    def get(self, request, error_msg=None):
        disciplinas = Disciplina.objects.all()
        context = {
            "disciplinas": disciplinas,
            "error_msg": error_msg,
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        prof = get_user(request.user)
        disc = Disciplina.objects.get(pk=request.POST['disciplina'])

        try:
            Turma.objects.create(
                disciplina=disc,
                professor=prof,
                ano=request.POST['ano'],
                periodo=request.POST['periodo'],
                codigo=request.POST['codigo'],
            )
        except IntegrityError:
            return self.get(request, "Uma turma com esses dados já existe!")

        return redirect('cadastro_turma')


class OfertarProjeto(View):
    """
    Um professor oferta projetos a uma turma específica
    """
    template_name = 'professor/ofertar_projeto.html'

    def get(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        return render(request, self.template_name)
    
    def post(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        Projeto.objects.create(
            titulo=request.POST['titulo'],
            descricao=request.POST['descricao'],
            tags=request.POST['tags'],
            turma=turma,
        )

        return redirect('ofertar_projeto', id_turma)


class ListarPropostas(View):
    template_name = 'professor/propostas.html'

    def get(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        propostas = Proposta.objects.filter(turma=turma)

        context = {
            "propostas": propostas,
            "id_turma": id_turma,
        }
        
        return render(request, self.template_name, context)


class DetalheProposta(View):
    template_name = 'detalhe_proposta.html'
    
    def get(self, request, id_turma, id_proposta):
        proposta = Proposta.objects.get(pk=id_proposta)
        avaliacao = proposta.avaliacao if hasattr(proposta, 'avaliacao') else None

        context = {
            'proposta': proposta,
            'avaliacao': avaliacao,
        }

        return render(request, self.template_name, context)

    def post(self, request, id_turma, id_proposta):
        proposta = Proposta.objects.get(pk=id_proposta)

        avaliacao = Avaliacao.objects.create(
            proposta=proposta,
            aprovado=bool(request.POST['aprovado']),
            mensagem=request.POST['mensagem'],
        )

        if avaliacao.aprovado:
            proposta.promover()

        return redirect('detalhe_proposta', id_turma, id_proposta)

class Escolher_projeto(View):
    template_name = 'aluno/escolher_projeto.html'

    def get(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        projetos = Projeto.objects.filter(turma=turma)
        return render(request, self.template_name, {'projetos': projetos, 'turma': turma })

class Escolher_membros_grupo(View):
    template_name = 'aluno/escolher_membros_grupo.html'

    def get(self, request, id_turma, id_projeto):
        turma = Turma.objects.get(pk=id_turma)
        alunos = turma.alunos.all()
        projeto = Projeto.objects.get(pk=id_projeto)
        return render(request, self.template_name, {'alunos': alunos, 'projeto': projeto})




class ProporProjeto(View):
    """
    Um aluno propõem um projeto para o professor da turma.
    """
    template_name = 'aluno/propor_projeto.html'

    def get(self, request, id_turma):
        return render(request, self.template_name)

    def post(self, request, id_turma):
        aluno = get_user(request.user)
        turma = Turma.objects.get(pk=id_turma)

        Proposta.objects.create(
            titulo=request.POST['titulo'],
            descricao=request.POST['descricao'],
            tags=request.POST['tags'],
            autor=aluno,
            turma=turma,
        )

        return redirect('detalhe_turma', id_turma)

def projetos(request):
    template_name = 'aluno/projetos.html'

    if request.method == 'GET':
        return render(request, template_name)

class ProjetoDetalhe(View):
    template_name = 'projeto.html'

    def get(self, request, id):
        projeto = get_object_or_404(Projeto, pk=id)
        return render(request, self.template_name, {'projeto': projeto})