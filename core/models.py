from distutils.command.upload import upload
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
        ("Disponivel", "Disponivel"),
        ("Emprestado", "Emprestado"),
        ("Indisponivel", "Indisponivel")
    )

    status = models.CharField(max_length=100, choices=STATUS_EQUIPAMENTO,
                              default="Disponivel", blank=False, null=True)

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

    STATUS_CHOICES = (
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
        blank=True,
    )

    data_devolucao = models.DateField(
        null=True,
        blank=True,
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
        ("Atrasado", "Atrasado"),
        ("Aberto", "Aberto"),
        ("Encerrado", "Encerrado"),
    )

    status_emprestimo = models.CharField(
        choices=STATUS_EMPRESTIMO_CHOICES,
        default="Aberto",
        max_length=100,
        blank=False,
        null=False,

    )


class TermoRespo(models.Model):
    colaborador = models.ForeignKey(Colaborador,
                                    on_delete=models.PROTECT,
                                    null=False,
                                    blank=False,
                                    )
    Emprestimo = models.ForeignKey(Emprestimo,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   blank=False,
                                   )
    url_termoRespo = models.FileField(upload_to="termos/")


class TermoDevo(models.Model):
    colaborador = models.ForeignKey(Colaborador,
                                    on_delete=models.PROTECT,
                                    null=False,
                                    blank=False,
                                    )
    Emprestimo = models.ForeignKey(Emprestimo,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   blank=False,
                                   )
    url_termoDevo = models.FileField(upload_to="termos/")
