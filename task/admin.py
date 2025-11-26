from django.contrib import admin
from .models import Administrador, Doctor, Paciente, Cita, HistorialMedico, Tratamiento

# Configuración del Admin para ADMINISTRADORES
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'rol')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('rol',)

# Configuración del Admin para DOCTORES
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'licencia', 'activo', 'email')
    search_fields = ('nombre', 'apellido', 'licencia', 'especialidad')
    list_filter = ('especialidad', 'activo')
    list_editable = ('activo',) # Permite activar/desactivar doctores desde la lista

# Configuración del Admin para PACIENTES
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('fecha_nacimiento',)

# Configuración del Admin para CITAS (Muy importante)
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora', 'doctor') # Filtros laterales
    search_fields = ('paciente__nombre', 'paciente__apellido', 'doctor__nombre', 'doctor__apellido')
    date_hierarchy = 'fecha_hora' # Navegación rápida por fechas arriba
    ordering = ('-fecha_hora',) # Las más recientes primero

# Configuración del Admin para HISTORIAL MÉDICO
@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha_consulta', 'cita')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'diagnostico')
    list_filter = ('fecha_consulta', 'doctor')

# Configuración del Admin para TRATAMIENTOS
@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre_tratamiento', 'historial', 'costo', 'estado', 'fecha_inicio')
    search_fields = ('nombre_tratamiento', 'historial__paciente__nombre')
    list_filter = ('estado', 'fecha_inicio')

def __str__(self):
    return self.nombre