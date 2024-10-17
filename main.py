import os
from dotenv import load_dotenv
from auth import Auth
from mediator_registration import MediatorRegistration
from heartbeat import Heartbeat
from apscheduler.schedulers.background import BackgroundScheduler

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class Main:
    def __init__(self, **kwargs):
        # Instancia de autenticación
        self.auth = Auth(kwargs['options'])

        # Instancia de registro de mediadores
        self.mediator_registration = MediatorRegistration(
            auth=self.auth,
            conf=kwargs['conf'],
            options={
                # Ajuste aquí: Cambiamos la URL para coincidir con la ruta del canal en OpenHIM
                'mediators_url': "{}/mediator/register".format(kwargs['options']['apiURL']),
                'verify_cert': kwargs['options']['verify_cert'],
                'force_config': kwargs['options']['force_config']
            }
        )

        # Instancia de latido (heartbeat)
        self.heartbeat = Heartbeat(
            self.auth,
            options=kwargs['options'],
            conf=kwargs['conf'],
            scheduler=BackgroundScheduler()
        )

    # Método para autenticar
    def authenticate(self):
        return self.auth.authenticate()

    # Método para generar encabezados de autenticación
    def gen_auth_headers(self):
        return self.auth.gen_auth_headers()

    # Método para registrar el mediador
    def register_mediator(self):
        self.mediator_registration.run()

    # Método para activar el heartbeat
    def activate_heartbeat(self):
        return self.heartbeat.activate()

    # Método para desactivar el heartbeat
    def deactivate_heartbeat(self):
        return self.heartbeat.deactivate()

    # Método para obtener la configuración actual
    def fetch_config(self):
        return self.heartbeat.fetch_config()


if __name__ == "__main__":
    # Configuración del mediador
    conf = {
        "urn": "urn:mediator:openmrs-mediator",
        "version": "1.0.0",
        "name": "OpenMRS Mediator",
        "description": "Este es un mediador de prueba para OpenHIM",
        "endpoints": [
            {
                "name": "Api Base URL",
                "host": "172.31.7.32",  # Dirección de tu mediador
                "path": "/",
                "port": 9800,
                "primary": True,
                "type": "http"
            }
        ]
    }

    # Opciones de OpenHIM y del mediador
    options = {
        'apiURL': os.getenv('OPENHIM_URL'),  # URL base de la API de OpenHIM
        'username': os.getenv('OPENHIM_USERNAME'),  # Nombre de usuario de OpenHIM
        'password': os.getenv('OPENHIM_PASSWORD'),  # Contraseña del usuario de OpenHIM
        'verify_cert': False,  # Verificar certificados SSL (cambiar a True en producción)
        'force_config': False  # Si necesitas forzar la configuración
    }

    # Crear instancia de Main
    main_instance = Main(options=options, conf=conf)

    # Autenticar y registrar el mediador
    try:
        print("Autenticando...")
        main_instance.authenticate()
        print("Autenticación exitosa.")

        print("Registrando mediador...")
        main_instance.register_mediator()
        print("Mediador registrado exitosamente.")

        print("Activando heartbeat...")
        main_instance.activate_heartbeat()
        print("Heartbeat activado.")

    except Exception as e:
        print(f"Error: {e}")
