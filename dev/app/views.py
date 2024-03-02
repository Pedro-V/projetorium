from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Professor, User, Aluno, Turma, Disciplina


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

def consulta_projeto(request):
    template_name = 'consulta_projeto.html'

    if request.method == "GET":
        return render(request, template_name)


class ListarTurmas(View):
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

        return redirect('cadastro_aluno')


class CadastrarTurma(View):
    """
    Um professor cadastra uma nova turma.
    """
    template_name = 'professor/cad_turma.html'

    def get(self, request):
        disciplinas = Disciplina.objects.all()
        
        return render(request, self.template_name, { "disciplinas": disciplinas })

    def post(self, request):
        prof = Professor.objects.get(user=request.user)
        disc = Disciplina.objects.get(pk=request.POST['disciplina'])

        Turma.objects.create(
            disciplina=disc,
            professor=prof,
            ano=request.POST['ano'],
            periodo=request.POST['periodo'],
            codigo=request.POST['codigo'],
        )

        return redirect('cadastro_turma')


def propostas(request):
    template_name = 'professor/propostas.html'

    if request.method == 'GET':
        return render(request, template_name)
        
def avaliar_proposta(request):
    template_name = 'professor/avaliar_proposta.html'
    
    if request.method == "GET":
        return render(request, template_name)

def escolher_projeto(request, id_turma):
    template_name = 'aluno/escolher_projeto.html'

    if request.method == 'GET':
        return render(request, template_name)


class ProporProjeto(View):
    """
    Um aluno propõem um projeto para o professor da turma.
    """
    template_name = 'aluno/propor_projeto.html'

    def get(request, id_turma):
        return render(request, template_name)


def projetos(request):
    template_name = 'aluno/projetos.html'

    if request.method == 'GET':
        return render(request, template_name)
