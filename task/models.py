from django.db import models

# Create your models here.

ROLES_ADMIN = [
    ('SuperAdmin', 'SuperAdmin'),
    ('Recepcionista', 'Recepcionista'),
]

ESTADO_CITA = [
    ('Reservada', 'Reservada'),
    ('Confirmada', 'Confirmada'),
    ('Cancelada', 'Cancelada'),
    ('Rechazada', 'Rechazada'),
    ('Completada', 'Completada'),
]

ESTADO_TRATAMIENTO = [
    ('Planificado', 'Planificado'),
    ('En Progreso', 'En Progreso'),
    ('Finalizado', 'Finalizado'),
    ('Pausado', 'Pausado'),
]

# --- MODELOS DE USUARIOS ---

class Administrador(models.Model):
    # Django crea automáticamente un id (pk) autoincremental, no es necesario declararlo explícitamente.
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255) # En producción, idealmente usar AbstractBaseUser
    rol = models.CharField(max_length=50, choices=ROLES_ADMIN)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"


class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    licencia = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"

    def __str__(self):
        return f"Dr. {self.apellido} - {self.especialidad}"


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=True, blank=True) # Puede ser opcional si es niño/anciano
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.TextField()

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# --- MODELOS DE TRANSACCIÓN Y REGISTRO ---

class Cita(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CITA, default='Reservada')
    notas_cancelacion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cita: {self.paciente} con {self.doctor} el {self.fecha_hora}"


class HistorialMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historiales')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='historiales_creados')
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_asociado')
    fecha_consulta = models.DateField(auto_now_add=True) # Se llena solo al crear
    diagnostico = models.TextField()
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"

    def __str__(self):
        return f"Historial {self.paciente} - {self.fecha_consulta}"


class Tratamiento(models.Model):
    historial = models.ForeignKey(HistorialMedico, on_delete=models.CASCADE, related_name='tratamientos')
    nombre_tratamiento = models.CharField(max_length=150)
    descripcion = models.TextField()
    # Numeric en SQL se traduce a DecimalField en Django para evitar errores de redondeo en dinero
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_TRATAMIENTO, default='Planificado')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"

    def __str__(self):
        return f"{self.nombre_tratamiento} ({self.estado})"

