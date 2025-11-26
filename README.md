# Sistema de Gestión Clínico (API Backend)

Este proyecto es un backend robusto construido con **Django** y **Django REST Framework** para la gestión integral de una clínica médica. Incluye autenticación, gestión de roles (Doctores, Pacientes, Admin), historial clínico y un **Chatbot inteligente** para la gestión de citas.

##Características Principales

* **Gestión de Usuarios:** Modelos separados para Administradores, Doctores y Pacientes.
* **Agenda Médica:** CRUD completo para reservar, reagendar y cancelar citas.
* **Expediente Clínico:** Registro de historial médico y tratamientos asociados.
* **API RESTful:** Endpoints estandarizados y ordenados lógicamente.
* **Chatbot Integrado:** Endpoint `/api/v1/chatbot/` capaz de procesar lenguaje natural simple para cancelar o consultar citas.
* **Documentación Automática:** Interfaz **Swagger/OpenAPI** interactiva integrada.
* **Seguridad:** Manejo de contraseñas con `write_only` para proteger datos sensibles.

## Tecnologías Usadas

* **Python** 3.12+
* **Django** 5.x
* **Django REST Framework**
* **drf-spectacular** (Para documentación OpenAPI)
* **PosgresSQL** (Base de datos por defecto, escalable a PostgreSQL)

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/RodriTrooCo9/BackEndConsultorio.git
cd Backend1
```

```
python -m venv .venv
.venv\Scripts\activate
```
```
python3 -m venv .venv
source .venv/bin/activate
```
```
pip install django djangorestframework drf-spectacular setuptools
```
```
python manage.py makemigrations
python manage.py migrate
```
```
python manage.py createsuperuser
python manage.py runserver
```

El servidor estará corriendo en http://127.0.0.1:8000/ Documentación de la APIGracias a drf-spectacular, puedes ver y probar todos los endpoints visualmente
sin necesidad de Postman.Swagger UI: http://127.0.0.1:8000/docs/Schema YAML:
 http://127.0.0.1:8000/api/schema/Endpoints PrincipalesMétodoEndpointDescripciónGET/POST/api/v1/doctores/Listar o registrar doctoresGET/POST/api/v1/pacientes/Listar o
 registrar pacientesGET/POST/api/v1/citas/Gestión de citas médicasGET/POST/api/v1/historiales/Historial médico de pacientesPOST/api/v1/chatbot/Interacción con el asistente virtual
 Uso del ChatbotEl chatbot acepta peticiones POST para realizar acciones rápidas.URL: 
 ```
 http://127.0.0.1:8000/api/v1/chatbot/Ejemplo de JSON (Body):JSON
{
    "paciente_id": 1,
    "message": "Hola, necesito cancelar mi cita numero 45"
}
Respuesta:JSON{
    "reply": " Listo. He cancelado tu cita #45."
}
```
Estructura del ProyectoBackend1/
```
├── manage.py
├── Backend1/           # Configuración principal (settings, urls)
└── task/               # Aplicación principal
    ├── admin.py        # Configuración del panel admin
    ├── models.py       # Modelos de base de datos
    ├── serializers.py  # Transformación de datos
    ├── views.py        # Lógica (ViewSets y Chatbot)
    └── urls.py         # Rutas de la API

```
