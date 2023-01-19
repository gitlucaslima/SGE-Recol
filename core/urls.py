from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.auth import views as auth_views

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registro/', registrar, name='registrar'),

    path('cadastrarColaborador/', cadastrarColaborador,
         name='cadastrarColaborador'),
    path('deletarColaborador/', deletarColaborador, name='deletarColaborador'),
    path('editarColaborador/', editarColaborador, name='editarColaborador'),

    path('cadastrarEquipamento/', cadastrarEquipamento,
         name='cadastrarEquipamento'),
    path('deletarEquipamento/', deletarEquipamento, name='deletarEquipamento'),
    path('editarEquipamento/', editarEquipamento, name='editarEquipamento'),

    path('novoEmprestimo/', novoEmprestimo, name='novoEmprestimo'),
    path('encerrarEmprestimo/', encerrarEmprestimo, name='encerrarEmprestimo'),

    path('cadastrarUsuario/', cadastrarUsuario, name='cadastrarUsuario'),
    path('deletarUsuario/', deletarUsuario, name='deletarUsuario'),
    path('editarUsuario/', editarUsuario, name='editarUsuario'),

    path('novoEmprestimo/', novoEmprestimo, name='novoEmprestimo'),
    path('editarEmprestimo/<int:id>/',
         editarEmprestimo, name='editarEmprestimo'),
    path('deletarEmprestimo/', deletaEmprestimo, name='deletarEmprestimo'),
    path('finalizarEmprestimo/<str:id>/',
         finalizarEmprestimo, name='finalizarEmprestimo'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
