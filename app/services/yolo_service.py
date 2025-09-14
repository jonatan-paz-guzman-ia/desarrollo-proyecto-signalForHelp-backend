import cv2
import numpy as np
import base64
import torch
from ultralytics import YOLO

# Detectar si hay GPU disponible
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Cargar modelo una sola vez, fijando device y precision
model = YOLO("models/best.pt")
model.fuse()  # 🔹 fusiona capas Conv + BN (más rápido en inferencia)
if DEVICE == "cuda":
    model.to("cuda")
    model.model.half()  # 🔹 half precision (fp16) en GPU
else:
    model.to("cpu")

def process_image(image_bytes: bytes):
    # convertir a numpy
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 🔹 reducir resolución para velocidad
    img = cv2.resize(img, (640, 640))

    # ejecutar predicción (ya no pasamos device aquí 👇)
    results = model(img)

    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    # 🔹 usar el frame anotado
    annotated = results[0].plot()

    # 🔹 convertir el frame anotado a base64
    _, buffer = cv2.imencode(".jpg", annotated)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    return detections, img_base64
