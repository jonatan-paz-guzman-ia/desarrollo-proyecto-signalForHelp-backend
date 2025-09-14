# ===== Etapa 1: Construcción de dependencias =====
FROM python:3.11-slim as builder

# Evitar mensajes interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar herramientas del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la app
WORKDIR /app

# Copiar los archivos de requirements y pyproject si existiera
COPY requirements.txt ./

# Instalar dependencias en cache de pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir grpcio grpcio-tools

# ===== Etapa 2: Copiar el código y generar proto =====
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código fuente
COPY . .

# Generar archivos Python a partir de Proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. signalforhelp.proto

# Exponer puerto FastAPI
EXPOSE 8000

# Comando por defecto para levantar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
