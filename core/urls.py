from django.urls import path

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    
    path('cadastrarColaborador/', cadastrarColaborador, name='cadastrarColaborador'),
    path('deletarColaborador/', deletarColaborador, name='deletarColaborador'),
    path('editarColaborador/', editarColaborador, name='editarColaborador'),

    
    path('cadastrarEquipamento/', cadastrarEquipamento, name='cadastrarEquipamento'),
    path('deletarEquipamento/', deletarEquipamento, name='deletarEquipamento'),
    path('editarEquipamento/', editarEquipamento, name='editarEquipamento'),


    path('novoEmprestimo/', novoEmprestimo, name='novoEmprestimo'),
    path('encerrarEmprestimo/', encerrarEmprestimo, name='encerrarEmprestimo'),


]
