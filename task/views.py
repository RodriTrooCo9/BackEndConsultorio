from rest_framework import viewsets, status
from rest_framework.response import Response
# modelos y serializers
from .models import Administrador, Doctor, Paciente, Cita, HistorialMedico, Tratamiento, Odontograma, Diente
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
TratamientoSerializer,
OdontogramaSerializer,
DienteSerializer
)

# Create your views here.
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()

        if not email or not password:
            return Response({'error': 'Faltan credenciales'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = None
        rol = None

        # 1. BUSCAR EN ADMINISTRADORES
        try:
            admin_user = Administrador.objects.get(email=email)
            # Aquí idealmente usaríamos: if check_password(password, admin_user.password_hash):
            if admin_user.password_hash == password: # Comparación simple (temporal)
                user_data = {'id': admin_user.id, 'nombre': admin_user.nombre, 'apellido': admin_user.apellido}
                rol = admin_user.rol # 'SuperAdmin' o 'Recepcionista'
        except Administrador.DoesNotExist:
            pass

        # 2. SI NO ES ADMIN, BUSCAR EN DOCTORES
        if not user_data:
            try:
                doctor = Doctor.objects.get(email=email)
                if doctor.password_hash == password:
                    if not doctor.activo:
                        return Response({'error': 'Cuenta de doctor inactiva'}, status=status.HTTP_403_FORBIDDEN)
                    user_data = {'id': doctor.id, 'nombre': doctor.nombre, 'apellido': doctor.apellido, 'especialidad': doctor.especialidad}
                    rol = 'Doctor'
            except Doctor.DoesNotExist:
                pass

        # 3. SI NO ES DOCTOR, BUSCAR EN PACIENTES
        if not user_data:
            try:
                paciente = Paciente.objects.get(email=email)
                if paciente.password_hash == password:
                    user_data = {'id': paciente.id, 'nombre': paciente.nombre, 'apellido': paciente.apellido}
                    rol = 'Paciente'
            except Paciente.DoesNotExist:
                pass

        # RESULTADO FINAL
        if user_data:
            return Response({
                'success': True,
                'rol': rol,
                'user': user_data,
                'token': 'demo-token-12345' # Aquí en el futuro pondrías un JWT real
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)




class OdontogramaViewSet(viewsets.ModelViewSet):
    queryset = Odontograma.objects.all()
    serializer_class = OdontogramaSerializer

class DienteViewSet(viewsets.ModelViewSet):
    queryset = Diente.objects.all()
    serializer_class = DienteSerializer
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