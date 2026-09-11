from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from datetime import date

from .forms import ClienteForm, HabitacionForm, ReservaForm, ServicioForm, TipoHabitacionForm, validar_rut_chileno
from .models import Cliente, Habitacion, Reserva, Servicio, TipoHabitacion


class RutChilenoTests(SimpleTestCase):
    def test_acepta_rut_valido_con_formato_simple(self):
        self.assertEqual(validar_rut_chileno('12345678-5'), '12345678-5')

    def test_normaliza_puntos_y_k_mayuscula(self):
        self.assertEqual(validar_rut_chileno('12.345.670-k'), '12345670-K')

    def test_rechaza_rut_con_digito_verificador_incorrecto(self):
        with self.assertRaises(ValidationError):
            validar_rut_chileno('12345678-9')

    def test_rechaza_texto_arbitrario(self):
        with self.assertRaises(ValidationError):
            validar_rut_chileno('rut falso')


class ValidacionesDuplicadosTests(TestCase):
    def setUp(self):
        self.tipo = TipoHabitacion.objects.create(
            nombre='Suite',
            descripcion='Habitacion amplia',
            precio_noche=50000,
            capacidad=2,
        )
        self.habitacion = Habitacion.objects.create(
            numero='101',
            piso=1,
            estado='Disponible',
            tipo=self.tipo,
        )
        self.cliente = Cliente.objects.create(
            nombre='Alicia',
            rut='12345678-5',
            email='alicia@gmail.com',
            telefono='+56911111111',
        )
        self.reserva = Reserva.objects.create(
            cliente=self.cliente,
            habitacion=self.habitacion,
            check_in=date(2026, 6, 10),
            check_out=date(2026, 6, 12),
            estado='Pendiente',
            total=0,
        )
        self.servicio = Servicio.objects.create(
            nombre='Desayuno',
            precio=10000,
            descripcion='Desayuno buffet',
        )

    def test_rechaza_tipo_habitacion_repetido(self):
        form = TipoHabitacionForm(data={
            'nombre': 'suite',
            'descripcion': 'Otra descripcion',
            'precio_noche': 60000,
            'capacidad': 2,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_rechaza_numero_habitacion_repetido(self):
        form = HabitacionForm(data={
            'numero': '101',
            'piso': 2,
            'estado': 'Disponible',
            'tipo': self.tipo.id,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('numero', form.errors)

    def test_rechaza_email_cliente_repetido(self):
        form = ClienteForm(data={
            'nombre': 'Marce',
            'rut': '12345670-K',
            'email': 'ALICIA@gmail.com',
            'telefono': '+56922222222',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_rechaza_reserva_repetida(self):
        form = ReservaForm(data={
            'cliente': self.cliente.id,
            'habitacion': self.habitacion.id,
            'check_in': '2026-06-10',
            'check_out': '2026-06-12',
            'estado': 'Pendiente',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_rechaza_servicio_repetido(self):
        form = ServicioForm(data={
            'nombre': 'desayuno',
            'precio': 12000,
            'descripcion': 'Otro desayuno',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)


class EliminacionHabitacionTests(TestCase):
    def test_no_elimina_habitacion_con_reserva_confirmada(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='ClaveSegura2026!',
        )
        tipo = TipoHabitacion.objects.create(
            nombre='Suite',
            descripcion='Habitacion amplia',
            precio_noche=50000,
            capacidad=2,
        )
        habitacion = Habitacion.objects.create(
            numero='101',
            piso=1,
            estado='Disponible',
            tipo=tipo,
        )
        cliente = Cliente.objects.create(
            nombre='Alicia',
            rut='12345678-5',
            email='alicia@gmail.com',
            telefono='+56911111111',
        )
        Reserva.objects.create(
            cliente=cliente,
            habitacion=habitacion,
            check_in=date(2026, 6, 10),
            check_out=date(2026, 6, 12),
            estado='Confirmada',
            total=0,
        )

        client = Client()
        client.force_login(user)
        response = client.post(reverse('eliminar', args=['habitaciones', habitacion.id]))

        self.assertRedirects(response, reverse('listar', args=['habitaciones']))
        self.assertTrue(Habitacion.objects.filter(id=habitacion.id).exists())


class ClientesSoloSuperusuarioTests(TestCase):
    def setUp(self):
        self.normal_user = get_user_model().objects.create_user(
            username='operador',
            email='operador@example.com',
            password='ClaveSegura2026!',
        )
        self.superuser = get_user_model().objects.create_superuser(
            username='adminclientes',
            email='adminclientes@example.com',
            password='ClaveSegura2026!',
        )
        Cliente.objects.create(
            nombre='Alicia',
            rut='12345678-5',
            email='alicia@gmail.com',
            telefono='+56911111111',
        )

    def test_usuario_normal_no_puede_listar_clientes(self):
        client = Client()
        client.force_login(self.normal_user)
        response = client.get(reverse('listar', args=['clientes']))

        self.assertRedirects(response, reverse('dashboard'))

    def test_usuario_normal_no_ve_accesos_a_clientes_en_dashboard(self):
        client = Client()
        client.force_login(self.normal_user)
        response = client.get(reverse('dashboard'))
        html = response.content.decode()

        self.assertNotIn('Ver clientes', html)
        self.assertNotIn('>Clientes<', html)

    def test_superusuario_puede_listar_clientes(self):
        client = Client()
        client.force_login(self.superuser)
        response = client.get(reverse('listar', args=['clientes']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alicia')
