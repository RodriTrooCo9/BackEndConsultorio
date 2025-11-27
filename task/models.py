from django.db import models

# --- OPCIONES ---

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

# LISTA DE SERVICIOS CLINICA ARMONIZA
LISTA_SERVICIOS = [
    ('Cirugía terceros molares', 'Cirugía de terceros molares'),
    ('Cirugía simple', 'Cirugía simple'),
    ('Cirugía dientes retenidos', 'Cirugía de dientes retenidos'),
    ('Implantes', 'Implantes'),
    ('Curaciones', 'Curaciones'),
    ('Protesis fija', 'Prótesis fija'),
    ('Protesis removible', 'Prótesis removible'),
    ('Limpieza', 'Limpieza'),
    ('Fluorizaciones', 'Fluorizaciones'),
    ('Conducto uniradicular', 'Tratamiento conducto uniradicular'),
    ('Conducto biradicular', 'Tratamiento conducto biradicular'),
    ('Conducto multiradicular', 'Tratamiento conducto multiradicular'),
    ('Ortodoncia', 'Ortodoncia'),
    ('Ortopedia', 'Ortopedia'),
    ('Botox', 'Botox'),
    ('Rinomodelacion', 'Rinomodelación'),
    ('Relleno labios', 'Relleno de labios'),
    ('PRP', 'Plasma rico en plaquetas'),
    ('Bioestimuladores', 'Bioestimuladores de colágeno'),
    ('Hilos PDO', 'Hilos de PDO'),
    ('PDRN y exosomas', 'PDRN y exosomas'),
]

REFERENCIAS_ODONTOGRAMA = [
    ('SANO', 'Sano (Sin marcas)'),
    ('C', 'Caries (Rojo)'),
    ('DO', 'Diente Obturado (Azul)'),
    ('X', 'Exodoncia/Ausente (Cruz Roja)'),
    ('CO', 'Corona (Azul)'),
    ('TC', 'Tratamiento de Conducto (Azul)'),
    ('IP', 'Implante (Azul)'),
    ('P', 'Puente'),
]

# --- USUARIOS ---

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=ROLES_ADMIN)
    foto_perfil = models.ImageField(upload_to='admins/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    licencia = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    foto_perfil = models.ImageField(upload_to='doctores/', null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.apellido} - {self.especialidad}"

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=True, blank=True)
    direccion = models.TextField()
    foto_perfil = models.ImageField(upload_to='pacientes/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# --- ODONTOGRAMA ---

class Odontograma(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='odontograma')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    observaciones_generales = models.TextField(null=True, blank=True, help_text="Notas generales sobre la boca completa")

    def __str__(self):
        return f"Odontograma de {self.paciente}"


class Diente(models.Model):
    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE, related_name='dientes')
    numero_diente = models.IntegerField(help_text="11 al 85 (ISO)")

    # ESTADO GENERAL (Para cuando afecta todo el diente, ej: Ausente/X)
    estado_general = models.CharField(max_length=10, choices=REFERENCIAS_ODONTOGRAMA, default='SANO')

    # LAS 5 CARAS DEL DIENTE (para pintar el circulo)
    # Si es 'C' el frontend lo pinta Rojo. Si es 'DO' lo pinta Azul.
    cara_oclusal = models.CharField(max_length=10, choices=REFERENCIAS_ODONTOGRAMA, default='SANO',
                                    verbose_name="Centro")
    cara_vestibular = models.CharField(max_length=10, choices=REFERENCIAS_ODONTOGRAMA, default='SANO',
                                       verbose_name="Arriba")
    cara_lingual = models.CharField(max_length=10, choices=REFERENCIAS_ODONTOGRAMA, default='SANO',
                                    verbose_name="Abajo")
    cara_mesial = models.CharField(max_length=10, choices=REFERENCIAS_ODONTOGRAMA, default='SANO',
                                   verbose_name="Izquierda")
    cara_distal = models.CharField(max_length=10, choices=REFERENCIAS_ODONTOGRAMA, default='SANO',
                                   verbose_name="Derecha")

    # Notas específicas para este diente (lo que pediste que el doctor escriba)
    notas = models.TextField(null=True, blank=True, help_text="Ej: Caries profunda, requiere endodoncia")

    class Meta:
        # Ordenamos por número para que salgan en orden (11, 12, 13...)
        ordering = ['numero_diente']
        unique_together = ('odontograma', 'numero_diente')

    def __str__(self):
        return f"Diente {self.numero_diente} - {self.odontograma.paciente}"



class Cita(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CITA, default='Reservada')

class HistorialMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_consulta = models.DateField(auto_now_add=True)
    diagnostico = models.TextField()

class Tratamiento(models.Model):
    historial = models.ForeignKey(HistorialMedico, on_delete=models.CASCADE, related_name='tratamientos')
    nombre_tratamiento = models.CharField(max_length=100, choices=LISTA_SERVICIOS)
    descripcion = models.TextField(null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_TRATAMIENTO, default='Planificado')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_tratamiento} ({self.estado})"