from django.db import models
from datetime import datetime

from accounts.models import User


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    matricula= models.CharField(primary_key=True, max_length=12)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    departamento = models.ForeignKey(Departamento, on_delete=models.SET("Nao existe"))

    def __str__(self):
        return self.nome

    def turmas(self):
        """
        Retorna as turmas que um professor leciona.
        """
        turmas = Turma.objects.filter(professor=self)
        return turmas


class Aluno(models.Model):
    matricula = models.CharField(primary_key=True, max_length=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=50)
    data_nascimento = models.DateField()

    def __str__(self):
        return f'{self.nome}: {self.matricula}'

    def turmas(self):
        """
        Retorna as turmas de um determinado aluno.
        """
        return self.turma_set.all()


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
    tags = models.CharField(max_length=800)
    data_proposta = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Aluno, on_delete=models.CASCADE)

class Avaliacao(models.Model):
    mensagem = models.CharField(max_length=800)
    proposta = models.OneToOneField(Proposta, on_delete=models.CASCADE)

    class StatusAvaliacao(models.TextChoices):
        APROVADO  = ('AP', 'Aprovado')
        REJEITADO = ('RE', 'Rejeitado')
        MELHORIAS = ('ME', 'Melhorias')
    
    status_avaliacao = models.CharField(max_length=2, choices=StatusAvaliacao.choices)
