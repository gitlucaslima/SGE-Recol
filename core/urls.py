from django.urls import path

from core.views import colaborador, encerrarEmprestimo, equipamento, index, novoEmprestimo

urlpatterns = [
    path('', index, name='index'),
    path('colaborador/', colaborador, name='colaborador'),
    path('equipamento/', equipamento, name='equipamento'),
    path('novoEmprestimo/', novoEmprestimo, name='novoEmprestimo'),
    path('encerrarEmprestimo/', encerrarEmprestimo, name='encerrarEmprestimo'),


]
