from django.db.models.signals import post_migrate
from django.dispatch import receiver

from accounts.models import *
from app.models import *

def initialize_basic_data():
    """
    Inicializa componentes básicos (Departamentos, Cursos e Disciplinas),
    os quais o usuário final não consegue criar.
    """

    departamentos = [
        {
            'nome': 'DCOMP',
        },
    ]
    for dep in departamentos:
        Departamento.objects.create(**dep)

    cursos = [
        {
            'nome': 'Ciência da Computação',
            'departamento': Departamento.objects.get(nome='DCOMP'),
        },
        {
            'nome': 'Engenharia da Computação',
            'departamento': Departamento.objects.get(nome='DCOMP'),
        },
        {
            'nome': 'Sistemas de Informação',
            'departamento': Departamento.objects.get(nome='DCOMP'),
        },
    ]
    for curso in cursos:
        Curso.objects.create(**curso)

    disciplinas = [
        {
            'codigo': '0438',
            'nome': 'Engenharia de Software I',
            'departamento': Departamento.objects.get(nome='DCOMP'),
        },
        {
            'codigo': '0439',
            'nome': 'Engenharia de Software II',
            'departamento': Departamento.objects.get(nome='DCOMP'),
        },
    ]
    for disc in disciplinas:
        Disciplina.objects.create(**disc)


def initialize_user_data():
    """
    Inicializa componentes de usuário final,
    os quais o usuário final consegue criar.
    """

    users = [
        {
            'email': 'admin@exemplo.com',
            'password': 'admin',
            'is_teacher': False,
            'is_student': False,
        },
        {
            'email': 'michel@dcomp.ufs.br',
            'password': 'michel',
            'is_teacher': True,
            'is_student': False,
        },
        {
            'email': 'pedro@academico.ufs.br',
            'password': 'pedro',
            'is_teacher': False,
            'is_student': True,
        },
        {
            'email': 'tiago@dcomp.ufs.br',
            'password': 'tiago',
            'is_teacher': False,
            'is_student': True,
        },
    ]
    for user in users:
        User.objects.create(**user)

    professors = [
        {
            'user': User.objects.get(email='michel@dcomp.ufs.br'),
            'matricula': 9,
            'nome': 'Michel Soares',
            'data_nascimento': '1980-03-03',
            'departamento': Departamento.objects.get(nome='DCOMP'),
        },
    ]
    for prof in professors:
        Professor.objects.create(**professors)

    alunos = [
        {
            'user': User.objects.get(email='pedro@academico.ufs.br'),
            'matricula': '202100011815',
            'nome': 'Pedro',
            'curso': Curso.objects.get(nome='Ciência da Computação'),
            'data_nascimento': '2003-04-23',
        },
        {
            'user': User.objects.get(email='tiago@academico.ufs.br'),
            'matricula': '202200011816',
            'nome': 'Tiago',
            'curso': Curso.objects.get(nome='Engenharia da Computação'),
            'data_nascimento': '2004-04-23',
        },
    ]
    for aluno in alunos:
        Aluno.objects.create(**aluno)

def initialize_data():
    initialize_basic_data()

@receiver(post_migrate)
def initialize_data_after_migrate(sender, **kwargs):
    # Só inicializa se dados não existirem.
    if sender.name == 'app' and not Professor.objects.all():
        initialize_data()
