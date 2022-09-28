from enum import unique
from urllib import request

from cpf_field.models import CPFField
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES =(
    ("1", "Ativo"),
    ("0", "Inativo"),
)

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

    STATUS_EQUIPAMENTO = (
        ("D", "Disponivel"),
        ("E", "Emprestado"),
        ("I", "Indisponivel")
    )

    status = models.CharField(max_length=1, choices=STATUS_EQUIPAMENTO, default="Disponivel", blank=False, null=True)

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

class Usuario(User):
    setor = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        null=False
    )

    def __str__(self):
        return self.username




