from core.models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    return render(request, template_name='base.html')

def colaborador(request):
    return render(request, template_name='colaborador/colaborador.html')

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
    


def novoEmprestimo(request):
    return render(request, template_name='emprestimo/novoEmprestimo.html')

def encerrarEmprestimo(request):
    return render(request, template_name='emprestimo/encerrarEmprestimo.html')
