from flask import Flask, request, jsonify, send_file
import numpy as np
import cv2
import io
from PIL import Image
import base64
from tasks import celery_app, enhance_and_denoise_task, enhance_contrast_task, combine_task

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Image Processing API"}), 200

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image file provided"}), 400
    
    image_file = request.files['image']
    img = Image.open(image_file)
    
    img_np = np.array(img)
    
    height, width, channels = img_np.shape
    image_data = img_np.tobytes()

    enhance_task = celery_app.send_task(
        "tasks.enhance_and_denoise_task", 
        args=[image_data, (height, width, channels)]
    )

    contrast_task = celery_app.send_task(
        "tasks.enhance_contrast_task", 
        args=[image_data, (height, width, channels)]
    )

    enhanced_and_denoised_image = enhance_task.get(timeout=10) 
    enhanced_contrast_image = contrast_task.get(timeout=10)

    combine_task = celery_app.send_task(
        "tasks.combine_task", 
        args=[enhanced_and_denoised_image, enhanced_contrast_image]
    )

    return jsonify({"message": "Image processing pipeline has started", "task_id": combine_task.id}), 202



@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    task = celery_app.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return jsonify({"message": "Task is still processing"}), 202
    elif task.state == 'FAILURE':
        return jsonify({"message": "Task failed"}), 500
    elif task.state == 'SUCCESS':
        processed_image_data = task.result
        return send_file(
            io.BytesIO(processed_image_data),  
            mimetype='image/png',             
            as_attachment=True,                
            download_name='processed_image.png' 
        )
    else:
        return jsonify({"message": "Task is in an unknown state"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
