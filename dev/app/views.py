from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Professor, User, Aluno, Turma, Disciplina

def get_user_obj(user):
    """
    Retorna o objeto que especifica o papel de user.
    Nesse caso, o objeto será um Professor ou Aluno.
    """
    if user.is_teacher:
        return Professor.objects.get(user=user)
    elif user.is_student:
        return Aluno.objects.get(user=user)

@login_required
def perfil(request):
    if request.method == 'GET':
        user = get_user_obj(request.user)
        template_name = type(user).__name__.lower() + "/perfil.html"
        return render(request, template_name, { 'usuario': user })

def consulta_projeto(request):
    template_name = 'consulta_projeto.html'

    if request.method == "GET":
        return render(request, template_name)
    
def turmas(request):
    template_name = 'turmas.html'
    if request.method == "GET":
        if request.user.is_student:
            turmas = turmas_aluno(request.user)
        else:
            turmas = turmas_professor(request.user)
        return render(request, template_name, { 'turmas': turmas })

def turmas_professor(user):
    """
    Retorna as turmas que um professor leciona.
    """
    prof = Professor.objects.get(user=user)
    turmas = Turma.objects.filter(professor=prof)
    return turmas

def turmas_aluno(user):
    """
    Retorna as turmas de um determinado aluno.
    """
    aluno = Aluno.objects.get(user=user)
    turmas = aluno.turma_set.all()
    return turmas

def turma_detalhe(request, id_turma):
    user = get_user_obj(request.user)
    template_name = type(user).__name__.lower() + "/turma.html"

    turma = Turma.objects.get(id=id_turma)
    return render(request, template_name, { 'turma': turma })

def cadastro_aluno(request):
    """
    Um professor cadastra um aluno numa turma.
    """
    if request.method == 'POST':
        id_turma = request.POST['turma']
        matricula = request.POST['aluno']

        turma = Turma.objects.get(id=id_turma)
        aluno = Aluno.objects.get(matricula=matricula)

        turma.alunos.add(aluno)

        return redirect('cadastro_aluno')
    elif request.method == 'GET':
        turmas = turmas_professor(request.user)
        alunos = Aluno.objects.all()
        context = { "turmas": turmas, "alunos": alunos }

        template_name = 'professor/cad_aluno.html'
        return render(request, template_name, context)

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

def propor_projeto(request, id_turma):
    template_name = 'aluno/propor_projeto.html'

    if request.method == 'GET':
        return render(request, template_name)

def cadastrar_turma(request):
    if request.method == "POST":
        prof = Professor.objects.get(user=request.user)
        disc = Disciplina.objects.get(codigo=request.POST['disciplina'])

        Turma.objects.create(
            disciplina=disc,
            professor=prof,
            ano=request.POST['ano'],
            periodo=request.POST['periodo'],
            codigo=request.POST['codigo'],
        )

        return redirect('cadastrar_turma')
    elif request.method == 'GET':
        template_name = 'professor/cad_turma.html'
        return render(request, template_name)

def projetos(request):
    template_name = 'aluno/projetos.html'

    if request.method == 'GET':
        return render(request, template_name)
