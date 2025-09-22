# ===== Etapa 1: Construcción de dependencias =====
FROM python:3.11-slim as builder

ENV DEBIAN_FRONTEND=noninteractive

# Instalar herramientas necesarias para compilar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias
COPY requirements.txt ./

# Instalar dependencias en builder
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ===== Etapa 2: Imagen final =====
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# 🔑 Librerías necesarias para OpenCV en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias instaladas desde builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código fuente
COPY . .

# Variable de entorno para el modelo
ENV MODEL_PATH=/app/models/best.pt


# Puerto expuesto para FastAPI
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
