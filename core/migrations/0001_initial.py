# Generated by Django 4.0.6 on 2022-09-06 03:34

import cpf_field.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cpf', cpf_field.models.CPFField(max_length=14, verbose_name='cpf')),
                ('setor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('n_serie', models.IntegerField()),
                ('quantidade', models.IntegerField()),
                ('observacao', models.TextField(max_length=300)),
            ],
        ),
    ]