FROM python:3.10-slim

# Instala dependencias del sistema necesarias para Chromium
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    chromium chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8080

# Ejecutar el servidor
CMD ["python", "app.py"]
