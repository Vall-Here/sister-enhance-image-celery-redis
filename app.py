from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import base64
import numpy as np
import cv2
from PIL import Image
from tasks import celery_app, enhance_and_denoise_task, enhance_contrast_task, combine_task

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_images', methods=['POST'])
def process_images():
    if 'images' not in request.files:
        return jsonify({"message": "No image files provided"}), 400

    files = request.files.getlist('images')
    task_ids = []

    for image_file in files:
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

        enhanced_and_denoised_image = enhance_task.get(timeout=30)
        enhanced_contrast_image = contrast_task.get(timeout=30)

        combine_task = celery_app.send_task(
            "tasks.combine_task",
            args=[enhanced_and_denoised_image, enhanced_contrast_image]
        )

        task_ids.append(combine_task.id)

    return jsonify({"message": "Image processing tasks have started", "task_ids": task_ids}), 202


@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    task = celery_app.AsyncResult(task_id)

    if task.state == 'PENDING':
        return jsonify({"message": "Task is still processing"}), 202
    elif task.state == 'FAILURE':
        return jsonify({"message": "Task failed"}), 500
    elif task.state == 'SUCCESS':
        processed_image_data = task.result
        
        # Convert binary data to base64 string for blob download
        processed_image_b64 = base64.b64encode(processed_image_data).decode('utf-8')

        return jsonify({
            "image_url": f"data:image/jpeg;base64,{processed_image_b64}",
            "task_id": task_id
        })
    else:
        return jsonify({"message": "Task is in an unknown state"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
