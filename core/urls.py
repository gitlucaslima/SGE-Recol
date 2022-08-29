from django.urls import path

from core.views import colaborador, equipamento, index

urlpatterns = [
    path('', index, name='index'),
    path('colaborador/', colaborador, name='colaborador'),
    path('equipamento/', equipamento, name='equipamento')

]
