
import base64
import datetime as dt
import locale
import os
from datetime import date, datetime, timedelta
from os import name

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as login_check
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.core.signing import TimestampSigner
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from docxtpl import DocxTemplate
from PIL import Image
from validate_docbr import CPF

from core.models import *
from core.utils import retornaData, saveMedia


def login(request):
    tem_usuarios = len(Usuario.objects.all())

    if(not tem_usuarios):
        return redirect('registrar')

    if request.method == 'POST':
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = Usuario.objects.filter(email=email).first()

        if(not user):

            messages.add_message(request, messages.ERROR,
                                 "Login ou senha inválidos")
            return redirect("login")

        is_user = user.check_password(senha)
        is_active = user.status

        if(is_active == 0):
            messages.add_message(request, messages.INFO,
                                 "Usuario inativo, entre em contato com o administrador do sistema")
            return redirect("login")

        if(is_user and (is_active == 1)):
            login_check(request, user)

            return redirect("index")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Login ou senha inválidos")
            return redirect("login")

    return render(request, template_name='accounts/login.html')


def registrar(request):

    is_usuarios = len(Usuario.objects.all())

    # Impede que alguém acesse essa funcionalidade sem a necessidade
    if is_usuarios:

        return redirect('login')

    if(request.method == "POST"):
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        senhaRepeat = request.POST.get("senha-repeat")
        setor = request.POST.get("setor")

        if senha == senhaRepeat:

            novo_usuario = Usuario()
            novo_usuario.email = email
            novo_usuario.setor = setor+'-ADM'
            novo_usuario.username = nome
            novo_usuario.status = 1
            novo_usuario.set_password(senha)

            try:

                novo_usuario.save()
                messages.add_message(
                    request, messages.SUCCESS, "Usuário criado com sucesso")
                return redirect('login')
            except Exception as e:

                messages.add_message(
                    request, messages.ERROR, "Ocorreu um erro ao salvar o usuário, tente novamente mais tarde")
                return redirect("login")

        else:

            messages.add_message(request, messages.ERROR,
                                 "A senha não são iguais")
            return redirect("registro")

    else:

        return render(request, 'accounts/registro.html')


def logout(request):

    logout_django(request)

    return redirect("login")


@login_required
def index(request):

    context = {}

    termosRepo = TermoRespo.objects.all()
    termosDevo = TermoDevo.objects.all()

    # Equipamentos disponiveis
    e_disponivel = Equipamento.objects.filter(
        status='Disponivel').count()

    # Equipamentos emprestados
    e_emprestado = Equipamento.objects.filter(
        status='Emprestado').count()  

    # Emprestimos
    emprestimos = Emprestimo.objects.all()  # todos
    emp_aberto = Emprestimo.objects.filter(
        status_emprestimo='Aberto').count()  # abertos
    emp_fechado = Emprestimo.objects.filter(
        status_emprestimo='Encerrado').count()  # abertos

    context['e_dispo'] = e_disponivel
    context['e_empr'] = e_emprestado

    context['termosRepo'] = termosRepo
    context['termosDevo'] = termosDevo


    context['emprestimos'] = emprestimos
    context['emp_aberto'] = emp_aberto
    context['emp_fechado'] = emp_fechado

    return render(request, template_name='base.html', context=context)


@login_required
def cadastrarUsuario(request):
    if request.method == "GET":

        usuarios = Usuario.objects.all()
        context = {}
        context['usuarios'] = usuarios

        return render(request, template_name='usuarios/usuarios.html', context=context)

    elif request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("password")
        setor = request.POST.get("setor")

        novoUsuario = Usuario()
        novoUsuario.username = nome
        novoUsuario.email = email
        novoUsuario.set_password(senha)
        novoUsuario.setor = setor

        jaExisteNome = Usuario.objects.filter(username=nome).first()
        jaExisteEmail = Usuario.objects.filter(email=email).first()

        if(jaExisteNome or jaExisteEmail):
            messages.add_message(
                request, messages.ERROR, 'Já existe um usuario cadastrado')

            return render(request, template_name='usuarios/usuarios.html')

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

        return render(request, template_name='usuarios/usuarios.html', context=context)


