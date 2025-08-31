FROM python:3.10-slim

# Paso 1: Solo update
RUN apt-get update

# Paso 2: Instalar dependencias básicas primero
RUN apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 curl

# Paso 3: Instalar Node.js por separado
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Limpiar
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN chmod +x start.sh
EXPOSE 10000
CMD ["./start.sh"]