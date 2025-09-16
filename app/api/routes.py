from fastapi import APIRouter, UploadFile, File, WebSocket
from app.services.yolo_service import process_image

router = APIRouter()

# REST - subir imagen
@router.post("/segment-image")
async def segment_image(file: UploadFile = File(...)):
    """
    Realiza la segmentación de una imagen utilizando el modelo YOLO.

    Parameters
    ----------
    file : UploadFile
        Imagen cargada por el cliente en formato JPG o PNG.

    Returns
    -------
    dict
        Diccionario con:
        - detections : list of dict
            Lista de detecciones con clase, confianza y bounding box.
        - image_base64 : str
            Imagen procesada codificada en Base64.
    """
    contents = await file.read()
    detections, img_base64 = process_image(contents)
    return {"detections": detections, "image_base64": img_base64}


# WS - stream de video
@router.websocket("/segment-video")
async def segment_video(websocket: WebSocket):
    """
    Maneja un stream de video en tiempo real mediante WebSocket,
    procesando cada frame con el modelo YOLO.

    Parameters
    ----------
    websocket : WebSocket
        Conexión WebSocket establecida con el cliente.

    Notes
    -----
    - Cada frame recibido se procesa con `process_image`.
    - El resultado se envía de vuelta como JSON con detecciones
      y la imagen procesada en Base64.
    - Si ocurre un error, la conexión WebSocket se cierra.
    """
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