@login_required
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

    return render(request, template_name='usuarios/usuarios.html', context=context)


@login_required
def editarUsuario(request):
    context = {}

    if request.method == "POST":
        id = request.POST.get("id")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        setor = request.POST.get("setor")
        status = request.POST.get("status")

        usuario = Usuario.objects.filter(id=int(id)).first()
        usuario.username = nome
        usuario.email = email
        usuario.setor = setor
        usuario.status = status

        jaExisteNome = Usuario.objects.filter(username=nome).first()
        jaExisteEmail = Usuario.objects.filter(email=email).first()

        if(jaExisteNome and jaExisteEmail):
            if(jaExisteNome.username != usuario.username or jaExisteEmail.email != usuario.email):
                messages.add_message(
                    request, messages.ERROR, 'Já existe um colaborador cadastrado')
                return render(request, template_name='usuarios/usuarios.html', context=context)

        try:
            usuario.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Registros atualizados com sucesso')
        except:
            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

        usuarios = Usuario.objects.all()
        context = {}
        context['usuarios'] = usuarios

    return render(request, template_name='usuarios/usuarios.html', context=context)


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
        rg = request.POST.get("rg")

        novoColaborador = Colaborador()
        novoColaborador.nome = nome
        novoColaborador.email = email
        novoColaborador.cpf = cpf
        novoColaborador.setor = setor
        novoColaborador.rg = rg

        jaExisteNome = Colaborador.objects.filter(nome=nome)
        jaExisteCpf = Colaborador.objects.filter(cpf=cpf)
        jaEmail = Colaborador.objects.filter(email=email)
        jaRg = Colaborador.objects.filter(rg=rg)

        colaboradores = Colaborador.objects.all()
        context = {}
        context['colaboradores'] = colaboradores

        # Verificando se o cpf é valido
        auxCpf = CPF()
        cpfValido = auxCpf.validate(cpf)

        # se não for valido
        if(cpfValido == False):
            messages.add_message(
                request, messages.ERROR, 'Esse número de CPF é invalido')
            return render(request, template_name='colaborador/colaborador.html', context=context)

        if(jaExisteNome or jaExisteCpf or jaEmail or jaRg):
            messages.add_message(
                request, messages.ERROR, 'Já existe um colaborador cadastrado')
            return render(request, template_name='colaborador/colaborador.html', context=context)

        try:
            novoColaborador.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Colaborador cadastrado com sucesso')
        except ValueError as Error:
            messages.add_message(request, messages.ERROR,
                                 'Ocorreu algum erro {Error}')

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
        context['colaboradores'] = colaboradores

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
        rg = request.POST.get("rg")

        colaborador = Colaborador.objects.filter(id=int(id)).first()
        colaborador.nome = nome
        colaborador.email = email
        colaborador.cpf = cpf
        colaborador.setor = setor
        colaborador.rg = rg

        colaboradores = Colaborador.objects.all()
        context = {}
        context['colaboradores'] = colaboradores

        # Verificando se o cpf é valido
        auxCpf = CPF()
        cpfValido = auxCpf.validate(cpf)

        # se não for valido
        if(cpfValido == False):
            messages.add_message(
                request, messages.ERROR, 'Esse número de CPF é invalido')
            return render(request, template_name='colaborador/colaborador.html', context=context)

        jaExisteNome = Colaborador.objects.filter(nome=nome).first()
        jaExisteCpf = Colaborador.objects.filter(cpf=cpf).first()
        jaEmail = Colaborador.objects.filter(email=email).first()
        jaRg = Colaborador.objects.filter(rg=rg).first()

        if(jaExisteNome and jaExisteCpf and jaEmail and jaRg):
            if(jaExisteNome.nome != colaborador.nome
               or jaExisteCpf.cpf != colaborador.cpf
               or jaEmail.email != colaborador.email
               or jaRg.rg != colaborador.rg
               ):
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
        observacao = request.POST.get("observacao")

        quantidade = request.POST.get("quantidade")

        novoEquipamento = Equipamento()

        if(quantidade):
            novoEquipamento.quantidade = quantidade
        else:
            novoEquipamento.quantidade = 1

        novoEquipamento.nome = nome
        novoEquipamento.n_serie = n_serie
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

        except:

            messages.add_message(request, messages.ERROR, 'Ocorreu algum erro')

    return render(request, template_name='equipamento/equipamento.html', context=context)


