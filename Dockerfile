# Imagen base con Python
FROM python:3.11-slim

# Instala dependencias necesarias para Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Establece la variable de entorno para que pyppeteer use Chromium del sistema
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Crea directorio para la app
WORKDIR /app

# Copia todos los archivos de la app
COPY . .

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto 8080 para DigitalOcean
EXPOSE 8080

# Comando para correr el servidor
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
