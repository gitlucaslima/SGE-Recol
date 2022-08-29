from django.shortcuts import render

def index(request):
    return render(request, template_name='base.html')

def colaborador(request):
    return render(request, template_name='colaborador/colaborador.html')

def equipamento(request):
    return render(request, template_name='equipamento/equipamento.html')

def novoEmprestimo(request):
    return render(request, template_name='emprestimo/novoEmprestimo.html')

def encerrarEmprestimo(request):
    return render(request, template_name='emprestimo/encerrarEmprestimo.html')
