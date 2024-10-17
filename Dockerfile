# Usar una imagen oficial de Python como imagen base
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Actualizar pip
RUN pip install --upgrade pip

# Copiar el archivo de dependencias y instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de código fuente al directorio de trabajo
COPY . .

# Exponer el puerto en el que FastAPI estará escuchando
EXPOSE 9800

# Ejecutar Uvicorn con la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9800"]
