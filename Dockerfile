# Usar una imagen base de Python ligera
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias (requirements.txt) al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación al contenedor
COPY . .

# Exponer el puerto 9800 para que el servidor esté disponible
EXPOSE 9800

# Comando para ejecutar Uvicorn con FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9800"]
