from datetime import datetime

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager

# User base model, used for authentication in the system
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_admin = models.BooleanField(
        'admin status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_student = models.BooleanField(
        'student',
        default=False,
        help_text='Designates whether the user is a student.'
    )
    is_teacher = models.BooleanField(
        'teacher',
        default=False,
        help_text=('Designates whether the user is a teacher.')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Departamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.departamento}{self.codigo}: {self.nome}'

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula= models.CharField(primary_key=True, max_length=12)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    departamento = models.ForeignKey(Departamento, on_delete=models.SET("Nao existe"))

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    matricula = models.CharField(primary_key=True, max_length=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=50)
    data_nascimento = models.DateField()

    def __str__(self):
        return f'{self.nome}: {self.matricula}'

class Grupo(models.Model):
    alunos = models.ManyToManyField(Aluno)

class Turma(models.Model):
    codigo = models.CharField(max_length=12)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    alunos = models.ManyToManyField(Aluno)

    ano = models.IntegerField(default=datetime.now().year)
    periodo = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.disciplina} -  T{self.codigo}'

class Projeto(models.Model):
    titulo = models.CharField(max_length=300)
    descricao = models.CharField(max_length=800)
    data_criacao = models.DateField()
    cod_grupo = models.OneToOneField(Grupo, on_delete=models.SET("Nao existe"))

    class StatusProjeto(models.TextChoices):
        CONCLUIDO    = ('CO', 'Concluido')
        CANCELADO    = ('CA', 'Cancelado')
        SUSPENSO     = ('SU', 'Suspenso')
        EM_PROGRESSO = ('EP', 'Em progresso')
    
    status_projeto = models.CharField(
        max_length=2,
        choices=StatusProjeto.choices,
        default=StatusProjeto.EM_PROGRESSO
    )

    def __str__(self):
        return self.titulo

class Proposta(models.Model):
    titulo = models.CharField(max_length=300)
    descricao = models.CharField(max_length=800)
    data_proposta = models.DateField()
    proponente = models.ForeignKey(Aluno, on_delete=models.CASCADE)

class Avaliacao(models.Model):
    mensagem = models.CharField(max_length=800)
    proposta = models.OneToOneField(Proposta, on_delete=models.CASCADE)

    class StatusAvaliacao(models.TextChoices):
        APROVADO  = ('AP', 'Aprovado')
        REJEITADO = ('RE', 'Rejeitado')
        MELHORIAS = ('ME', 'Melhorias')
    
    status_avaliacao = models.CharField(max_length=2, choices=StatusAvaliacao.choices)
