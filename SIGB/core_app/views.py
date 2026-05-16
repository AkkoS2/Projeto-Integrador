from django.utils import timezone
from .forms import EscalaForm, ManutencaoForm, BombeiroForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bombeiro, Viatura, Ocorrencia, Manutencao, Escala, Evento, Treinamento, Patente, TipoEvento, EscalaBombeiro


def dashboard(request):

    total_bombeiros = Bombeiro.objects.count()
    viaturas_ativas = Viatura.objects.filter(status='Operacional').count()
    viaturas_manutencao = Manutencao.objects.filter(status='Em Andamento').count()
    ocorrencias_vivas = Ocorrencia.objects.filter(status='Em Atendimento').count()
    escalas = Escala.objects.filter(data_inicio__gte=timezone.now().date())[:5]

    context = {
        'total_bombeiros': total_bombeiros,
        'viaturas_ativas': viaturas_ativas,
        'viaturas_manutencao': viaturas_manutencao,
        'ocorrencias_vivas': ocorrencias_vivas,
        'escalas_hoje': escalas
    }

    return render(request, "dashboard.html", context)


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
    form = BombeiroForm()

    if request.method == 'POST':

        if 'btn_salvar' in request.POST:
            id_bombeiro = request.POST.get('id_bombeiro')

            if id_bombeiro:
                instancia = get_object_or_404(Bombeiro, id=id_bombeiro)
                form = BombeiroForm(request.POST, instance=instancia)
            
            else:
                form = BombeiroForm(request.POST)
            
            if form.is_valid():
                form.save()

                return redirect('core_app:bombeiros')
        
        elif 'btn_excluir' in request.POST:
            id_bombeiro = request.POST.get('id_bombeiro')
            bombeiro = get_object_or_404(Bombeiro, id=id_bombeiro)
            bombeiro.delete()

            return redirect('core_app:bombeiros')


    return render(request, "bombeiros.html", {'lista': lista, 'form': form})


def frotas(request):

    lista = Viatura.objects.all().prefetch_related('manutencao_set')
    form = ManutencaoForm()

    if request.method == 'POST':

        if 'btn_manutencao' in request.POST:
            id_viatura = request.POST.get('id_viatura')
            viatura_obj = get_object_or_404(Viatura, id=id_viatura)
            form = ManutencaoForm(request.POST)

            if form.is_valid():
                nova_manutencao = form.save(commit=False)
                nova_manutencao.viatura = viatura_obj
                nova_manutencao.save()

                novo_status = request.POST.get('novo_status_viatura')

                if novo_status:
                    viatura_obj.status = novo_status
                    viatura_obj.save()

                return redirect('core_app:frotas')

    return render(request, "frotas.html",{
        'viaturas': lista,
        'form': form
    })


def escalas(request):

    escalas = Escala.objects.all().prefetch_related('escalabombeiro_set__bombeiro')
    form = EscalaForm()

    if request.method == 'POST':

        if 'btn_cadastrar' in request.POST:
            form = EscalaForm(request.POST)

            if form.is_valid():
                nova_escala = form.save()
                bombeiros_escolhidos = form.cleaned_data['bombeiros']

                for b in bombeiros_escolhidos:
                    EscalaBombeiro.objects.create(escala=nova_escala, bombeiro=b)
                
                return redirect('core_app:escalas')
    
        elif 'btn_excluir' in request.POST:

            id_escala = request.POST.get('id_escala')
            get_object_or_404(Escala, id=id_escala).delete()
            return redirect('core_app:escalas')

    return render(request, "escala.html", {
        'escala': escalas,
        'form': form})
