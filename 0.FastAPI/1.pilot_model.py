import cv2
import numpy as np

# Функция для обработки изображения (в тестовых целях)
def pilot_model(input_image):
    # Преобразуем изображение в массив numpy
    image_array = np.array(input_image)
    
    # Преобразуем массив в изображение OpenCV
    image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    dark_green_lower = (25, 52, 72)
    dark_green_upper = (102, 255, 255)
    light_green_lower = (35, 50, 50)
    light_green_upper = (85, 255, 255)
    dark_green_mask = cv2.inRange(hsv, dark_green_lower, dark_green_upper)
    light_green_mask = cv2.inRange(hsv, light_green_lower, light_green_upper)
    mask = cv2.bitwise_or(dark_green_mask, light_green_mask)
    
    result = cv2.bitwise_and(image, image, mask=mask)
    _, thresholded = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    result[thresholded == 255] = (0, 255, 0)
    result[thresholded == 0] = (0, 0, 0)
    
    # Преобразуем изображение OpenCV в массив numpy
    result_array = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    return result_array
