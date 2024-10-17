from fastapi import FastAPI, Request, Response
import httpx
from openmrs_client import OpenMRSClient
from openhim_client import OpenHIMClient
import os
from contextlib import asynccontextmanager


# Función para registrar el mediador en OpenHIM



# Crear el contexto del ciclo de vida de la aplicación

app = FastAPI()

# Inicializamos los clientes de OpenMRS y OpenHIM
openmrs_client = OpenMRSClient()
openhim_client = OpenHIMClient()


@app.post("/openhim-to-openmrs")
async def openhim_to_openmrs(request: Request):
    """
    Endpoint que recibe las solicitudes desde OpenHIM y las reenvía a OpenMRS.
    """
    # Extraer los datos de la solicitud de OpenHIM
    data = await request.json()

    # Hacer una solicitud a OpenMRS con los datos de OpenHIM
    openmrs_response = await openmrs_client.send_data_to_openmrs(data)

    # Devolver la respuesta de OpenMRS a OpenHIM
    return Response(content=openmrs_response.text, status_code=openmrs_response.status_code)


@app.post("/openmrs-to-openhim")
async def openmrs_to_openhim(request: Request):
    """
    Endpoint que recibe las solicitudes desde OpenMRS y las reenvía a OpenHIM.
    """
    # Extraer los datos de la solicitud de OpenMRS
    data = await request.json()

    # Hacer una solicitud a OpenHIM con los datos de OpenMRS
    openhim_response = await openhim_client.send_data_to_openhim(data)

    # Devolver la respuesta de OpenHIM
    return Response(content=openhim_response.text, status_code=openhim_response.status_code)


@app.get("/heartbeat")
async def heartbeat():
    """
    Endpoint para verificar que el mediador esté activo.
    """
    return {"status": "alive"}
