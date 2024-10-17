import httpx
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Cargar variables de entorno
load_dotenv()

class OpenHIMClient:
    def __init__(self):
        self.base_url = os.getenv('OPENHIM_URL')

    async def send_data_to_openhim(self, data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/channel/endpoint", json=data)
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=500, detail=f"Error al conectar con OpenHIM: {exc.response.content.decode()}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
