from django.contrib import messages
from django.contrib.auth import login as login_check
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from validate_docbr import CPF

from core.models import *


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = Usuario.objects.filter(email=email).first()
        print(user)

        if(not user):

            messages.add_message(request, messages.ERROR,
                                "Login ou senha inválidos")
            return redirect("login")

        is_equal_password = user.check_password(senha)

        if(is_equal_password):

            login_check(request, user)

            return redirect("/")
    return render(request, template_name='gerenciarAcesso/login.html')

def index(request):
    return render(request, template_name='base.html')
    
def cadastrarUsuario(request):
    if request.method == "GET":

        usuarios = Usuario.objects.all()
        context = {}
        context['usuarios'] = usuarios

        return render(request, template_name='gerenciarAcesso/registrarUsuario/registro.html', context=context)

    elif request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("password")
        setor = request.POST.get("setor")

        novoUsuario = Usuario()
        novoUsuario.username = nome
        novoUsuario.email = email
        novoUsuario.password = senha
        novoUsuario.setor = setor

        jaExisteNome = Usuario.objects.filter(username=nome)
        jaExisteEmail = Usuario.objects.filter(email=email)

        if(jaExisteNome or jaExisteEmail):
            messages.add_message(
                request, messages.ERROR, 'Já existe um usuario cadastrado')

            return render(request, template_name='gerenciarAcesso/registrarUsuario/registro.html')

        try:
            
            novoUsuario.is_staff = True
            novoUsuario.is_admin = True
            novoUsuario.is_superuser = True
            novoUsuario.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Usuario cadastrado com sucesso')
        except:
            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

        usuarios = Usuario.objects.all()
        context = {}
        context['usuarios'] = usuarios

        return render(request, template_name='gerenciarAcesso/registrarUsuario/registro.html', context=context)

def deletarUsuario(request):
        context = {}

        if request.method == "POST":
            id = request.POST.get("id")

            colaborador = get_object_or_404(Usuario, id=id)

            try:
                colaborador.delete()
                messages.add_message(request, messages.SUCCESS,
                                 "O usuario foi excluido com sucesso!")
            

            except ValueError:
                messages.add_message(request, messages.ERROR,
                                 "Não foi possivel excluir o usuario")
                                 

            usuarios = Usuario.objects.all()
            context['usuarios'] = usuarios
        

        return render(request, template_name='gerenciarAcesso/registrarUsuario/registro.html', context=context)

def editarUsuario(request):
        context = {}

        if request.method == "POST":
            id = request.POST.get("id")
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            senha = request.POST.get("senha")
            setor = request.POST.get("setor")
            status = request.POST.get("status")

            usuario = Usuario.objects.filter(id=int(id)).first()
            usuario.username = nome
            usuario.email = email
            usuario.password = senha
            usuario.setor = setor
            usuario.status = status

            jaExisteNome = Usuario.objects.filter(username=nome).first()
            jaExisteEmail = Usuario.objects.filter(email=email).first()

            if(jaExisteNome and jaExisteEmail):
                if(jaExisteNome.username != usuario.username or jaExisteEmail.email != usuario.email):
                    messages.add_message(
                        request, messages.ERROR, 'Já existe um colaborador cadastrado')
                    return render(request, template_name='gerenciarAcesso/registrarUsuario/registro.html', context=context)

            try:
                usuario.save()
                messages.add_message(request, messages.SUCCESS,
                                    'Registros atualizados com sucesso')
            except:
                messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

            usuarios = Usuario.objects.all()
            context = {}
            context['usuarios'] = usuarios

        return render(request, template_name='gerenciarAcesso/registrarUsuario/registro.html', context=context)

@login_required
def cadastrarColaborador(request):
   
    if request.method == "GET":

        colaboradores = Colaborador.objects.all()
        context = {}
        context['colaboradores'] = colaboradores
        
        return render(request, template_name='colaborador/colaborador.html', context=context)

    elif request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        setor = request.POST.get("setor")

        novoColaborador = Colaborador()
        novoColaborador.nome = nome
        novoColaborador.email = email
        novoColaborador.cpf = cpf
        novoColaborador.setor = setor

        jaExisteNome = Colaborador.objects.filter(nome=nome)
        jaExisteCpf = Colaborador.objects.filter(cpf=cpf)

        colaboradores = Colaborador.objects.all()
        context = {}
        context['colaboradores'] = colaboradores

        # Verificando se o cpf é valido
        auxCpf = CPF()
        cpfValido = auxCpf.validate(cpf)

        #se não for valido
        if(cpfValido == False):
            messages.add_message(
                request, messages.ERROR, 'Esse número de CPF é invalido')
            return render(request, template_name='colaborador/colaborador.html', context=context)

        if(jaExisteNome or jaExisteCpf):
            messages.add_message(
                request, messages.ERROR, 'Já existe um colaborador cadastrado')
            return render(request, template_name='colaborador/colaborador.html', context=context)

        try:
            novoColaborador.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Colaborador cadastrado com sucesso')
        except:
            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

    return render(request, template_name='colaborador/colaborador.html', context=context)

