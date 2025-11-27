from django.contrib import admin
from .models import Administrador, Doctor, Paciente, Cita, HistorialMedico, Tratamiento, Odontograma, Diente


# --- USUARIOS ---

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'rol')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('rol',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'activo', 'email')
    search_fields = ('nombre', 'apellido', 'licencia', 'especialidad')
    list_filter = ('especialidad', 'activo')
    list_editable = ('activo',)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('fecha_nacimiento',)


# --- ODONTOGRAMA (Corregido) ---

@admin.register(Odontograma)
class OdontogramaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'ultima_actualizacion')
    search_fields = ('paciente__nombre', 'paciente__apellido')


@admin.register(Diente)
class DienteAdmin(admin.ModelAdmin):
    # CORRECCIÓN: Usamos los campos nuevos (estado_general, caras)
    list_display = ('odontograma', 'numero_diente', 'estado_general', 'cara_oclusal', 'notas')

    # Filtros útiles para encontrar caries rápido
    list_filter = ('estado_general', 'numero_diente')

    # Búsqueda por nombre del paciente
    search_fields = ('odontograma__paciente__nombre', 'odontograma__paciente__apellido')

    # Opcional: Esto te permite editar el estado del diente directamente desde la lista sin entrar
    list_editable = ('estado_general',)


# --- GESTIÓN CLÍNICA ---

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora', 'doctor')
    search_fields = ('paciente__nombre', 'doctor__nombre')
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)


@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha_consulta')
    search_fields = ('paciente__nombre', 'diagnostico')
    list_filter = ('fecha_consulta', 'doctor')


@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre_tratamiento', 'historial', 'costo', 'estado', 'fecha_inicio')
    search_fields = ('nombre_tratamiento', 'historial__paciente__nombre')
    list_filter = ('estado', 'fecha_inicio', 'nombre_tratamiento')