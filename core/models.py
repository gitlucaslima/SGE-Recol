from django.db import models
from cpf_field.models import CPFField
# Create your models here.

class Equipamento(models.Model):
    nome = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    n_serie = models.IntegerField(
        null=False,
        blank=False,
        unique=True
    )

    quantidade = models.IntegerField(
        null=False,
        blank=False
    )

    observacao = models.TextField(max_length=300)
    
    def __str__(self):
        return self.nome


class Colaborador(models.Model):
    nome = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    email = models.EmailField(
        null=False,
        blank=False,
    )

    cpf = CPFField('cpf',
        null=False,
        blank=False,
        unique=True
    )

    setor = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.nome





