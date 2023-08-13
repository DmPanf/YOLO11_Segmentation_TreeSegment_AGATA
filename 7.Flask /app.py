from flask import Flask, render_template, request, send_file
import os
import io
import numpy as np
import cv2
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    input_image = request.files['image']
    image_array = np.frombuffer(input_image.read(), np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
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
    
    _, result_png = cv2.imencode('.png', result)
    output_image = io.BytesIO(result_png.tobytes())
    
    return send_file(output_image, mimetype='image/png', as_attachment=True, download_name='result.png')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
