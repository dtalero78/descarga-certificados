# Usa una imagen liviana de Python con apt
FROM python:3.11-slim

# Instala Chromium y dependencias necesarias
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
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
    wget \
    && rm -rf /var/lib/apt/lists/*

# Configura la variable de entorno para que Pyppeteer use Chromium del sistema
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Define el directorio de trabajo
WORKDIR /app

# Copia todos los archivos de tu proyecto a /app
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expón el puerto 8080
EXPOSE 8080

# Usa gunicorn como servidor de producción
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
