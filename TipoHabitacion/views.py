import base64
from io import BytesIO

from bson import ObjectId
from bson.errors import InvalidId
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from matplotlib import pyplot as plt

from .forms import (
    ClienteFilterForm,
    ClienteForm,
    LoginForm,
    HabitacionFilterForm,
    HabitacionForm,
    RegistroForm,
    ReservaFilterForm,
    ReservaForm,
    ServicioFilterForm,
    ServicioForm,
    TipoHabitacionFilterForm,
    TipoHabitacionForm,
)
from .models import Cliente, Habitacion, Reserva, Servicio, TipoHabitacion


MODEL_CONFIG = {
    'tipos': {
        'model': TipoHabitacion,
        'form': TipoHabitacionForm,
        'filter_form': TipoHabitacionFilterForm,
        'title': 'Tipos de habitacion',
        'singular': 'tipo de habitacion',
        'fields': ['nombre', 'descripcion', 'precio_noche', 'capacidad', 'foto'],
        'headers': ['Nombre', 'Descripcion', 'Precio noche', 'Capacidad', 'Foto'],
        'search_fields': ['nombre', 'descripcion'],
    },
    'habitaciones': {
        'model': Habitacion,
        'form': HabitacionForm,
        'filter_form': HabitacionFilterForm,
        'title': 'Habitaciones',
        'singular': 'habitacion',
        'fields': ['numero', 'piso', 'estado', 'tipo'],
        'headers': ['Numero', 'Piso', 'Estado', 'Tipo'],
        'search_fields': ['numero', 'tipo__nombre'],
    },
    'clientes': {
        'model': Cliente,
        'form': ClienteForm,
        'filter_form': ClienteFilterForm,
        'title': 'Clientes',
        'singular': 'cliente',
        'fields': ['nombre', 'rut', 'email', 'telefono'],
        'headers': ['Nombre', 'RUT', 'Email', 'Telefono'],
        'search_fields': ['nombre', 'rut', 'email', 'telefono'],
    },
    'reservas': {
        'model': Reserva,
        'form': ReservaForm,
        'filter_form': ReservaFilterForm,
        'title': 'Reservas',
        'singular': 'reserva',
        'fields': ['cliente', 'habitacion', 'check_in', 'check_out', 'estado', 'total'],
        'headers': ['Cliente', 'Habitacion', 'Check in', 'Check out', 'Estado', 'Total'],
        'search_fields': ['cliente__nombre', 'cliente__rut', 'habitacion__numero'],
    },
    'servicios': {
        'model': Servicio,
        'form': ServicioForm,
        'filter_form': ServicioFilterForm,
        'title': 'Servicios',
        'singular': 'servicio',
        'fields': ['nombre', 'precio', 'descripcion', 'reservas'],
        'headers': ['Nombre', 'Precio', 'Descripcion', 'Reservas'],
        'search_fields': ['nombre', 'descripcion'],
    },
}


def _get_config(modelo):
    return MODEL_CONFIG[modelo]


def _get_object_or_404(modelo, pk):
    """Convierte el pk (string) a ObjectId y busca el objeto, o lanza 404."""
    try:
        object_id = ObjectId(pk)
    except (InvalidId, TypeError):
        raise Http404('ID invalido')
    return get_object_or_404(_select_queryset(modelo), pk=object_id)


def _permission_name(model, action):
    meta = model._meta
    return f'{meta.app_label}.{action}_{meta.model_name}'


def _has_permission(user, model, action):
    if model is Cliente:
        return user.is_superuser
    return user.is_superuser or user.has_perm(_permission_name(model, action))


def _deny(request, message_text, target='dashboard'):
    messages.error(request, message_text)
    return redirect(target)


def _cannot_delete(objeto, modelo):
    if modelo == 'habitaciones' and objeto.reservas.filter(estado='Confirmada').exists():
        return 'No se puede eliminar la habitacion porque tiene una reserva confirmada.'
    return None


def _porcentaje(valor, total):
    if not total:
        return 0
    return min(round((valor / total) * 100, 1), 100)


def _filter_query_string(request):
    params = request.GET.copy()
    params.pop('page', None)
    return params.urlencode()


