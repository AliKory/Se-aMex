FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

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
