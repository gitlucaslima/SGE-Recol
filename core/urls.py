from django.urls import include, path

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registro/', registrar, name='registrar'),


    
    path('cadastrarColaborador/', cadastrarColaborador, name='cadastrarColaborador'),
    path('deletarColaborador/', deletarColaborador, name='deletarColaborador'),
    path('editarColaborador/', editarColaborador, name='editarColaborador'),

    path('cadastrarEquipamento/', cadastrarEquipamento, name='cadastrarEquipamento'),
    path('deletarEquipamento/', deletarEquipamento, name='deletarEquipamento'),
    path('editarEquipamento/', editarEquipamento, name='editarEquipamento'),

    path('novoEmprestimo/', novoEmprestimo, name='novoEmprestimo'),
    path('encerrarEmprestimo/', encerrarEmprestimo, name='encerrarEmprestimo'),

    path('cadastrarUsuario/', cadastrarUsuario, name='cadastrarUsuario'),
    path('deletarUsuario/', deletarUsuario, name='deletarUsuario'),
    path('editarUsuario/', editarUsuario, name='editarUsuario'),




]
