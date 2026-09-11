from django.db import models


class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    foto = models.ImageField(upload_to='habitaciones/', blank=True, null=True)
   

    class Meta:
        db_table = 'Tipo de habitación'  
    
    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    ESTADOS = [
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Mantenimiento', 'Mantenimiento'),
    ]
    numero = models.CharField(max_length=10, unique=True)
    piso = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Disponible')
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE, related_name='habitaciones')

    class Meta:
        db_table = 'Habitación'
        ordering = ['numero']

    def __str__(self):
        return f'Habitación {self.numero}'


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

    class Meta:
        db_table = 'Cliente'       
        

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='reservas')
    check_in = models.DateField()
    check_out = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Reserva'

    def _estado_habitacion(self):
        return 'Ocupada' if self.estado == 'Confirmada' else 'Disponible'

    def calcular_total(self):
        if not self.habitacion_id or not self.check_in or not self.check_out:
            return self.total

        noches = (self.check_out - self.check_in).days
        if noches <= 0:
            return 0

        return self.habitacion.tipo.precio_noche * noches

    def _sincronizar_habitacion(self, habitacion=None):
        habitacion = habitacion or self.habitacion
        if habitacion is None:
            return

        estado_deseado = self._estado_habitacion()
        if habitacion.estado != estado_deseado:
            habitacion.estado = estado_deseado
            habitacion.save(update_fields=['estado'])

    def save(self, *args, **kwargs):
        habitacion_anterior_id = None

        if self.pk:
            habitacion_anterior_id = Reserva.objects.only('habitacion_id').get(pk=self.pk).habitacion_id

        self.total = self.calcular_total()
        super().save(*args, **kwargs)

        if habitacion_anterior_id and habitacion_anterior_id != self.habitacion_id:
            habitacion_anterior = Habitacion.objects.get(pk=habitacion_anterior_id)
            habitacion_anterior.estado = 'Disponible'
            habitacion_anterior.save(update_fields=['estado'])

        self._sincronizar_habitacion()

    def delete(self, *args, **kwargs):
        habitacion = self.habitacion
        super().delete(*args, **kwargs)
        if habitacion and habitacion.estado != 'Disponible':
            habitacion.estado = 'Disponible'
            habitacion.save(update_fields=['estado'])

    def __str__(self):
        return f'Reserva de {self.cliente}'


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    reservas = models.ManyToManyField(Reserva, related_name='servicios', blank=True)

    class Meta:
        db_table = 'Servicio'

    def __str__(self):
        return self.nombre
