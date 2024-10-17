import httpx
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Cargar variables de entorno
load_dotenv()

class OpenMRSClient:
    def __init__(self):
        self.base_url = os.getenv('OPENMRS_BASE_URL')
        self.auth = (os.getenv('OPENMRS_USER'), os.getenv('OPENMRS_PASSWORD'))  # Autenticación básica

    async def send_data_to_openmrs(self, data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/ws/rest/v1/patient",
                    json=data,
                    auth=self.auth
                )
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=500, detail=f"Error al conectar con OpenMRS: {exc.response.content.decode()}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
