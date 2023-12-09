from django.db import models


class Departamento(models.Model):
    cod_departamento = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)

class Pessoa(models.Model):
    """
    Uma pessoa, base para outros modelos.
    """
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=10, primary_key=True)
    data_nascimento = models.DateField()

    class Meta:
        # Como queremos que NÃO seja criada uma tabela para essa classe, ela
        # vira uma ABC.
        abstract = True


class Professor(Pessoa):
    matriculaProfessor = models.CharField(primary_key=True, max_length=12)
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.SET("Nao existe"))

class Projeto(models.Model):
    id_projeto = models.CharField(max_length=10)

class Proposta(models.Model):
    id_proposta = models.charField(10)
    matriculaProfessor = models.ForeignKey(Professor, on_delete=) #
    id_projeto = models.ForeignKey(Projeto, on_delete=)
