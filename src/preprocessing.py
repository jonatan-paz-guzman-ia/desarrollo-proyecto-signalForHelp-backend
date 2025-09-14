import cv2
import numpy as np

def apply_preprocessing(frame):
    # suavizado con GaussianBlur
    # se utiliza principalmente para reducir el ruido y eliminar valores atípicos en una imagen
    # referencia: Clase__2_Filtrado_de_imagenes_E.ipynb
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    # filtro de sharpening (realce de bordes)
    kernel_sharpening = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])

    sharpened = cv2.filter2D(blurred, -1, kernel_sharpening)

    return sharpened
