from django.contrib import admin
from .models import *

admin.site.register(Patente)
admin.site.register(Perfil)
admin.site.register(Bombeiro)
admin.site.register(Viatura)
admin.site.register(Manutencao)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(EventoBombeiro)
admin.site.register(ViaturaEvento)
admin.site.register(Ocorrencia)
admin.site.register(Escala)
admin.site.register(EscalaBombeiro)
admin.site.register(Treinamento)
admin.site.register(TreinamentoBombeiro)