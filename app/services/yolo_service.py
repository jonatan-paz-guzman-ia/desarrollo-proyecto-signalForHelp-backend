import cv2
import numpy as np
from ultralytics import YOLO

# cargar modelo entrenado al inicio
model = YOLO("models/best.pt")

def process_image(image_bytes: bytes):
    # convertir a numpy
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(img)
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })
    return detections
