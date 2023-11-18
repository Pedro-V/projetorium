from django.db import models


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
