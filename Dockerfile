# Usar una imagen base de Python (la versión 3.9 es adecuada, pero puedes cambiarla a la versión que necesites)
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias (requirements.txt) al contenedor
COPY requirements.txt .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al directorio de trabajo dentro del contenedor
COPY . .

# Establecer la variable de entorno para que Python no almacene archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Establecer la variable de entorno para que Python no almacene los logs en buffer (útil para contenedores)
ENV PYTHONUNBUFFERED 1

# Exponer el puerto si tu aplicación necesita aceptar conexiones
EXPOSE 9800

# Comando para ejecutar la aplicación (ajustar según cómo corras tu aplicación)
CMD ["python", "main.py"]
