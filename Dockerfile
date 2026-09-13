FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . .

# Comando para ejecutar el bot con la salida de log sin buffer
CMD ["python", "-u", "main.py"]
