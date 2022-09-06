from django.db import models

from cpffield import cpffield


class MyModel(models.Model):
    cpf = cpffield.CPFField('CPF', max_length=14)
