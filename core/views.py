from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, template_name='base.html')

def colaborador(request):
    return render(request, template_name='colaborador/colaborador.html')

def equipamento(request):
    return render(request, template_name='equipamento/equipamento.html')
