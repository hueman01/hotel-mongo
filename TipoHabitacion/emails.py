"""Envio de correos automaticos del sistema de hotel.

Los correos nunca deben impedir el flujo de la web: si el SMTP falla
(cae la red, credenciales invalidas, etc.) solo se registra en el log
y la peticion sigue normal. Para activarlos configure en el .env o en
Render:

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=micorreo@gmail.com
    EMAIL_HOST_PASSWORD=clave-de-aplicacion-generada
    EMAIL_USE_TLS=1
    DEFAULT_FROM_EMAIL=Hotel H.H. <micorreo@gmail.com>
"""

import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _enviar(destino, asunto, plantilla, contexto):
    """Envia un correo con version texto + html. Devuelve True si sale."""
    if not getattr(settings, 'EMAILS_ENABLED', False):
        return False

    if not destino:
        logger.warning('Correo "%s" descartado: sin destinatario.', asunto)
        return False

    try:
        cuerpo_texto = render_to_string(plantilla + '.txt', contexto)
        cuerpo_html = render_to_string(plantilla + '.html', contexto)
        mensaje = EmailMultiAlternatives(
            subject=asunto,
            body=cuerpo_texto.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destino],
        )
        mensaje.attach_alternative(cuerpo_html, 'text/html')
        mensaje.send()
        logger.info('Correo "%s" enviado a %s', asunto, destino)
        return True
    except Exception:
        logger.warning(
            'No fue posible enviar el correo "%s" a %s',
            asunto,
            destino,
            exc_info=True,
        )
        return False


def enviar_bienvenida(usuario, cliente=None):
    """Correo de bienvenida al finalizar el registro."""
    nombre = (
        f'{usuario.first_name} {usuario.last_name}'.strip()
        or (cliente.nombre if cliente else '')
        or usuario.username
    )
    contexto = {
        'nombre': nombre,
        'username': usuario.username,
        'cliente': cliente,
    }
    destino = (cliente.email if cliente else '') or usuario.email
    return _enviar(
        destino,
        '[Hotel H.H.] Bienvenido al sistema',
        'emails/bienvenida',
        contexto,
    )


def enviar_confirmacion_reserva(reserva):
    """Correo con el detalle de una reserva recien creada."""
    cliente = reserva.cliente
    habitacion = reserva.habitacion

    noches = 0
    if reserva.check_in and reserva.check_out:
        noches = (reserva.check_out - reserva.check_in).days

    contexto = {
        'cliente': cliente,
        'reserva': reserva,
        'habitacion': habitacion,
        'tipo': getattr(habitacion, 'tipo', None),
        'noches': noches,
        'total': reserva.total,
    }
    return _enviar(
        cliente.email,
        f'[Hotel H.H.] Reserva de la habitacion {habitacion.numero}',
        'emails/reserva_confirmacion',
        contexto,
    )
