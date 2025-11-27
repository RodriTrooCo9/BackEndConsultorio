from rest_framework import serializers
from .models import Administrador, Doctor, Paciente, Cita, HistorialMedico, Tratamiento
from .models import Odontograma, Diente



class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'
        extra_kwargs = {
            'password_hash': {'write_only': True}  # Oculta el password en las respuestas GET
        }


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }


# --- SERIALIZERS DE TRANSACCIÓN Y REGISTRO ---

class CitaSerializer(serializers.ModelSerializer):
    # Tip Pro: Si quisieras que en lugar del ID (ej: 1) salga el nombre del doctor,
    # podrías agregar: doctor_nombre = serializers.CharField(source='doctor.nombre', read_only=True)

    class Meta:
        model = Cita
        fields = '__all__'


class HistorialMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMedico
        fields = '__all__'


class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = '__all__'



class DienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diente
        fields = '__all__' # Enviará cara_oclusal, cara_mesial, etc.


class OdontogramaSerializer(serializers.ModelSerializer):
    # Esto mostrará la lista completa de dientes dentro del odontograma
    dientes = DienteSerializer(many=True, read_only=True)

    class Meta:
        model = Odontograma
        fields = ['id', 'paciente', 'fecha_creacion', 'observaciones_generales', 'dientes']