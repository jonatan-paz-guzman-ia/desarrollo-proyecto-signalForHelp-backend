from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(title="SignalForHelp Backend")

# CORS: permitir todo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],      # permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],      # permite todos los headers
)

# Incluir rutas
app.include_router(routes.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
