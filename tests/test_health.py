from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """
    Prueba unitaria para el endpoint `/health`.

    Verifica que el endpoint de salud de la aplicación responda correctamente
    y confirme que el backend está en funcionamiento.

    Assertions
    ----------
    - El código de estado de la respuesta debe ser 200.
    - El JSON de la respuesta debe ser {"status": "ok"}.
    """
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
