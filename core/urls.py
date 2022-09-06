from django.urls import path

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    path('colaborador/', colaborador, name='colaborador'),

    
    path('cadastrarEquipamento/', cadastrarEquipamento, name='cadastrarEquipamento'),
    path('deletarEquipamento/', deletarEquipamento, name='deletarEquipamento'),
    path('editarEquipamento/', editarEquipamento, name='editarEquipamento'),


    path('novoEmprestimo/', novoEmprestimo, name='novoEmprestimo'),
    path('encerrarEmprestimo/', encerrarEmprestimo, name='encerrarEmprestimo'),


]