@login_required
def editarEquipamento(request):

    context = {}

    if request.method == "POST":
        id = request.POST.get("id")
        nome = request.POST.get("nome")
        n_serie = request.POST.get("n_serie")
        status = request.POST.get("status")
        quantidade = request.POST.get("quantidade")
        observacao = request.POST.get("observacao")
        print(status)

        equipamento_edit = Equipamento.objects.filter(id=int(id)).first()

        equipamento_edit.nome = nome
        equipamento_edit.n_serie = n_serie
        equipamento_edit.quantidade = quantidade
        equipamento_edit.status = status
        equipamento_edit.observacao = observacao

        equipamentos = Equipamento.objects.all()
        context['equipamentos'] = equipamentos

        jaExisteNome = Equipamento.objects.filter(nome=nome).first()
        jaExisteN_serie = Equipamento.objects.filter(n_serie=n_serie).first()

        if(jaExisteNome and jaExisteN_serie):
            if(jaExisteN_serie.id != equipamento_edit.id and jaExisteNome.id != equipamento_edit.id):
                messages.add_message(
                    request, messages.ERROR, 'Já existe um equipamento cadastrado')
                return render(request, template_name='equipamento/equipamento.html', context=context)

        try:
            equipamento_edit.save()
            messages.add_message(request, messages.SUCCESS,
                                 "O equipamento foi atualizado com sucesso!")

        except Exception as Error:
            messages.add_message(request, messages.ERROR,
                                 "Ocorreu um erro "+{Error})

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
    context = {}

    colaboradores = Colaborador.objects.all()
    equipamentos = Equipamento.objects.filter(status="Disponivel")
    context['colaboradores'] = colaboradores
    context['equipamentos'] = equipamentos

    if request.method == "POST":
        colaborador = request.POST.get("colaborador")
        nomeEquipamento = request.POST.get("nomeEquipamento")
        quantidade = request.POST.get("quantidade")
        dataDevolucao = request.POST.get("data")
        assinaturaColaborador = request.POST.get("assinaturaColaborador")
        assinaturaResponsavel = request.POST.get("assinaturaResponsavel")

        responsavel = Usuario.objects.filter(first_name=request.user).first()
        colaboradorRequisitante = Colaborador.objects.filter(
            cpf=colaborador).first()
        equipamentoEmprestimo = Equipamento.objects.filter(
            nome=nomeEquipamento).first()

        novoEmprestimo = Emprestimo()

        # Cadastro do colaborador requisitante do emprestimo
        novoEmprestimo.colaborador = colaboradorRequisitante

        # Emprestimo aberto no dia da solicittação
        novoEmprestimo.data_criacao = date.today()

        if(equipamentoEmprestimo.quantidade < int(quantidade)):
            messages.add_message(request, messages.ERROR,
                                 'Quantidade solicitada indisponivel')
            return render(request, template_name='emprestimo/novoEmprestimo.html', context=context)

        novoEmprestimo.emprestimo_equipamento = equipamentoEmprestimo

        # Decrementação da quantidade no estoque do equipamento
        equipamentoEmprestimo.quantidade = equipamentoEmprestimo.quantidade - \
            int(quantidade)

        novoEmprestimo.emprestimo_equipamento.quantidade = quantidade

        # Alteração status do equipamento
        equipamentoEmprestimo.status = "Emprestado"

        if(dataDevolucao):
            novoEmprestimo.data_devolucao = dataDevolucao

        novoEmprestimo.data_encerramento = novoEmprestimo.data_criacao + \
            timedelta(365)

        # Converter assinatura Responsavel
        ar = retornaData(assinaturaResponsavel)

        # Converter assinatura Colaborador
        ac = retornaData(assinaturaColaborador)

        # Nomeando as assinaturas
        nomeRespo = request.user
        nomeColab = colaboradorRequisitante.nome

        # write the decoded data back to original format in  file
        urlRespoAssi = saveMedia(ar, nomeRespo)
        urlColabAssi = saveMedia(ac, nomeColab)

        print(urlRespoAssi)
        print(urlColabAssi)
        
        novoEmprestimo.assinatura_responsavel = urlRespoAssi
        novoEmprestimo.assinatura_colaborador = urlColabAssi

        # Importação do doc que será usado como template
        doc = DocxTemplate("media/modelo/modeloRespo.docx")

        locale.getlocale()
        ('pt_BR', 'UTF-8')

        # this sets the date time formats to es_ES, there are many other options for currency, numbers etc.
        locale.setlocale(locale.LC_TIME, 'pt_BR')
        'pt_BR'

        today = dt.datetime.now()

        dt.datetime(2020, 2, 14, 10, 33, 56, 487228)

        data = today.strftime('%d de %B de %Y')

        def formatcpf(cpf):
            vezes = 0
            novo = ""
            for quantidade in range(11):
                numero = cpf[quantidade]
                novo += numero
                vezes += 1
                if(quantidade == 8):
                    novo += "-"
                    vezes -= 3
                if(vezes == 3):
                    novo += "."
                    vezes -= 3
            return novo
        
        # Trocar informações pelas do modelo
        context = {
            "nomeColaborador": colaboradorRequisitante.nome,
            "cpf": formatcpf(colaboradorRequisitante.cpf),
            "rg": colaboradorRequisitante.rg,
            "quantidade": quantidade,
            "equipamento": nomeEquipamento,
            "n_serie": equipamentoEmprestimo.n_serie,
            "data": data
        }

        # Trocar assinatura do responsavel e do colab, pelas do modelo
        doc.replace_pic('Imagem 10', urlColabAssi)
        doc.replace_pic('Imagem 11', urlRespoAssi)

        # Aplicar a troca de informações
        doc.render(context)

        # Gerar um hash de
        signer = TimestampSigner()
        value = signer.sign(colaboradorRequisitante.nome).split(":")[-1]

        nome_arquivo = f"media/termos/termo{value}.docx"

        try:
            doc.save(nome_arquivo)

        except Exception as e1:
            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel gerar o termo de responsabilidade")
            return render(request, template_name='emprestimo/novoEmprestimo.html', context=context)

        novo_termo = TermoRespo()
        novo_termo.colaborador = colaboradorRequisitante
        novo_termo.Emprestimo = novoEmprestimo
        novo_termo.url_termoRespo = nome_arquivo

        try:
            novoEmprestimo.save()
            novo_termo.save()
            equipamentoEmprestimo.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Emprestimo realizado com sucesso')
        except Exception as Error:
            messages.add_message(
                request, messages.ERROR, 'Não foi possivel realizar o emprestimo')

    return render(request, template_name='emprestimo/novoEmprestimo.html', context=context)