def _select_queryset(modelo):
    queryset = _get_config(modelo)['model'].objects.all()
    if modelo == 'habitaciones':
        return queryset.select_related('tipo')
    if modelo == 'reservas':
        return queryset.select_related('cliente', 'habitacion', 'habitacion__tipo')
    if modelo == 'servicios':
        return queryset.prefetch_related('reservas')
    return queryset


def _search_queryset(queryset, search_fields, term):
    if not term:
        return queryset

    query = Q()
    for field in search_fields:
        query |= Q(**{f'{field}__icontains': term})
    return queryset.filter(query)


def _apply_filters(modelo, queryset, cleaned_data):
    q = cleaned_data.get('q')
    queryset = _search_queryset(queryset, _get_config(modelo)['search_fields'], q)

    if modelo == 'tipos':
        capacidad_min = cleaned_data.get('capacidad_min')
        capacidad_max = cleaned_data.get('capacidad_max')
        precio_min = cleaned_data.get('precio_min')
        precio_max = cleaned_data.get('precio_max')
        if capacidad_min is not None:
            queryset = queryset.filter(capacidad__gte=capacidad_min)
        if capacidad_max is not None:
            queryset = queryset.filter(capacidad__lte=capacidad_max)
        if precio_min is not None:
            queryset = queryset.filter(precio_noche__gte=precio_min)
        if precio_max is not None:
            queryset = queryset.filter(precio_noche__lte=precio_max)

    elif modelo == 'habitaciones':
        estado = cleaned_data.get('estado')
        tipo = cleaned_data.get('tipo')
        if estado:
            queryset = queryset.filter(estado=estado)
        if tipo:
            queryset = queryset.filter(tipo=tipo)

    elif modelo == 'reservas':
        estado = cleaned_data.get('estado')
        check_in_desde = cleaned_data.get('check_in_desde')
        check_in_hasta = cleaned_data.get('check_in_hasta')
        if estado:
            queryset = queryset.filter(estado=estado)
        if check_in_desde:
            queryset = queryset.filter(check_in__gte=check_in_desde)
        if check_in_hasta:
            queryset = queryset.filter(check_in__lte=check_in_hasta)

    elif modelo == 'servicios':
        precio_min = cleaned_data.get('precio_min')
        precio_max = cleaned_data.get('precio_max')
        if precio_min is not None:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max is not None:
            queryset = queryset.filter(precio__lte=precio_max)

    return queryset


def _filtered_queryset(modelo, request):
    config = _get_config(modelo)
    queryset = _select_queryset(modelo)
    form = config['filter_form'](request.GET or None)
    if form.is_valid():
        queryset = _apply_filters(modelo, queryset, form.cleaned_data)
    return queryset, form


def _value(obj, field):
    value = getattr(obj, field)
    if field == 'foto':
        return value.url if value else 'Sin foto'
    if field == 'reservas':
        return ', '.join(str(r) for r in value.all()) or 'Sin reservas'
    return value


def _export_fields(config, modelo, formato):
    headers = config['headers']
    fields = config['fields']
    if formato == 'pdf' and modelo == 'tipos':
        headers = [header for header, field in zip(headers, fields) if field != 'foto']
        fields = [field for field in fields if field != 'foto']
    return headers, fields


