from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.messages import constants
from django.contrib import messages

from accounts.models import User
from app.models import Aluno, Professor, Departamento, Curso

# Create your views here.
class CadastrarAluno(View):
    template_name = 'registration/aluno.html'

    def get(self, request):
        cursos = Curso.objects.all()
        return render(request, self.template_name, { 'cursos': cursos })

    def post(self, request):
        email = request.POST['email']
        matricula = request.POST['matricula']
        
        if checar_credenciais(request, email, matricula):
            return redirect('cadastrar_aluno')

        user = User(
            email=email,
            is_student=True,
        )
        user.set_password(request.POST['senha'])
        user.save()

        curso = Curso.objects.get(pk=request.POST['curso'])
        
        Aluno.objects.create(
            user=user,
            matricula=matricula,
            nome=request.POST['nome'],
            data_nascimento=request.POST['nasc'],
            curso=curso,
        )

        login(request, user)
        return redirect('perfil')


class CadastrarProfessor(View):
    template_name = 'registration/professor.html'

    def get(self, request):
        departamentos = Departamento.objects.all()

        return render(request, self.template_name, { 'departamentos': departamentos })

    def post(self, request):
        email = request.POST['email']
        matricula = request.POST['matricula']

        if checar_credenciais(request, email, matricula):
            return redirect('cadastrar_professor')

        user = User(
            email=email,
            is_teacher=True,
        )
        user.set_password(request.POST['senha'])
        user.save()
        
        dept = Departamento.objects.get(pk=request.POST['dept'])

        Professor.objects.create(
            user=user,
            matricula=matricula,
            nome=request.POST['nome'],
            data_nascimento=request.POST['nasc'],
            departamento=dept,
        )

        login(request, user)
        return redirect('perfil')


def checar_credenciais(request, email, matricula):
    """
        Checa se já existe um usuário cadastrado com o email
        e matrícula digitados
    """
    user = User.objects.filter(email=email)
    if user.exists():
        messages.add_message(request, constants.ERROR, "Email já cadastrado!")
        return True
        
    aluno = Aluno.objects.filter(matricula=matricula)
    prof = Professor.objects.filter(matricula=matricula)
    if aluno.exists() or prof.exists():
        messages.add_message(request, constants.ERROR, "Matrícula já cadastrada!")
        return True
    return False