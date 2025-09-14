import cv2
from ultralytics import YOLO
from src.preprocessing import apply_preprocessing
from src.utils import draw_results

def run_segmentation():
    # cargar modelo entrenado con YoloV8
    # NOTA: aunque el modelo se entreno con YOLOV8 pudimos cargar el modelo con YOLO11
    # https://docs.ultralytics.com/es/modes/predict/#key-features-of-predict-mode
    model = YOLO("models/best.pt")

    # capturar video desde la camara,
    # en este caso utilizamos 0 porque es la camara integrada de la mac
    cap = cv2.VideoCapture(0)

    # estamos evitando errores si la camara no esta disponible
    # (es mejor ponerlo, ya nos paso y el programa rompe sin este filtro)
    if not cap.isOpened():
        print("Error: no se pudo abrir la cámara")
        return
    # por comodidad utilizamos un cilo infinito para capturar y mostrar los frames
    while True:
        # cap.read() nos ayuda a capturar los frames
        # utilizamos ret para validar si el frame se capturo correctamente
        ret, frame = cap.read()
        if not ret:
            break

        # encapsulamos la logica del pre procesamiento del frame en esta funcion
        frame = apply_preprocessing(frame)

        # segun la documentacion de YOLO11
        # https://docs.ultralytics.com/es/modes/predict/#key-features-of-predict-mode
        # results	Contiene:
            # Cajas delimitadoras (bounding boxes)
            # Mascaras de segmentación (solo si es un modelo 'seg'),
            # Puntos clave (solo si es un modelo 'pose'),
            # Probabilidades de clasificación (solo si es un modelo 'cls')
            # Cajas orientadas (solo si es un modelo 'obb')

        results = model(frame)

        # encapsulamos la logica para dibujar los resultados en esta funcion
        annotated = draw_results(results)

        # cv2.imshow() es una función de OpenCV que crea una ventana donde se puede ver una imagen
        # https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html
        # El primer argumento es el nombre de la ventana.
        # El segundo argumento es una imagen en formato NumPy array
        cv2.imshow("Segmentación en Tiempo Real", annotated)


        # si se presiona la tecla q, salimos del cilo y cerramos la camara y la ventana.
        # https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    # detiene la captura de video.
    # libera los recursos del sistema (en este caso la webcam)
    # https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
    cap.release()

    # cierra las ventanas
    # https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
    cv2.destroyAllWindows()
