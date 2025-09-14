# Backend - SignalForHelp

Este repositorio contiene el backend del proyecto **SignalForHelp**, implementado con **FastAPI**, que permite:

- Subir imágenes y obtener segmentación y anotaciones usando un modelo YOLO entrenado.
- Streaming de video vía WebSocket con segmentación en tiempo real.
- Retorno de imágenes anotadas en base64 junto con los resultados de detección.

---

## Requisitos

- Python >= 3.11
- [uv](https://pypi.org/project/uv/)
- GPU NVIDIA opcional para aceleración (CUDA)
- Node.js y frontend independiente para consumir la API

---

## Instalación y Configuración Local

1. **Clonar el repositorio:**

```bash
git clone https://github.com/jonatan-paz-guzman-ia/desarrollo-proyecto-signalForHelp-backend.git
cd desarrollo-proyecto-signalForHelp-backend
```

2. **Inicializar `uv` en el proyecto:**

```bash
uv init
```

3. **Crear y activar un entorno virtual local:**

```bash
uv venv .venv
```

- Si ya existe `.venv` y quieres reemplazarlo, responde `yes` cuando pregunte.

4. **Sincronizar dependencias con `uv` (instalar requirements):**

```bash
uv sync
```

- Esto instalará todas las dependencias definidas en `uv.lock`.

5. **Instalar dependencias adicionales si es necesario:**

```bash
uv add python-multipart grpcio grpcio-tools
```

---

## Generación de Archivos Protobuf

Para que gRPC funcione correctamente, se deben generar los archivos Python a partir del `.proto`:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. app/utils/signalforhelp.proto
```

- Esto generará los módulos necesarios para la comunicación gRPC.

---

## Ejecutar el Backend

### Modo Desarrollo con hot reload:

```bash
uv run uvicorn app.main:app --reload
```

- El backend quedará escuchando por defecto en `http://127.0.0.1:8000`.

### Endpoints disponibles:

1. **Health check:**

```
GET /health
```

2. **Subir imagen (REST):**

```
POST /api/segment-image
```

- Retorna:
```json
{
  "detections": [...],
  "image_base64": "..."
}
```

3. **Streaming de video (WebSocket):**

```
ws://127.0.0.1:8000/api/segment-video
```

- Envía los bytes de cada frame.
- Recibe JSON con las detecciones y la imagen anotada en base64.

---

## Tips de Uso

- Para pruebas académicas, CORS está abierto para todo.
- El modelo YOLO se carga al inicio para acelerar inferencia.
- Se recomienda usar GPU si está disponible; de lo contrario, se ejecuta en CPU.

---

## Estructura del Proyecto

```
desarrollo-proyecto-signalForHelp-backend
├── .gitignore
├── README.md
├── Dockerfile
├── Makefile
├── uv.lock
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services
│   │   └── yolo_service.py
│   └── utils
│       └── signalforhelp.proto
└── tests
    └── test_health.py
```

---

Con esto cualquier persona puede clonar el repositorio, configurar el entorno, generar los archivos de proto y levantar el backend de manera local.