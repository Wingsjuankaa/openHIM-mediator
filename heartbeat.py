import requests
import urllib3
from uptime import uptime


class Heartbeat:
    def __init__(self, auth, **kwargs):
        self.auth = auth  # Instancia de autenticación básica
        self.options = kwargs['options']
        self.__scheduler = kwargs['scheduler']
        self.__job = None
        self.conf = kwargs['conf']

    def _send(self, force_config=False):
        body = {'uptime': uptime()}
        if force_config or self.options['force_config']:
            body['config'] = True

        if not self.options['verify_cert']:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

        # Ajustamos la URL del heartbeat, asegúrate de que sea correcta
        mediators_url = "{}/mediator/{}/heartbeat".format(self.options['apiURL'], self.conf['urn'])

        # Usamos autenticación básica en lugar de headers manuales
        response = requests.post(
            url=mediators_url,
            verify=self.options['verify_cert'],
            json=body,
            auth=self.auth.authenticate()  # Autenticación básica
        )

        # Comprobamos que la respuesta sea 200 (OK)
        if response.status_code != 200:
            raise Exception(
                "Heartbeat unsuccessful, received status code of {}".format(response.status_code)
            )

    def activate(self):
        self.auth.authenticate()  # Autenticamos al activar
        if self.__job is None:
            # Programamos la tarea para enviar el heartbeat periódicamente
            self.__job = self.__scheduler.add_job(
                self._send,
                'interval',
                seconds=self.options.get('interval', 10)  # Intervalo configurado o 10 segundos por defecto
            )
            self.__scheduler.start()

    def deactivate(self):
        if self.__job is not None:
            self.__job.remove()

    def fetch_config(self):
        self.auth.authenticate()
        return self._send(True)
