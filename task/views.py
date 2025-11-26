from rest_framework import viewsets, status
from rest_framework.response import Response
# modelos y serializers
from .models import Administrador, Doctor, Paciente, Cita, HistorialMedico, Tratamiento
# chatBot
from rest_framework.views import APIView
from django.utils import timezone
import re

from .serializer import (
AdministradorSerializer,
DoctorSerializer,
PacienteSerializer,
CitaSerializer,
HistorialMedicoSerializer,
TratamientoSerializer
)

# Create your views here.

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    # Lógica: Ordenamos alfabéticamente por apellido para facilitar la búsqueda en listas desplegables
    queryset = Doctor.objects.all().order_by('apellido')
    serializer_class = DoctorSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    # Lógica: Igual que los doctores, ordenados por apellido
    queryset = Paciente.objects.all().order_by('apellido')
    serializer_class = PacienteSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by('-fecha_hora')
    serializer_class = CitaSerializer

    # 1. PUT: Actualizar TODO el registro
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

    # 2. PATCH: Actualizar solo UNA PARTE del registro
    def partial_update(self, request, *args, **kwargs):
        # Ej: Solo cambiar el estado a 'Cancelada' sin enviar los otros datos
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    # 3. DELETE: Borrar el registro
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # --- Lógica de seguridad (Opcional) ---
        # Ej: No permitir borrar si la cita ya pasó
        # if instance.estado == 'Completada':
        #     return Response({"error": "No puedes borrar citas completadas"}, status=400)

        # Realizar el borrado
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class HistorialMedicoViewSet(viewsets.ModelViewSet):
    queryset = HistorialMedico.objects.all().order_by('-fecha_consulta')
    serializer_class = HistorialMedicoSerializer

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all().order_by('estado', '-fecha_inicio')
    serializer_class = TratamientoSerializer

# -----chatBot------
class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get('message', '').lower()
        paciente_id = request.data.get('paciente_id')  # El frontend debe enviar quién habla

        response_text = "No entendí tu solicitud. Puedes decir 'cancelar cita', 'mis citas' o consultar horarios."

        # --- LÓGICA 1: CANCELAR CITA ---
        if "cancelar" in user_message and "cita" in user_message:
            # Buscamos si el usuario escribió un número (ID de la cita)
            match = re.search(r'\d+', user_message)

            if match:
                cita_id = match.group()
                try:
                    cita = Cita.objects.get(id=cita_id, paciente_id=paciente_id)
                    cita.estado = 'Cancelada'
                    cita.notas_cancelacion = "Cancelada vía Chatbot"
                    cita.save()
                    response_text = f"Listo. He cancelado tu cita #{cita_id}."
                except Cita.DoesNotExist:
                    response_text = f" No encontré ninguna cita tuya con el número {cita_id}."
            else:
                response_text = "Para cancelar, necesito el número de la cita. Ej: 'Cancelar cita 45'."

        # --- LÓGICA 2: CONSULTAR MIS CITAS ---
        elif "mis citas" in user_message or "tengo cita" in user_message:
            citas = Cita.objects.filter(paciente_id=paciente_id, estado='Reservada', fecha_hora__gte=timezone.now())
            if citas.exists():
                texto_citas = "\n".join(
                    [f"- Cita #{c.id} con Dr. {c.doctor.apellido} el {c.fecha_hora.strftime('%d/%m %H:%M')}" for c in
                     citas])
                response_text = f" Tienes estas citas próximas:\n{texto_citas}"
            else:
                response_text = "No tienes citas próximas reservadas."

        # --- LÓGICA 3: CONSULTORIA (Simulada o IA) ---
        elif "dolor" in user_message or "sintoma" in user_message:
            # AQUÍ es donde conectarías con ChatGPT/Gemini si quisieras inteligencia real
            response_text = "Entiendo que tienes malestar. Recuerda que soy un bot. Por favor reserva una cita con Medicina General para una valoración real."

        # --- LÓGICA 4: RESERVAR (Simplificado) ---
        elif "reservar" in user_message:
            response_text = "Para reservar, por favor indica: Especialidad y Fecha. (Esta función requiere lógica compleja de horarios, te sugiero usar el calendario visual del frontend)."

        return Response({'reply': response_text}, status=status.HTTP_200_OK)