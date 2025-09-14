from fastapi import APIRouter, UploadFile, File, WebSocket
from app.services.yolo_service import process_image

router = APIRouter()

# REST - subir imagen
@router.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    contents = await file.read()
    result = process_image(contents)
    return {"result": result}

# WS - stream de video
@router.websocket("/segment-video")
async def segment_video(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            frame_bytes = await websocket.receive_bytes()
            result = process_image(frame_bytes)
            await websocket.send_json({"result": result})
        except Exception:
            await websocket.close()
            break
