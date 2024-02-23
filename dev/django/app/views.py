from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Professor, User, Aluno

@login_required
def perfil(request):
    if request.method == 'GET':
        if request.user.is_teacher:
            template_name = 'professor/perfil.html'
    
            prof = Professor.objects.filter(user=request.user)
            return render(request, template_name, {'usuarios': prof})
        
        if request.user.is_student:
            template_name = 'aluno/perfil.html'

            aluno = Aluno.objects.filter(user=request.user)
            return render(request, template_name, {'usuarios': aluno})


def cadastro_aluno(request):
    template_name = 'professor/cad_aluno.html'

    if request.method == 'GET':
        return render(request, template_name)

def consulta_projeto(request):
    template_name = 'consulta_projeto.html'

    if request.method == "GET":
        return render(request, template_name)
    
def turmas(request):
    template_name = 'turmas.html'

    if request.method == "GET":
        return render(request, template_name)

def propostas(request):
    template_name = 'professor/propostas.html'

    if request.method == 'GET':
        return render(request, template_name)
        
def avaliar_proposta(request):
    template_name = 'professor/avaliar_proposta.html'
    
    if request.method == "GET":
        return render(request, template_name)

def cadastrar_turma(request):
    template_name = 'professor/cad_turma.html'

    if request.method == 'GET':
        return render(request, template_name)