# Imagen base con más librerías que slim para evitar errores en Render Free
FROM python:3.10

# Evitar interacción durante la instalación de paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias básicas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 18 LTS desde repositorio oficial
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar y instalar dependencias de Python
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Dar permisos al script de inicio
RUN chmod +x start.sh

# Exponer el puerto que Render requiere
EXPOSE 10000

# Comando principal
CMD ["./start.sh"]
