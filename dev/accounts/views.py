from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

from accounts.models import User
from app.models import Aluno, Professor, Departamento, Curso

# Create your views here.
class CadastrarAluno(View):
    template_name = 'registration/aluno.html'

    def get(self, request):
        cursos = Curso.objects.all()

        return render(request, self.template_name, { 'cursos': cursos })

    def post(self, request):
        user = User(
            email=request.POST['email'],
            is_student=True,
        )
        user.set_password(request.POST['senha'])
        user.save()

        curso = Curso.objects.get(pk=request.POST['curso'])
        
        Aluno.objects.create(
            user=user,
            matricula=request.POST['matricula'],
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
        user = User(
            email=request.POST['email'],
            is_teacher=True,
        )
        user.set_password(request.POST['senha'])
        user.save()
        
        dept = Departamento.objects.get(pk=request.POST['dept'])

        Professor.objects.create(
            user=user,
            matricula=request.POST['matricula'],
            nome=request.POST['nome'],
            data_nascimento=request.POST['nasc'],
            departamento=dept,
        )

        login(request, user)
        return redirect('perfil')

