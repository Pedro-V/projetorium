from django.db import models
from datetime import datetime

from accounts.models import User


class Departamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.departamento}{self.codigo}: {self.nome}'

    class Meta:
        constraints = [
            # Uma disciplina é identificada unicamente por essas informações.
            models.UniqueConstraint(
                fields=['codigo', 'departamento'],
                name='unique_disciplina',
            )
        ]


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    matricula= models.CharField(primary_key=True, max_length=12)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    departamento = models.ForeignKey(Departamento, null=True, on_delete=models.SET_NULL)

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
    curso = models.ForeignKey(Curso, null=True, on_delete=models.SET_NULL)
    data_nascimento = models.DateField()

    def __str__(self):
        return f'{self.nome}: {self.matricula}'

    def turmas(self):
        """
        Retorna as turmas de um determinado aluno.
        """
        return self.turma_set.all()


class Grupo(models.Model):
    membros = models.ManyToManyField(Aluno, db_table="app_forma")

    def add_membro(self, aluno):
        self.membros.add(aluno)

    def get_membros(self):
        return self.membros.all()


class Turma(models.Model):
    codigo = models.CharField(max_length=12)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    alunos = models.ManyToManyField(Aluno, db_table="app_estuda")
    ano = models.IntegerField(default=datetime.now().year)
    periodo = models.IntegerField(default=1)

    class Meta:
        constraints = [
            # Uma turma é identificada unicamente por essas informações.
            models.UniqueConstraint(
                fields=['codigo', 'disciplina', 'ano', 'periodo'],
                name='unique_turma',
            )
        ]


    def __str__(self):
        return f'{self.disciplina} -  T{self.codigo} - {self.ano}.{self.periodo}'

    def get_alunos(self):
        """
        Alunos que estudam nessa turma.
        """
        return self.alunos.all()


class Projeto(models.Model):
    titulo = models.CharField(max_length=300)
    descricao = models.CharField(max_length=800)
    data_criacao = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=800, default="")
    versao = models.CharField(max_length=20, default="")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    grupo = models.OneToOneField(Grupo, null=True, on_delete=models.SET_NULL)
    publico = models.BooleanField(default=False)
    disponivel = models.BooleanField(default=True)

    class Status(models.TextChoices):
        CONCLUIDO    = ('Concluido')
        CANCELADO    = ('Cancelado')
        SUSPENSO     = ('Suspenso')
        EM_PROGRESSO = ('Em progresso')

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EM_PROGRESSO
    )

    def __str__(self):
        return self.titulo

    def editar_tags(self, novas_tags):
        """
        Edita as tags do projeto.
        """
        self.tags = novas_tags
        self.save()


class Proposta(models.Model):
    titulo = models.CharField(max_length=300)
    descricao = models.CharField(max_length=800)
    tags = models.CharField(max_length=800, default="")
    data_proposta = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    projeto_promovido = models.ForeignKey(Projeto, null=True, on_delete=models.SET_NULL)

    def promover(self):
        grupo = Grupo.objects.create()
        grupo.add_membro(self.autor)

        Projeto.objects.create(
            titulo=self.titulo,
            descricao=self.descricao,
            tags=self.tags,
            grupo=grupo,
            status=Projeto.Status.EM_PROGRESSO,
            turma=self.turma,
            disponivel=False,
        )


class Avaliacao(models.Model):
    mensagem = models.CharField(max_length=800)
    proposta = models.OneToOneField(Proposta, on_delete=models.CASCADE)
    aprovado = models.BooleanField(default=False)
