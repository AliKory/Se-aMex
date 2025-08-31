# Imagen base de Python 3.10 slim
FROM python:3.10

# Evitar interacción durante la instalación de paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    ca-certificates \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 18 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar dependencias de Python e instalar
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Dar permisos al script de inicio
RUN chmod +x start.sh

# Exponer el puerto que Render debe usar
EXPOSE 10000

# Comando principal
CMD ["./start.sh"]
