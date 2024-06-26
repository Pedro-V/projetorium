from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from accounts.decorators import student_required, teacher_required
from django.utils.decorators import method_decorator
from django.contrib.messages import constants
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from app.signals import *
from app.models import *


def get_user(user, template_name=None):
    """
    Retorna o objeto que especifica o papel de user, e a versão específica do
    template.

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
        turmas = Turma.objects.all()
        return render(request, self.template_name, { 'turmas': turmas })

    def post(self, request):
        nome = request.POST.get('nome_proj')
        tags = request.POST.get('tags')
        turma = request.POST.get('turma')
        data = request.POST.get('data')

        # Passando os valores como parâmetros de consulta na URL para ResultadoProjeto
        get_params = f'?nome_proj={nome}&tags={tags}&turma={turma}&data={data}'
        return redirect(reverse('resultado_projeto') + get_params)


class ResultadoProjeto(View):
    template_name = 'resultado_projeto.html'

    def get(self, request):
        nome = request.GET.get('nome_proj',"")
        tags = request.GET.get('tags',"")
        turma = request.GET.get('turma',"")
        data = request.GET.get('data',"")

        try:
            aluno = Aluno.objects.get(user=request.user)
            user_grupos = Grupo.objects.filter(membros=aluno)
        except Aluno.DoesNotExist:
            aluno = None
            user_grupos = []

        projetos = Projeto.objects.filter(
            Q(publico=True) | 
            Q(publico=False, grupo__in=user_grupos) | 
            Q(publico=False, turma__professor__user=request.user)
        ).filter(
            titulo__icontains=nome,
            turma__codigo__icontains=turma,
            tags__icontains=tags
        )

        if data:
            projetos = projetos.filter(data_criacao__gte=data)

        return render(request, self.template_name, {'projetos': projetos})

@method_decorator(login_required, name="dispatch")
class ProjetosTurma(View):
    template_name = 'projetos_turma.html'

    def get(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        projetos = Projeto.objects.filter(turma=turma)
        return render(request, self.template_name, { 'projetos': projetos, 'turma': turma })

@method_decorator(login_required, name="dispatch")
class ListaTurmas(View):
    template_name = 'turmas.html'

    def get(self, request):
        user = get_user(request.user)
        return render(request, self.template_name, { 'turmas': user.turmas() })

@method_decorator(login_required, name="dispatch")
class DetalheTurma(View):
    def get(self, request, id_turma):
        _, template_name = get_user(request.user, 'turma.html')
        turma = Turma.objects.get(id=id_turma)
        return render(request, template_name, { 'turma': turma })

@method_decorator(teacher_required, name="dispatch")
class AdicionarAluno(View):
    """
    Um professor adiciona um aluno numa turma.
    """
    template_name = 'professor/adicionar_aluno.html'

    def get(self, request, id_turma):
        turma = get_object_or_404(Turma, pk=id_turma)
        prof = get_user(request.user)

        pk_alunos_atuais = [aluno.pk for aluno in turma.alunos.all()]
        alunos_elegiveis = Aluno.objects.exclude(pk__in=pk_alunos_atuais)

        return render(request, self.template_name, { 'alunos': alunos_elegiveis })

    def post(self, request, id_turma):
        matricula = request.POST['aluno']

        turma = Turma.objects.get(id=id_turma)
        aluno = Aluno.objects.get(matricula=matricula)

        turma.alunos.add(aluno)

        messages.add_message(request, constants.SUCCESS, "Aluno adicionado com sucesso.")
        return redirect('adicionar_aluno', id_turma)

@method_decorator(teacher_required, name="dispatch")
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
            messages.add_message(request, constants.ERROR, "Uma turma com esses dados já existe!")
            return redirect('cadastro_turma')

        messages.add_message(request, constants.SUCCESS, "Turma criada com sucesso.")
        return redirect('cadastro_turma')

@method_decorator(teacher_required, name="dispatch")
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
        messages.add_message(request, constants.SUCCESS, "Projeto criado com sucesso")
        return redirect('ofertar_projeto', id_turma)

@method_decorator(login_required, name="dispatch")
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

@method_decorator(login_required, name="dispatch")
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

@method_decorator(login_required, name="dispatch")
class EscolherProjeto(View):
    template_name = 'aluno/escolher_projeto.html'

    def get(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        projetos = Projeto.objects.filter(turma=turma, disponivel=True)
        return render(request, self.template_name, {'projetos': projetos, 'turma': turma })
    
    def post(self, request, id_turma):
        projeto_id = request.POST.get('projeto')
        projeto = Projeto.objects.get(pk=projeto_id)

        projeto.disponivel = False

        grupo = Grupo.objects.create()
        aluno = Aluno.objects.get(user=request.user)
        grupo.add_membro(aluno)

        projeto.grupo = grupo

        projeto.save()
        messages.add_message(request, constants.SUCCESS, "Projeto escolhido com sucesso.")
        return redirect('escolher_projeto', id_turma) 

@method_decorator(login_required, name="dispatch")
class ParticipantesTurma(View):
    """
    Lista os alunos participantes de uma turma.
    """
    template_name = 'participantes_turma.html'

    def get(self, request, id_turma):
        turma = Turma.objects.get(pk=id_turma)
        alunos = turma.get_alunos()
        context = {
            'alunos': alunos,
            'turma': turma,
        }

        return render(request, self.template_name, context)

@method_decorator(student_required, name="dispatch")
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
        messages.add_message(request, constants.SUCCESS, "Proposta criada com sucesso.")
        return redirect('detalhe_turma', id_turma)

@method_decorator(login_required, name="dispatch")
class ListarProjetos(View):
    template_name = 'aluno/projetos.html'

    def get(self, request):
        aluno = Aluno.objects.get(user=request.user)
        user_grupos = Grupo.objects.filter(membros=aluno)
        projetos_aluno = Projeto.objects.filter(grupo__in=user_grupos)
        return render(request, self.template_name, {'projetos': projetos_aluno, 'aluno': aluno})

@method_decorator(login_required, name="dispatch")
class AdicionarMembro(View):
    template_name = 'adicionar_membro.html'

    def get(self, request, id_proj):
        proj = get_object_or_404(Projeto, pk=id_proj)
        pk_membros = [membro.pk for membro in proj.grupo.get_membros()]

        alunos_elegiveis = (
            Aluno.objects
            .exclude(pk__in=pk_membros)
            .filter(turma=proj.turma)
        )

        return render(request, self.template_name, { 'alunos': alunos_elegiveis })
    
    def post(self, request, id_proj):
        proj = get_object_or_404(Projeto, pk=id_proj)
        matricula = request.POST['aluno']
        aluno = Aluno.objects.get(matricula=matricula)
        proj.grupo.add_membro(aluno)

        messages.add_message(request, constants.SUCCESS, "Aluno adicionado com sucesso.")
        return redirect('adicionar_membro', id_proj)

@method_decorator(login_required, name="dispatch")
class EditarProjeto(View):
    template_name = 'editar_projeto.html'

    def get(self, request, id_proj):
        projeto = get_object_or_404(Projeto, pk=id_proj)
        outras_opcoes = projeto.outras_opcoes()
        context = {
            'projeto': projeto,
            'outras_opcoes': outras_opcoes,
        }
        return render(request, self.template_name, context)

    def post(self, request, id_proj):
        projeto = get_object_or_404(Projeto, pk=id_proj)

        projeto.tags = request.POST.get('tags', projeto.tags)
        projeto.versao = request.POST.get('versao', projeto.versao)
        projeto.publico = bool(request.POST.get('visibilidade', projeto.publico))
        projeto.descricao = request.POST.get('descricao', projeto.descricao)
        projeto.titulo = request.POST.get('titulo', projeto.titulo)
        projeto.status = request.POST.get('status', projeto.status)
        print(request.POST['status'])
        print(projeto.status)

        projeto.save()

        messages.add_message(request, constants.SUCCESS, "Projeto editado com sucesso.")

        return redirect('projeto', id_proj=id_proj)

@method_decorator(login_required, name="dispatch")
class ProjetoDetalhe(View):
    template_name = 'projeto.html'

    def get(self, request, id_proj):
        projeto = get_object_or_404(Projeto, pk=id_proj)
        grupo = projeto.grupo
        context = {
            'projeto': projeto,
            'tags': projeto.tags_formatadas(),
        }
        if grupo is not None:
            membros = grupo.membros.all()

            autorizado = request.user in [membro.user for membro in membros]

            context['autorizado'] = autorizado
            context['membros'] = membros

        return render(request, self.template_name, context)