@login_required
def deletaEmprestimo(request):

    context = {}

    if request.method == "POST":
        id = request.POST.get("id")

        emprestimo = get_object_or_404(Emprestimo, id=id)
        equipamentoEmprestimo = Equipamento.objects.filter(
            nome=emprestimo.emprestimo_equipamento.nome).first()

        equipamentoEmprestimo.status = "Disponivel"

        try:
            emprestimo.delete()
            equipamentoEmprestimo.save()
            messages.add_message(request, messages.SUCCESS,
                                 "O emprestimo foi excluido com sucesso!")

        except ValueError:
            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel deletar o emprestimo")

    return redirect('index')


@login_required
def editarEmprestimo(request, id):

    emprestimo = get_object_or_404(Emprestimo, pk=id)

    context = {}

    colaboradores = Colaborador.objects.all()
    equipamentos = Equipamento.objects.filter(status="Disponivel")
    context['colaboradores'] = colaboradores
    context['equipamentos'] = equipamentos
    context['emprestimo'] = emprestimo

    if request.method == "POST":
        colaborador = request.POST.get("colaborador")
        nomeEquipamento = request.POST.get("nomeEquipamento")
        quantidade = request.POST.get("quantidade")
        dataDevolucao = request.POST.get("data")
        assinaturaColaborador = request.POST.get("assinaturaColaborador")
        assinaturaResponsavel = request.POST.get("assinaturaResponsavel")

        emprestimo = get_object_or_404(Emprestimo, pk=id)
        colaboradorSolicitante = get_object_or_404(
            Colaborador, cpf=colaborador)

        emprestimo.colaborador = colaboradorSolicitante

        equipamentoEmprestimo = Equipamento.objects.filter(
            nome=nomeEquipamento).first()

        if(equipamentoEmprestimo.quantidade < int(quantidade)):
            messages.add_message(request, messages.ERROR,
                                 'Quantidade solicitada indisponivel')
            return render(request, template_name='emprestimo/editarEmprestimo.html', context=context)

        equipamentoAntigo = emprestimo.emprestimo_equipamento

        equipamentoAntigo.status = "Disponivel"
        equipamentoAntigo.quantidade = quantidade

        emprestimo.emprestimo_equipamento = equipamentoEmprestimo
        equipamentoEmprestimo.status = "Emprestado"

        equipamentoEmprestimo.quantidade = quantidade

        if(dataDevolucao):
            emprestimo.data_devolucao = dataDevolucao

        emprestimo.data_encerramento = emprestimo.data_criacao + \
            timedelta(365)

        # Converter assinatura Responsavel
        ar = retornaData(assinaturaResponsavel)

        # Converter assinatura Colaborador
        ac = retornaData(assinaturaColaborador)

        # Nomeando as assinaturas
        nomeRespo = request.user
        nomeColab = emprestimo.colaborador.nome

        # write the decoded data back to original format in  file
        urlRespoAssi = saveMedia(ar, nomeRespo)
        urlColabAssi = saveMedia(ac, nomeColab)

        emprestimo.assinatura_responsavel = urlRespoAssi
        emprestimo.assinatura_colaborador = urlColabAssi

        try:
            equipamentoEmprestimo.save()
            emprestimo.save()
            equipamentoAntigo.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Informações alteradas com sucesso')
        except Exception as Error:
            print(Error)
            messages.add_message(
                request, messages.ERROR, 'Não foi possivel alterar as informações do emprestimo')

    return render(request, template_name='emprestimo/editarEmprestimo.html', context=context)


