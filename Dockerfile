FROM python:3.10-slim

# Instalar dependencias del sistema en pasos separados
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js desde NodeSource (más confiable)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Verificar instalaciones
RUN node --version && npm --version

# Crear carpeta de trabajo
WORKDIR /app

# Copiar dependencias de Python e instalar
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Dar permisos al script
RUN chmod +x start.sh

# Exponer solo el puerto que Render debe usar
EXPOSE 10000

# Comando principal
CMD ["./start.sh"]