from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

from accounts.models import User
from app.models import Aluno, Professor, Departamento

# Create your views here.
class CadastrarAluno(View):
    template_name = 'registration/aluno.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = User(
            email=request.POST['email'],
            is_student=True,
        )
        user.set_password(request.POST['senha'])
        user.save()
        
        Aluno.objects.create(
            user=user,
            matricula=request.POST['matricula'],
            nome=request.POST['nome'],
            data_nascimento=request.POST['nasc'],
            curso=request.POST['curso'],
        )

        login(request, user)
        return redirect('perfil')


class CadastrarProfessor(View):
    template_name = 'registration/professor.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = User(
            email=request.POST['email'],
            is_teacher=True,
        )
        user.set_password(request.POST['senha'])
        user.save()
        
        dept = Departamento.objects.get(nome=request.POST['dept'])

        Professor.objects.create(
            user=user,
            matricula=request.POST['matricula'],
            nome=request.POST['nome'],
            data_nascimento=request.POST['nasc'],
            departamento=dept,
        )

        login(request, user)
        return redirect('perfil')