@login_required
def deletarColaborador(request):
    context = {}

    if request.method == "POST":
        id = request.POST.get("id")

        colaborador = get_object_or_404(Colaborador, id=id)

        try:
            colaborador.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "O colaborador foi excluido com sucesso!")
            

        except ValueError:
            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel deletar o colaborador")
                                 

        colaboradores = Colaborador.objects.all()
        context['colaboradores'] =  colaboradores
        

    return render(request, template_name='colaborador/colaborador.html', context=context)

@login_required
def editarColaborador(request):
    context = {}

    if request.method == "POST":
        id = request.POST.get("id")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        setor = request.POST.get("setor")

        colaborador = Colaborador.objects.filter(id=int(id)).first()
        colaborador.nome = nome
        colaborador.email = email
        colaborador.cpf = cpf
        colaborador.setor = setor

        colaboradores = Colaborador.objects.all()
        context = {}
        context['colaboradores'] = colaboradores

        # Verificando se o cpf é valido
        auxCpf = CPF()
        cpfValido = auxCpf.validate(cpf)

        #se não for valido
        if(cpfValido == False):
            messages.add_message(
                request, messages.ERROR, 'Esse número de CPF é invalido')
            return render(request, template_name='colaborador/colaborador.html', context=context)

        jaExisteNome = Colaborador.objects.filter(nome=nome).first()
        jaExisteCpf = Colaborador.objects.filter(cpf=cpf).first()

        if(jaExisteNome and jaExisteCpf):
            if(jaExisteNome.nome != colaborador.nome or jaExisteCpf.cpf != colaborador.cpf):
                messages.add_message(
                    request, messages.ERROR, 'Já existe um colaborador cadastrado')
                return render(request, template_name='colaborador/colaborador.html', context=context)

        try:
            colaborador.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Registros atualizados com sucesso')
        except Exception as Error:
            messages.add_message(
                    request, messages.ERROR, 'Já existe um colaborador cadastrado')

    return render(request, template_name='colaborador/colaborador.html', context=context)

@login_required
def cadastrarEquipamento(request):

    if request.method == "GET":

        equipamentos = Equipamento.objects.all()
        context = {}
        context['equipamentos'] = equipamentos

        return render(request, template_name='equipamento/equipamento.html', context=context)
    
    elif request.method == "POST":

        nome = request.POST.get("nome")
        n_serie = request.POST.get("n_serie")
        quantidade = request.POST.get("quantidade")
        observacao = request.POST.get("observacao")

        novoEquipamento = Equipamento()
        novoEquipamento.nome = nome
        novoEquipamento.n_serie = n_serie
        novoEquipamento.quantidade = quantidade
        novoEquipamento.observacao = observacao

        jaExisteNome = Equipamento.objects.filter(nome=nome)
        jaExisteN_serie = Equipamento.objects.filter(n_serie=n_serie)

        equipamentos = Equipamento.objects.all()
        context = {}
        context['equipamentos'] = equipamentos

        if(jaExisteNome or jaExisteN_serie):
            messages.add_message(
                request, messages.ERROR, 'Já existe um equipamento cadastrado')
            return render(request, template_name='equipamento/equipamento.html', context=context)

        try:
            novoEquipamento.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Equipamento cadastrado com sucesso')

        except Error:

            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')


    return render(request, template_name='equipamento/equipamento.html', context=context)

@login_required
def editarEquipamento(request):

    context = {}

    if request.method == "POST":
        id = request.POST.get("id")
        nome = request.POST.get("nome")
        n_serie = request.POST.get("n_serie")
        quantidade = request.POST.get("quantidade")
        observacao = request.POST.get("observacao")

        equipamento = Equipamento.objects.filter(id=int(id)).first()

        equipamento.nome = nome
        equipamento.n_serie = n_serie
        equipamento.quantidade = quantidade
        equipamento.observacao = observacao

        jaExisteNome = Equipamento.objects.filter(nome=nome)
        jaExisteN_serie = Equipamento.objects.filter(n_serie=n_serie)

        equipamentos = Equipamento.objects.all()
        context['equipamentos'] = equipamentos

        if(jaExisteNome or jaExisteN_serie):
            messages.add_message(
                request, messages.ERROR, 'Já existe um equipamento com essas especificações')
            return render(request, template_name='equipamento/equipamento.html', context=context)

        try:
            equipamento.save()
            messages.add_message(request, messages.SUCCESS,
                                 "O equipamento foi atualizado com sucesso!")

            
        except ValueError:
            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel atualizar o equipamento")
            
        
        equipamentos = Equipamento.objects.all()
        context['equipamentos'] = equipamentos


    return render(request, template_name='equipamento/equipamento.html', context=context)

@login_required
def deletarEquipamento(request):

    context = {}

    if request.method == "POST":
        id = request.POST.get("id")

        equipamento = get_object_or_404(Equipamento, id=id)

        try:
            equipamento.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "O equipamento foi excluido com sucesso!")
            

        except ValueError:
            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel deletar o equipamento")
                                 

        equipamentos = Equipamento.objects.all()
        context['equipamentos'] = equipamentos
        

    return render(request, template_name='equipamento/equipamento.html', context=context)

@login_required
def novoEmprestimo(request):
    return render(request, template_name='emprestimo/novoEmprestimo.html')

@login_required
def encerrarEmprestimo(request):
    return render(request, template_name='emprestimo/encerrarEmprestimo.html')
