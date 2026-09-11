import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import TipoHabitacion, Habitacion, Cliente, Reserva, Servicio


User = get_user_model()


def _aplicar_ejemplos(form, ejemplos):
    for field_name, ejemplo in ejemplos.items():
        if field_name not in form.fields:
            continue
        field = form.fields[field_name]
        field.widget.attrs.setdefault('placeholder', ejemplo)
        if not field.help_text:
            field.help_text = f'Ejemplo: {ejemplo}'


def _normalizar_rut(rut):
    return rut.strip().replace('.', '').replace(' ', '').replace('‐', '-').upper()


def _digito_verificador_rut(numero):
    suma = 0
    multiplicador = 2
    for digito in reversed(numero):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resultado = 11 - (suma % 11)
    if resultado == 11:
        return '0'
    if resultado == 10:
        return 'K'
    return str(resultado)


def validar_rut_chileno(rut):
    rut_normalizado = _normalizar_rut(rut)
    if not re.fullmatch(r'\d{7,8}-[\dK]', rut_normalizado):
        raise ValidationError('Ingresa un RUT valido con formato 12345678-5.')

    numero, digito = rut_normalizado.split('-')
    if _digito_verificador_rut(numero) != digito:
        raise ValidationError('El RUT ingresado no es valido.')

    return rut_normalizado


def _validar_unico(modelo, campo, valor, instancia, mensaje):
    queryset = modelo.objects.filter(**{f'{campo}__iexact': valor})
    if instancia.pk:
        queryset = queryset.exclude(pk=instancia.pk)
    if queryset.exists():
        raise ValidationError(mensaje)
    return valor


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Ingresa tu usuario',
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        })


class TipoHabitacionForm(forms.ModelForm):
    class Meta:
        model = TipoHabitacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'nombre': 'Suite ejecutiva',
            'descripcion': 'Habitacion amplia con vista al jardin',
            'precio_noche': '85000',
            'capacidad': '2',
            'foto': 'Selecciona una imagen JPG o PNG',
        })

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise ValidationError('El nombre no puede estar vacio.')
        return _validar_unico(
            TipoHabitacion,
            'nombre',
            nombre,
            self.instance,
            'Ya existe un tipo de habitacion con ese nombre.',
        )

    def clean_precio_noche(self):
        precio = self.cleaned_data['precio_noche']
        if precio <= 0:
            raise ValidationError('El precio por noche debe ser mayor que cero.')
        return precio

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad <= 0:
            raise ValidationError('La capacidad debe ser mayor que cero.')
        return capacidad


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'numero': '204',
            'piso': '2',
            'estado': 'Disponible',
            'tipo': 'Selecciona un tipo de habitacion',
        })

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if not numero.strip():
            raise ValidationError('El numero de habitacion no puede estar vacio.')
        return _validar_unico(
            Habitacion,
            'numero',
            numero.strip(),
            self.instance,
            'Ya existe una habitacion con ese numero.',
        )


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'nombre': 'Andres Hueman Ovalle',
            'rut': '20850578-6',
            'email': 'cliente@correo.cl',
            'telefono': '+56935547698',
        })

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut_validado = validar_rut_chileno(rut)
        return _validar_unico(
            Cliente,
            'rut',
            rut_validado,
            self.instance,
            'Ya existe un cliente con ese RUT.',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        return _validar_unico(
            Cliente,
            'email',
            email,
            self.instance,
            'Ya existe un cliente con ese email.',
        )

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if len(telefono.strip()) < 8:
            raise ValidationError('El telefono debe contener al menos 8 caracteres.')
        return telefono.strip()


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ('total',)
        widgets = {
            'check_in': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'check_out': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'cliente': 'Selecciona un cliente',
            'habitacion': 'Selecciona una habitacion',
            'check_in': '2026-06-10',
            'check_out': '2026-06-12',
            'estado': 'Pendiente',
        })

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        cliente = cleaned_data.get('cliente')
        habitacion = cleaned_data.get('habitacion')

        if check_in and check_out and check_out <= check_in:
            raise ValidationError('La fecha de salida debe ser posterior a la de entrada.')

        if cliente and habitacion and check_in and check_out:
            reservas_duplicadas = Reserva.objects.filter(
                cliente=cliente,
                habitacion=habitacion,
                check_in=check_in,
                check_out=check_out,
            ).exclude(pk=self.instance.pk)
            if reservas_duplicadas.exists():
                raise ValidationError('Ya existe una reserva registrada con esos mismos datos.')

            reservas = Reserva.objects.filter(habitacion=habitacion).exclude(pk=self.instance.pk)
            reservas = reservas.exclude(estado='Cancelada')
            existe_solapamiento = reservas.filter(check_in__lt=check_out, check_out__gt=check_in).exists()
            if existe_solapamiento:
                raise ValidationError('La habitacion ya tiene una reserva en ese rango de fechas.')

        return cleaned_data


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'reservas': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'nombre': 'Desayuno buffet',
            'precio': '15000',
            'descripcion': 'Servicio de desayuno para huespedes',
            'reservas': 'Selecciona reservas asociadas',
        })

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise ValidationError('El nombre no puede estar vacio.')
        return _validar_unico(
            Servicio,
            'nombre',
            nombre,
            self.instance,
            'Ya existe un servicio con ese nombre.',
        )


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo electronico')
    first_name = forms.CharField(label='Nombre', max_length=150, required=False)
    last_name = forms.CharField(label='Apellido', max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'username',
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Nombre',
            'autocomplete': 'given-name',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Apellido',
            'autocomplete': 'family-name',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Crea una contraseña segura',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repite la contraseña',
            'autocomplete': 'new-password',
        })

        _aplicar_ejemplos(self, {
            'username': 'cliente_demo',
            'first_name': 'Andres',
            'last_name': 'Hueman',
            'email': 'usuario@correo.cl',
            'password1': 'ClaveSegura2026!',
            'password2': 'ClaveSegura2026!',
        })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Ya existe un usuario con ese correo.')
        return email


class TipoHabitacionFilterForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    capacidad_min = forms.IntegerField(label='Capacidad minima', required=False, min_value=1)
    capacidad_max = forms.IntegerField(label='Capacidad maxima', required=False, min_value=1)
    precio_min = forms.DecimalField(label='Precio minimo', required=False, min_value=0)
    precio_max = forms.DecimalField(label='Precio maximo', required=False, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'q': 'Suite',
            'capacidad_min': '1',
            'capacidad_max': '4',
            'precio_min': '30000',
            'precio_max': '120000',
        })


class HabitacionFilterForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    estado = forms.ChoiceField(label='Estado', required=False, choices=[('', 'Todos')])
    tipo = forms.ModelChoiceField(label='Tipo', required=False, queryset=TipoHabitacion.objects.none(), empty_label='Todos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [('', 'Todos')] + list(Habitacion.ESTADOS)
        self.fields['tipo'].queryset = TipoHabitacion.objects.order_by('nombre')
        _aplicar_ejemplos(self, {
            'q': '204',
            'estado': 'Disponible',
            'tipo': 'Selecciona un tipo',
        })


class ClienteFilterForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'q': '16850587-6',
        })


class ReservaFilterForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    estado = forms.ChoiceField(label='Estado', required=False, choices=[('', 'Todos')])
    check_in_desde = forms.DateField(label='Check in desde', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    check_in_hasta = forms.DateField(label='Check in hasta', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [('', 'Todos')] + list(Reserva.ESTADOS)
        _aplicar_ejemplos(self, {
            'q': 'Andres',
            'estado': 'Confirmada',
            'check_in_desde': '2026-06-01',
            'check_in_hasta': '2026-06-30',
        })


class ServicioFilterForm(forms.Form):
    q = forms.CharField(label='Buscar', required=False)
    precio_min = forms.DecimalField(label='Precio minimo', required=False, min_value=0)
    precio_max = forms.DecimalField(label='Precio maximo', required=False, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_ejemplos(self, {
            'q': 'Desayuno',
            'precio_min': '5000',
            'precio_max': '50000',
        })
