# Generated by Django 4.0.6 on 2022-09-30 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField(auto_now=True)),
                ('assinatura_colaborador', models.ImageField(upload_to='')),
                ('assinatura_responsavel', models.ImageField(upload_to='')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.colaborador')),
                ('emprestimo_equipamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipamento')),
            ],
        ),
    ]
