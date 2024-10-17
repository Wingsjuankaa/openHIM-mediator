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

    def authenticate(self):
        return self.auth.authenticate()

    def register_mediator(self):
        self.mediator_registration.run()

    def activate_heartbeat(self):
        return self.heartbeat.activate()

    def deactivate_heartbeat(self):
        return self.heartbeat.deactivate()

    def fetch_config(self):
        return self.heartbeat.fetch_config()


# Ejecutar el mediador al iniciar
def run_mediator():
    # Configuración del mediador
    conf = {
        "urn": "urn:mediator:openmrs-mediator",
        "version": "1.0.0",
        "name": "OpenMRS Mediator",
        "description": "Este es un mediador de prueba para OpenHIM",
        "endpoints": [
            {
                "name": "Api Base URL",
                "host": "172.31.7.32",
                "path": "/",
                "port": 9800,
                "primary": True,
                "type": "http"
            }
        ]
    }

    # Opciones de OpenHIM y del mediador
    options = {
        'apiURL': os.getenv('OPENHIM_URL'),
        'username': os.getenv('OPENHIM_USERNAME'),
        'password': os.getenv('OPENHIM_PASSWORD'),
        'verify_cert': False,
        'force_config': False
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


if __name__ == "__main__":
    # Ejecutar el mediador
    run_mediator()

    # Mantener la aplicación viva (simulación de servidor)
    import time

    while True:
        time.sleep(10)
