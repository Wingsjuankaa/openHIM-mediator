import requests
import urllib3
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import datetime

# Cargar el archivo .env
load_dotenv()


class Auth:
    def __init__(self, options):
        self.options = options

    # Autenticación usando HTTP Basic Auth
    def authenticate(self):
        if not self.options['verify_cert']:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Devuelve un objeto HTTPBasicAuth que se usa en las solicitudes
        return HTTPBasicAuth(self.options['username'], self.options['password'])

    # No es necesario generar encabezados personalizados aquí,
    # ya que se usa autenticación básica.
    def gen_auth_headers(self):
        # En el caso de Basic Auth, puedes devolver un encabezado simple si es necesario
        return {
            'Content-Type': 'application/json'
        }
