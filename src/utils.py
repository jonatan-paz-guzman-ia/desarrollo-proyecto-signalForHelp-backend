def draw_results(results):
    # segun la documentacion de YOLO, el resultado de una predicción
    # es un objeto que contiene un frame anotado como un array de NumPy compatible con OpenCV.
    # por lo que se puede mostrar directamente las predicciones con cv2.imshow().
    # en este caso dejamos la abstraccion en esta funcion por si a futuro este concepto cambia
    # results[0] es porque solo es un frame el que enviamos
    # https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Results.plot
    return results[0].plot()  # frame con anotaciones dibujadas