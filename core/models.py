from enum import auto, unique
from urllib import request

from cpf_field.models import CPFField
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models


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
        default=1,
        null=False,
        blank=True
    )

    arquivo_foto = models.FileField(
        ('Foto do objeto'), 
        null=True, 
        blank=True, 
        upload_to='midias', 
        help_text='Tamanho máximo de 64MB'
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
        blank=False,
        unique=True
    )

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True
    )

    cpf = CPFField('cpf',
        null=False,
        blank=False,
        unique=True
    )

    rg = models.CharField(
        max_length=9,
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

    STATUS_CHOICES =(
        ("1", "Ativo"),
        ("0", "Inativo"),
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        null=False
    )

    def __str__(self):
        return self.username

class Emprestimo(models.Model):
    colaborador = models.ForeignKey(Colaborador, 
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    data_criacao = models.DateField(
        auto_now=True,
        null=False,
        blank=False,
    )

    data_encerramento = models.DateField(
        auto_now=False,
        null=False,
        blank=False,
    )

    emprestimo_equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    assinatura_colaborador = models.ImageField(        
        null=False,
        blank=False,
    )

    assinatura_responsavel = models.ImageField(        
        null=False,
        blank=False,
    )

    STATUS_EMPRESTIMO_CHOICES = (
        ("0", "Atrasado"),
        ("1", "Aberto"),
        ("2", "Encerrado"),
    )

    status_emprestimo = models.IntegerField(
        choices = STATUS_EMPRESTIMO_CHOICES,
        default = 1,
        blank=False,
        null = False,
    )




