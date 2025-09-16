import cv2
import numpy as np
import base64
import os
from ultralytics import YOLO

# Leer ruta desde variable de entorno o usar default
MODEL_PATH = os.getenv("MODEL_PATH", "models/best.pt")

# Cargar modelo al inicio
model = YOLO(MODEL_PATH)

def process_image(image_bytes: bytes):
    """
    Procesa una imagen usando el modelo YOLO entrenado para realizar detección y segmentación.

    Parameters
    ----------
    image_bytes : bytes
        Imagen en formato de bytes (ej. archivo cargado o frame de video).

    Returns
    -------
    tuple
        detections : list of dict
            Lista de detecciones realizadas por el modelo YOLO.
            Cada detección contiene:
            - class : int
                ID de la clase detectada.
            - confidence : float
                Nivel de confianza de la detección (0.0 - 1.0).
            - bbox : list of float
                Coordenadas del bounding box en formato [x1, y1, x2, y2].
        img_base64 : str
            Imagen anotada (con detecciones dibujadas) codificada en Base64.

    Notes
    -----
    - Se convierte la imagen de bytes a formato OpenCV (numpy array).
    - El modelo genera automáticamente un frame anotado con las predicciones.
    - La imagen anotada se devuelve en formato Base64 para su fácil transmisión en APIs o WebSockets.
    """
    # convertir a numpy
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # ejecutar predicción
    results = model(img)

    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    # 🔹 usar el frame anotado que YOLO genera automáticamente
    annotated = results[0].plot()

    # 🔹 convertir el frame anotado a base64
    _, buffer = cv2.imencode(".jpg", annotated)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    return detections, img_base64
