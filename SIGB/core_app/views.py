from .forms import FormBombeiro
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bombeiro, Viatura, Ocorrencia, Manutencao, Escala, Evento, Treinamento, Patente, TipoEvento


def dashboard(request):
    return render(request, "dashboard.html")


def agenda(request):
    agenda_tz = timezone.now()

    proximos_eventos = Evento.objects.filter(data_inicio__gte=agenda_tz).order_by('data_inicio')
    ocorrencia_aberta = Ocorrencia.objects.filter(status='Em Atendimento').order_by('-id')
    ocorrencia_fechada = Ocorrencia.objects.filter(status='Finalizada').order_by('-id')
    eventos_fechados = Evento.objects.filter(data_inicio__lt=agenda_tz)

    historico = []

    for i in eventos_fechados:
        historico.append({
            'data': i.data_inicio,
            'tipo': f"EVENTO: {i.titulo}",
            'badge': 'badge-info',
            'info': i.local
        })

    for i in ocorrencia_fechada:
        historico.append({
            'data': None,
            'tipo': f"OCORRÊNCIA: {i.tipo}",
            'badge': 'badge-danger',
            'info': f" Gravidade {i.gravidade}"
        })

    return render(request, "agenda.html", {
        'evento': proximos_eventos,
        'aberto':  ocorrencia_aberta,
        'historico': historico
    })


def historico(request):
    filtrar_modulo = request.GET.get('modulo')
    buscar_texto = request.GET.get('busca')

    todos_modelos = [Bombeiro, Viatura, Ocorrencia, Manutencao, Escala, Evento, Patente,Treinamento, TipoEvento]
    logs_processados = []

    for modelo in todos_modelos:
        nome_mod = modelo._meta.verbose_name.upper()
        
        if filtrar_modulo and filtrar_modulo != nome_mod:
            continue

        for log in modelo.historico.all():
            identificador = (
                getattr(log, 'nome_completo', None) or 
                getattr(log, 'prefixo', None) or 
                getattr(log, 'titulo', None) or 
                getattr(log, 'nome', None) or 
                getattr(log, 'tipo', None) or 
                f"ID: {log.id}"
            )

            if buscar_texto and buscar_texto.lower() not in str(identificador).lower():
                continue

            log.modulo_display = nome_mod
            log.identificador_display = identificador
            logs_processados.append(log)

    logs_completos = sorted(
        logs_processados, 
        key=lambda x: x.history_date, 
        reverse=True
    )[:100]

    lista_modulos = [m._meta.verbose_name.upper() for m in todos_modelos]

    context = {
        'logs': logs_completos,
        'lista_modulos': sorted(lista_modulos),
        'filtro_modulo': filtrar_modulo,
        'busca_texto': buscar_texto
    }
    return render(request, 'historico.html', context)


def bombeiros(request):

    lista = Bombeiro.objects.all().select_related('patente', 'perfil')
    form = FormBombeiro()

    if request.method == 'POST':

        if 'cadastrar' in request.POST:
            form = FormBombeiro(request.POST)

            if form.is_valid():
                form.save()

                return redirect('core_app:bombeiros')
    
    elif 'editar' in request.POST:
        id_bombeiro = request.POST.get('id_bombeiro')

        instancia = get_object_or_404(Bombeiro, id=id_bombeiro)
        form_editado = FormBombeiro(request.POST, instance=instancia)

        if form_editado.is_valid():
            form_editado.save()

            return redirect('core_app:bombeiros')
    
    elif 'excluir' in request.POST:
        id_bombeiro = request.POST.get('id_bombeiro')

        instancia = get_object_or_404(Bombeiro, id=id_bombeiro)
        instancia.delete()

        return redirect('core_app:bombeiros')


    return render(request, "bombeiros.html", {'lista': lista, 'form': form})


def manutencoes(request):
    return render(request, "manutencoes.html")


def viaturas(request):
    return render(request, "viaturas.html")
