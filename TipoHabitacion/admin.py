from django.contrib import admin
from .models import TipoHabitacion, Habitacion, Cliente, Reserva, Servicio

admin.site.register(TipoHabitacion)
admin.site.register(Habitacion)
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Servicio)
