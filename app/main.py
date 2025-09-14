from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="SignalForHelp Backend")

# Incluir rutas
app.include_router(routes.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