def _build_dashboard_chart():
    conteos = {
        estado: Reserva.objects.filter(estado=estado).count()
        for estado, _ in Reserva.ESTADOS
    }
    labels = list(conteos.keys()) or ['Sin datos']
    values = list(conteos.values()) or [0]

    fig, ax = plt.subplots(figsize=(8.4, 6.2))
    colors = ['#243b78', '#a33257', '#f59e0b', '#10b981']
    bars = ax.bar(labels, values, color=colors[:len(labels)] or ['#243b78'])
    ax.set_title('Reservas por estado')
    ax.set_ylabel('Cantidad')
    ax.grid(axis='y', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar, value in zip(bars, values):
        ax.annotate(
            str(value),
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha='center',
            va='bottom',
            fontsize=9,
        )

    buffer = BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


def inicio(request):
    return render(request, 'hotel/inicio.html')


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request=request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        messages.success(request, f'Bienvenido, {user.username}.')
        return redirect('dashboard')
    if request.method == 'POST':
        messages.error(request, 'No fue posible iniciar sesion. Revisa tus credenciales.')

    return render(request, 'registration/login.html', {'form': form})


@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistroForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            cliente_group, _ = Group.objects.get_or_create(name='Clientes')
            user.groups.add(cliente_group)
            messages.success(request, 'Usuario registrado correctamente. Ya puedes iniciar sesion.')
            return redirect('login')
        messages.error(request, 'Corrige los campos marcados en el formulario.')

    return render(request, 'registration/register.html', {'form': form})


@login_required
@never_cache
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Sesion cerrada correctamente.')
    return redirect('login')


@login_required
@never_cache
def dashboard(request):
    total_habitaciones = Habitacion.objects.count()
    habitaciones_disponibles = Habitacion.objects.filter(estado='Disponible').count()
    habitaciones_ocupadas = Habitacion.objects.filter(estado='Ocupada').count()
    habitaciones_mantenimiento = Habitacion.objects.filter(estado='Mantenimiento').count()

    total_reservas = Reserva.objects.count()
    reservas_pendientes = Reserva.objects.filter(estado='Pendiente').count()
    reservas_confirmadas = Reserva.objects.filter(estado='Confirmada').count()
    reservas_finalizadas = Reserva.objects.filter(estado='Finalizada').count()
    reservas_canceladas = Reserva.objects.filter(estado='Cancelada').count()

    ocupacion = round((habitaciones_ocupadas / total_habitaciones) * 100, 1) if total_habitaciones else 0
    tipos_url = reverse('listar', kwargs={'modelo': 'tipos'})
    habitaciones_url = reverse('listar', kwargs={'modelo': 'habitaciones'})
    clientes_url = reverse('listar', kwargs={'modelo': 'clientes'})
    reservas_url = reverse('listar', kwargs={'modelo': 'reservas'})

    metricas = [
        {'label': 'Tipos de habitacion', 'value': TipoHabitacion.objects.count(), 'href': tipos_url},
        {'label': 'Habitaciones', 'value': total_habitaciones, 'href': habitaciones_url},
        {'label': 'Reservas', 'value': total_reservas, 'href': reservas_url},
        {'label': 'Ocupacion', 'value': f'{ocupacion}%'},
        {'label': 'Pendientes', 'value': reservas_pendientes, 'href': f'{reservas_url}?estado=Pendiente'},
    ]
    if request.user.is_superuser:
        metricas.insert(2, {'label': 'Clientes', 'value': Cliente.objects.count(), 'href': clientes_url})

    resumen_circular = [
        {
            'label': 'Habitaciones disponibles',
            'current': habitaciones_disponibles,
            'min': 0,
            'max': total_habitaciones,
            'aria_max': max(total_habitaciones, 1),
            'value': habitaciones_disponibles,
            'progress': _porcentaje(habitaciones_disponibles, total_habitaciones),
            'detail': f'{habitaciones_disponibles} de {total_habitaciones}',
            'color': '#10b981',
            'soft_color': '#ecfdf5',
            'href': f'{habitaciones_url}?estado=Disponible',
        },
        {
            'label': 'Habitaciones ocupadas',
            'current': habitaciones_ocupadas,
            'min': 0,
            'max': total_habitaciones,
            'aria_max': max(total_habitaciones, 1),
            'value': habitaciones_ocupadas,
            'progress': _porcentaje(habitaciones_ocupadas, total_habitaciones),
            'detail': f'{habitaciones_ocupadas} de {total_habitaciones}',
            'color': '#ef4444',
            'soft_color': '#fef2f2',
            'href': f'{habitaciones_url}?estado=Ocupada',
        },
        {
            'label': 'En mantenimiento',
            'current': habitaciones_mantenimiento,
            'min': 0,
            'max': total_habitaciones,
            'aria_max': max(total_habitaciones, 1),
            'value': habitaciones_mantenimiento,
            'progress': _porcentaje(habitaciones_mantenimiento, total_habitaciones),
            'detail': f'{habitaciones_mantenimiento} de {total_habitaciones}',
            'color': '#f59e0b',
            'soft_color': '#fffbeb',
            'href': f'{habitaciones_url}?estado=Mantenimiento',
        },
        {
            'label': 'Reservas pendientes',
            'current': reservas_pendientes,
            'min': 0,
            'max': total_reservas,
            'aria_max': max(total_reservas, 1),
            'value': reservas_pendientes,
            'progress': _porcentaje(reservas_pendientes, total_reservas),
            'detail': f'{reservas_pendientes} de {total_reservas}',
            'color': '#8b5cf6',
            'soft_color': '#f5f3ff',
            'href': f'{reservas_url}?estado=Pendiente',
        },
        {
            'label': 'Ocupacion',
            'current': ocupacion,
            'min': 0,
            'max': 100,
            'aria_max': 100,
            'value': f'{str(ocupacion).replace(".", ",")}%',
            'progress': ocupacion,
            'detail': f'{str(ocupacion).replace(".", ",")}% de 100%',
            'color': '#2563eb',
            'soft_color': '#eff6ff',
        },
        {
            'label': 'Total reservas',
            'current': total_reservas,
            'min': 0,
            'max': total_reservas,
            'aria_max': max(total_reservas, 1),
            'value': total_reservas,
            'progress': 100 if total_reservas else 0,
            'detail': f'{total_reservas} de {total_reservas}',
            'color': '#06b6d4',
            'soft_color': '#ecfeff',
            'href': reservas_url,
        },
    ]

    if request.user.is_superuser:
        ultimas_reservas = Reserva.objects.select_related('cliente', 'habitacion').order_by('-id')[:5]
        ultimos_clientes = Cliente.objects.order_by('-id')[:5]
    else:
        ultimas_reservas = []
        ultimos_clientes = []

    ultimos_tipos = TipoHabitacion.objects.order_by('-id')[:4]
    ultimas_habitaciones = Habitacion.objects.select_related('tipo').order_by('-id')[:4]
    chart = _build_dashboard_chart()

    return render(request, 'hotel/dashboard.html', {
        'metricas': metricas,
        'habitaciones_disponibles': habitaciones_disponibles,
        'habitaciones_ocupadas': habitaciones_ocupadas,
        'habitaciones_mantenimiento': habitaciones_mantenimiento,
        'reservas_pendientes': reservas_pendientes,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_finalizadas': reservas_finalizadas,
        'reservas_canceladas': reservas_canceladas,
        'total_reservas': total_reservas,
        'ocupacion': ocupacion,
        'resumen_circular': resumen_circular,
        'mostrar_datos_admin': request.user.is_superuser,
        'ultimas_reservas': ultimas_reservas,
        'ultimos_clientes': ultimos_clientes,
        'ultimos_tipos': ultimos_tipos,
        'ultimas_habitaciones': ultimas_habitaciones,
        'chart_base64': chart,
    })


@login_required
@never_cache
def listar(request, modelo):
    config = _get_config(modelo)
    if not _has_permission(request.user, config['model'], 'view'):
        return _deny(request, 'No tienes permiso para ver estos datos.')

    queryset, filter_form = _filtered_queryset(modelo, request)
    paginator = Paginator(queryset, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    query_string = _filter_query_string(request)
    start_index = page_obj.start_index() if paginator.count else 0
    end_index = page_obj.end_index() if paginator.count else 0

    return render(request, 'hotel/lista.html', {
        'modelo': modelo,
        'config': config,
        'page_obj': page_obj,
        'fields': config['fields'],
        'filter_form': filter_form,
        'query_string': query_string,
        'total_resultados': paginator.count,
        'rango_resultados': f'{start_index}-{end_index}' if paginator.count else '0-0',
        'can_add': _has_permission(request.user, config['model'], 'add'),
        'can_change': _has_permission(request.user, config['model'], 'change'),
        'can_delete': _has_permission(request.user, config['model'], 'delete'),
    })


@login_required
@never_cache
def detalle(request, modelo, pk):
    config = _get_config(modelo)
    objeto = _get_object_or_404(modelo, pk)
    if not _has_permission(request.user, config['model'], 'view'):
        return _deny(request, 'No tienes permiso para ver este registro.')

    datos = [(header, _value(objeto, field)) for header, field in zip(config['headers'], config['fields'])]
    if modelo == 'habitaciones':
        datos.append(('Foto', objeto.tipo.foto if objeto.tipo.foto else 'Sin foto'))

    return render(request, 'hotel/detalle.html', {
        'modelo': modelo,
        'config': config,
        'objeto': objeto,
        'datos': datos,
        'can_change': _has_permission(request.user, config['model'], 'change'),
        'can_delete': _has_permission(request.user, config['model'], 'delete'),
    })


@login_required
@never_cache
def crear(request, modelo):
    config = _get_config(modelo)
    if not _has_permission(request.user, config['model'], 'add'):
        return _deny(request, 'No tienes permiso para crear registros.')

    form = config['form'](request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'El {config["singular"]} se creo correctamente.')
        return redirect('listar', modelo=modelo)
    if request.method == 'POST':
        messages.error(request, f'No fue posible crear el {config["singular"]}. Revisa los datos ingresados.')

    return render(request, 'hotel/formulario.html', {
        'modelo': modelo,
        'config': config,
        'form': form,
        'accion': 'Crear',
    })


@login_required
@never_cache
def editar(request, modelo, pk):
    config = _get_config(modelo)
    if not _has_permission(request.user, config['model'], 'change'):
        return _deny(request, 'No tienes permiso para editar registros.')

    objeto = _get_object_or_404(modelo, pk)
    form = config['form'](request.POST or None, request.FILES or None, instance=objeto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'El {config["singular"]} se actualizo correctamente.')
        return redirect('listar', modelo=modelo)
    if request.method == 'POST':
        messages.error(request, f'No fue posible actualizar el {config["singular"]}. Revisa los datos ingresados.')

    return render(request, 'hotel/formulario.html', {
        'modelo': modelo,
        'config': config,
        'form': form,
        'accion': 'Editar',
    })


@login_required
@never_cache
def eliminar(request, modelo, pk):
    config = _get_config(modelo)
    if not _has_permission(request.user, config['model'], 'delete'):
        return _deny(request, 'No tienes permiso para eliminar registros.')

    objeto = _get_object_or_404(modelo, pk)
    mensaje_bloqueo = _cannot_delete(objeto, modelo)
    if mensaje_bloqueo:
        messages.error(request, mensaje_bloqueo)
        return redirect('listar', modelo=modelo)

    if request.method == 'POST':
        objeto.delete()
        messages.warning(request, f'El {config["singular"]} fue eliminado correctamente.')
        return redirect('listar', modelo=modelo)

    return render(request, 'hotel/confirmar_eliminar.html', {
        'modelo': modelo,
        'config': config,
        'objeto': objeto,
    })


@login_required
@never_cache
def exportar_excel(request, modelo):
    config = _get_config(modelo)
    if not _has_permission(request.user, config['model'], 'view'):
        return _deny(request, 'No tienes permiso para exportar estos datos.')

    queryset, _ = _filtered_queryset(modelo, request)

    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = config['title'][:31]
    headers, fields = _export_fields(config, modelo, 'excel')
    ws.append(headers)

    for obj in queryset:
        ws.append([str(_value(obj, field)) for field in fields])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{modelo}_filtrado.xlsx"'
    wb.save(response)
    return response


@login_required
@never_cache
def exportar_pdf(request, modelo):
    config = _get_config(modelo)
    if not _has_permission(request.user, config['model'], 'view'):
        return _deny(request, 'No tienes permiso para exportar estos datos.')

    queryset, _ = _filtered_queryset(modelo, request)

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{modelo}_filtrado.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter), leftMargin=28, rightMargin=28)
    styles = getSampleStyleSheet()
    cell_style = styles['BodyText']
    cell_style.fontName = 'Helvetica'
    cell_style.fontSize = 8
    cell_style.leading = 10
    elements = [
        Paragraph(config['title'], styles['Title']),
        Paragraph('Reporte generado desde el sistema.', styles['Normal']),
        Spacer(1, 12),
    ]

    headers, fields = _export_fields(config, modelo, 'pdf')
    data = [headers]
    for obj in queryset:
        data.append([Paragraph(str(_value(obj, field)), cell_style) for field in fields])

    if len(data) == 1:
        data.append(['Sin resultados'] + [''] * (len(headers) - 1))

    col_widths = None
    if modelo == 'tipos':
        col_widths = [120, 430, 85, 65]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dbeafe')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(table)
    doc.build(elements)
    return response


def custom_404(request, exception):
    return render(request, '404.html', status=404)