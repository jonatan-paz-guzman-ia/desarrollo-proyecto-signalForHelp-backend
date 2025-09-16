import base64
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
import app.api.routes as yolo_routes

# Crear app de prueba y montar el router
app = FastAPI()
app.include_router(yolo_routes.router)

client = TestClient(app)


def fake_process_image(_):
    """
    Función mock para simular el procesamiento de imágenes con YOLO.

    Retorna siempre una detección falsa con clase `0` y una imagen codificada
    en base64 para reemplazar la inferencia real del modelo.

    Parameters
    ----------
    _ : bytes
        Bytes de la imagen de entrada (no se utilizan en esta simulación).

    Returns
    -------
    tuple
        detections : list of dict
            Lista con una única detección falsa que contiene:
            - class : int
            - confidence : float
            - bbox : list[int]
        img_base64 : str
            Imagen codificada en base64 simulada.
    """
    return [
        {"class": 0, "confidence": 0.99, "bbox": [10, 10, 100, 100]}
    ], base64.b64encode(b"fake_image").decode("utf-8")


@patch("app.api.routes.process_image", side_effect=fake_process_image)
def test_segment_image(mock_process):
    """
    Prueba unitaria para el endpoint `/segment-image`.

    Simula el envío de un archivo de imagen y valida que el backend
    retorne detecciones e imagen codificada en base64.

    Parameters
    ----------
    mock_process : MagicMock
        Objeto mock que reemplaza la función `process_image`.

    Assertions
    ----------
    - El código de estado de la respuesta debe ser 200.
    - El JSON de la respuesta debe contener las claves `detections` e `image_base64`.
    - Debe existir exactamente una detección simulada.
    - La clase de la detección debe ser 0.
    """
    file_content = b"fake_image_bytes"
    response = client.post(
        "/segment-image",
        files={"file": ("test.jpg", file_content, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "detections" in data
    assert "image_base64" in data
    assert len(data["detections"]) == 1
    assert data["detections"][0]["class"] == 0


@patch("app.api.routes.process_image", side_effect=fake_process_image)
def test_segment_video(mock_process):
    """
    Prueba unitaria para el endpoint `/segment-video` (WebSocket).

    Simula el envío de un frame de video por WebSocket y valida que el backend
    retorne detecciones e imagen codificada en base64.

    Parameters
    ----------
    mock_process : MagicMock
        Objeto mock que reemplaza la función `process_image`.

    Assertions
    ----------
    - El JSON recibido debe contener las claves `detections` e `image_base64`.
    - Debe existir exactamente una detección simulada.
    - La clase de la detección debe ser 0.
    """
    with client.websocket_connect("/segment-video") as websocket:
        websocket.send_bytes(b"fake_frame_bytes")
        data = websocket.receive_json()
        assert "detections" in data
        assert "image_base64" in data
        assert len(data["detections"]) == 1
        assert data["detections"][0]["class"] == 0
