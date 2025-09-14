from fastapi import APIRouter, UploadFile, File, WebSocket
from app.services.yolo_service import process_image

router = APIRouter()

# REST - subir imagen
@router.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    contents = await file.read()
    detections, img_base64 = process_image(contents)
    return {"detections": detections, "image_base64": img_base64}

# WS - stream de video
@router.websocket("/segment-video")
async def segment_video(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            frame_bytes = await websocket.receive_bytes()
            detections, img_base64 = process_image(frame_bytes)
            await websocket.send_json({
                "detections": detections,
                "image_base64": img_base64
            })
        except Exception:
            await websocket.close()
            break
