# Generated by Django 4.1 on 2022-10-18 23:01

import cpf_field.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cpf', cpf_field.models.CPFField(max_length=14, unique=True, verbose_name='cpf')),
                ('rg', models.CharField(max_length=9, unique=True)),
                ('setor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField(auto_now=True)),
                ('data_encerramento', models.DateField(blank=True)),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('assinatura_colaborador', models.ImageField(upload_to='')),
                ('assinatura_responsavel', models.ImageField(upload_to='')),
                ('status_emprestimo', models.CharField(choices=[('Atrasado', 'Atrasado'), ('Aberto', 'Aberto'), ('Encerrado', 'Encerrado')], default='Aberto', max_length=100)),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.colaborador')),
            ],
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('n_serie', models.IntegerField(unique=True)),
                ('quantidade', models.IntegerField(blank=True, default=1)),
                ('arquivo_foto', models.FileField(blank=True, help_text='Tamanho máximo de 64MB', null=True, upload_to='midias', verbose_name='Foto do objeto')),
                ('status', models.CharField(choices=[('Disponivel', 'Disponivel'), ('Emprestado', 'Emprestado'), ('Indisponivel', 'Indisponivel')], default='Disponivel', max_length=100, null=True)),
                ('observacao', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('setor', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[('1', 'Ativo'), ('0', 'Inativo')], default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TermoRespo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_termoRespo', models.FileField(upload_to='termos/')),
                ('Emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.emprestimo')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.colaborador')),
            ],
        ),
        migrations.CreateModel(
            name='TermoDevo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_termoDevo', models.FileField(upload_to='termos/')),
                ('Emprestimo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.emprestimo')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.colaborador')),
            ],
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='emprestimo_equipamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.equipamento'),
        ),
    ]
