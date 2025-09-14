from fastapi import APIRouter, UploadFile, File, WebSocket
from app.services.yolo_service import process_image
import asyncio

router = APIRouter()

# REST - subir imagen
@router.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    contents = await file.read()
    detections, img_base64 = process_image(contents)
    return {"detections": detections, "image_base64": img_base64}


# WS - stream de video con rate limit (procesa un frame a la vez)
@router.websocket("/segment-video")
async def segment_video(websocket: WebSocket):
    await websocket.accept()
    processing = False  # bandera para controlar si ya hay un frame en proceso

    async def handle_frame(frame_bytes):
        nonlocal processing
        try:
            detections, img_base64 = process_image(frame_bytes)
            await websocket.send_json({
                "detections": detections,
                "image_base64": img_base64
            })
        finally:
            processing = False  # liberar la bandera cuando termina

    try:
        while True:
            frame_bytes = await websocket.receive_bytes()

            if processing:
                # ⚠️ descartamos el frame si aún estamos procesando
                continue

            processing = True
            # procesar el frame en un task asincrónico para no bloquear el loop
            asyncio.create_task(handle_frame(frame_bytes))

    except Exception:
        await websocket.close()
