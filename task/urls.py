from django.template.defaultfilters import title
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from . import views
#documentacion de la api
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# Configuración del Router
router = routers.DefaultRouter()

# Registro de rutas (Endpoints)
# El primer parámetro es la URL (ej: api/v1/doctores/)
# El segundo es el ViewSet que controla la lógica
# El tercero es el nombre interno para Django
router.register(r'admins', views.AdministradorViewSet, basename='administradores')
router.register(r'doctores', views.DoctorViewSet, basename='doctores')
router.register(r'pacientes', views.PacienteViewSet, basename='pacientes')
router.register(r'citas', views.CitaViewSet, basename='citas')
router.register(r'historiales', views.HistorialMedicoViewSet, basename='historiales')
router.register(r'tratamientos', views.TratamientoViewSet, basename='tratamientos')

router.register(r'odontogramas', views.OdontogramaViewSet, basename='odontogramas')
router.register(r'dientes', views.DienteViewSet, basename='dientes')

urlpatterns = [

    path("api/v1/", include(router.urls)),
    path('api/v1/auth/login/', views.LoginView.as_view(), name='auth_login'),
    path('api/v1/chatbot/',views.ChatbotView.as_view(), name='chatbot'),

    #api documentacion

    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


]