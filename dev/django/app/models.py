from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django import forms 
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class Departamento(models.Model):
    cod_departamento = models.CharField(max_length=10)
    nome = models.CharField(max_length=300)

class Disciplina(models.Model):
    cod_disciplina = models.CharField(max_length=10)
    nome = models.CharField(max_length=300)
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.SET("Nao existe"))

class Professor(models.Model):
    matricula_professor = models.CharField(primary_key=True, max_length=12)
    nome = models.CharField(max_length=300)
    data_nascimento = models.DateField()
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.SET("Nao existe"))

class Grupo(models.Model):
    cod_grupo = models.AutoField(primary_key=True)


class Aluno(models.Model):
    matricula_aluno = models.CharField(primary_key=True, max_length=12)
    nome = models.CharField(max_length=300)
    curso = models.CharField(max_length=300)
    data_nascimento = models.DateField()
    cod_grupo = models.ForeignKey(Grupo, null=True, on_delete=models.SET("Nao existe"))

class Turma(models.Model):
    cod_turma = models.CharField(primary_key=True, max_length=12)
    cod_disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

class Turma_Professor(models.Model):
    cod_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    matricula_professor = models.ForeignKEY(Professor, on_delete=models.CASCADE)
    class Meta:#para a chave primária composta
        constraints = [
            models.UniqueConstraint(
                fields = ['cod_turma', 'matricula_professor'], name="cod_turma_professor"
            )
        ]

class Turma_Aluno(models.Model):
    cod_turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    matricula_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    class Meta:#para a chave primária composta
        constraints = [
            models.UniqueConstraint(
                fields = ['cod_turma', 'matricula_aluno'], name="cod_turma_aluno"
            )
        ]

class Projeto_Abstrato(models.Model, forms.Form):
    cod_projeto_abstrato = models.CharField(primary_key=True, max_lenght=10)
    titulo = models.CharField(max_lenght=300)
    descricao = models.CharField(max_lenght=800)
    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    documentos = ArrayField(forms.FileField(), blank=True, null=True)

class Projeto(Projeto_Abstrato):
    data_criacao = models.DateField()
    cod_grupo = models.OneToOneField(Grupo, on_delete=models.SET("Nao existe"))

    class Status_Projeto(models.TextChoices):
        CONCLUIDO = 'CO', _('Concluido')
        CANCELADO = 'CA', _('Cancelado')
        SUSPENSO = 'SU', _('Suspenso')
        EM_PROGRESSO = 'EP', _('Em progresso')
    
    status_projeto = models.CharField(max_lenght=2, choices=Status_Projeto.choices, default=Status_Projeto.EM_PROGRESSO)

class Proposta(Projeto_Abstrato):
    data_proposta = models.DateField()

class Avaliacao(models.Model):
    cod_avaliacao = models.AutoField(primary_key=True)
    mensagem = models.CharField(max_length=800)
    cod_proposta = models.OneToOneField(Proposta, on_delete=models.SET("Nao existe"))

    class Status_Avaliacao(models.TextChoices):
            APROVADO = 'AP', _('Aprovado')
            REJEITADO = 'RE', _('Rejeitado')
            MELHORIAS = 'ME', _('Melhorias')
    
    status_avaliacao = models.CharField(max_lenght=2, choices=Status_Avaliacao.choices)



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