@login_required
def encerrarEmprestimo(request):

    context = {}
    # Emprestimos
    emprestimos = Emprestimo.objects.all()  # todos
    emp_aberto = Emprestimo.objects.filter(
        status_emprestimo='Aberto').count()  # abertos
    emp_fechado = Emprestimo.objects.filter(
        status_emprestimo='Encerrado').count()  # abertos

    context['emp_aberto'] = emp_aberto
    context['emp_fechado'] = emp_fechado
    context['emprestimos'] = emprestimos

    return render(request, template_name='emprestimo/encerrarEmprestimo.html', context=context)


@login_required
def finalizarEmprestimo(request, id):
    context = {}
    emprestimo = get_object_or_404(Emprestimo, pk=id)
    context['emprestimo'] = emprestimo

    if request.method == "POST":
        emprestimo = get_object_or_404(Emprestimo, pk=id)
        assinaturaColaborador = request.POST.get("assinaturaColaborador")
        assinaturaResponsavel = request.POST.get("assinaturaResponsavel")

        emprestimo.data_devolucao = datetime.today()
        emprestimo.data_encerramento = datetime.today()

        equipamento = Equipamento.objects.filter(
            nome=emprestimo.emprestimo_equipamento.nome).first()

        equipamento.status = "Disponivel"
        equipamento.quantidade = emprestimo.emprestimo_equipamento.quantidade

        emprestimo.status_emprestimo = "Encerrado"

        # Converter assinatura Responsavel
        ar = retornaData(assinaturaResponsavel)

        # Converter assinatura Colaborador
        ac = retornaData(assinaturaColaborador)

        # Nomeando as assinaturas
        nomeRespo = request.user
        nomeColab = emprestimo.colaborador.nome

        # write the decoded data back to original format in  file
        urlRespoAssi = saveMedia(ar, nomeRespo)
        urlColabAssi = saveMedia(ac, nomeColab)

        emprestimo.assinatura_responsavel = urlRespoAssi
        emprestimo.assinatura_colaborador = urlColabAssi

         # Importação do doc que será usado como template
        doc = DocxTemplate("media/modelo/modeloDevo.docx")

        locale.getlocale()
        ('pt_BR', 'UTF-8')

        # this sets the date time formats to es_ES, there are many other options for currency, numbers etc.
        locale.setlocale(locale.LC_TIME, 'pt_BR')
        'pt_BR'

        today = dt.datetime.now()

        dt.datetime(2020, 2, 14, 10, 33, 56, 487228)

        data = today.strftime('%d de %B de %Y')

        def formatcpf(cpf):
            vezes = 0
            novo = ""
            for quantidade in range(11):
                numero = cpf[quantidade]
                novo += numero
                vezes += 1
                if(quantidade == 8):
                    novo += "-"
                    vezes -= 3
                if(vezes == 3):
                    novo += "."
                    vezes -= 3
            return novo

        # Trocar informações pelas do modelo
        conteudo = {
            "nomeColaborador": emprestimo.colaborador.nome,
            "cpf": formatcpf(emprestimo.colaborador.cpf),
            "equipamento": emprestimo.emprestimo_equipamento.nome,
            "n_serie": emprestimo.emprestimo_equipamento.n_serie,
            "data": data
        }

        # Trocar assinatura do responsavel e do colab, pelas do modelo
        doc.replace_pic('Imagem 10', urlColabAssi)
        doc.replace_pic('Imagem 10', urlRespoAssi)

        # Aplicar a troca de informações
        doc.render(conteudo)

        # Gerar um hash de
        signer = TimestampSigner()
        value = signer.sign(emprestimo.colaborador.nome).split(":")[-1]

        nome_arquivo = f"media/termos/termo{value}.docx"

        try:
            doc.save(nome_arquivo)

        except Exception as e1:
            print(e1)
            messages.add_message(request, messages.ERROR,
                                 "Não foi possivel gerar o termo de devolução")
            return render(request, template_name='emprestimo/finalizarEmprestimo.html', context=context)

        novo_termo = TermoDevo()
        novo_termo.colaborador = emprestimo.colaborador
        novo_termo.Emprestimo = emprestimo
        novo_termo.url_termoDevo = nome_arquivo

        try:
            novo_termo.save()
            equipamento.save()
            emprestimo.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Emprestimo finalizado com sucesso')
        except Exception as Error:
            messages.add_message(
                request, messages.ERROR, 'Não foi possivel finalizar o emprestimo')

    return render(request, template_name='emprestimo/finalizarEmprestimo.html', context=context)
