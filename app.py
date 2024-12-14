from flask import Flask, request, jsonify, send_file
import numpy as np
import cv2
import io
from PIL import Image
import base64
from tasks import celery_app, enhance_and_denoise_task

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
    
    # Konversi gambar menjadi array numpy
    img_np = np.array(img)
    
    # Ambil dimensi gambar
    height, width, channels = img_np.shape

    # Convert gambar menjadi byte array
    image_data = img_np.tobytes()

    # Kirim image_data dan dimensi gambar (height, width, channels)
    task = celery_app.send_task(
        "tasks.enhance_and_denoise_task", 
        args=[image_data, (height, width, channels)]
    )

    return jsonify({"message": "Image processing has been started", "task_id": task.id}), 202






@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    task = celery_app.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return jsonify({"message": "Task is still processing"}), 202
    elif task.state == 'FAILURE':
        return jsonify({"message": "Task failed"}), 500
    
    # Ambil hasil gambar yang sudah diproses dari task
    processed_image_data = task.result

    # Kirim gambar yang sudah diproses sebagai file PNG (atau format lain sesuai kebutuhan)
    return send_file(
        io.BytesIO(processed_image_data),  # Konversi byte array menjadi file-like object
        mimetype='image/png',              # Jenis mimetype gambar (sesuaikan dengan format gambar Anda)
        as_attachment=True,                # Menandakan bahwa ini adalah file yang akan diunduh
        download_name='processed_image.png'  # Nama file yang diunduh
    )



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
