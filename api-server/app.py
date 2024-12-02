# from flask import Flask, request, jsonify
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from tasks import enhance_image
# from celery.result import AsyncResult # type: ignore

# app = Flask(__name__)

# @app.route('/enhance', methods=['POST'])
# def enhance():
#     if 'image' not in request.files:
#         return jsonify({"error": "Image file is required"}), 400

#     image = request.files['image']
#     image_path = os.path.join('/tmp', image.filename)
    
#     # Log untuk memastikan file berhasil disimpan
#     print(f"Saving image to {image_path}")
#     try:
#         image.save(image_path)
#         print(f"Image saved to {image_path}")
#     except Exception as e:
#         print(f"Error saving image: {str(e)}")
#         return jsonify({"error": "Failed to save image"}), 500
    
#     task = enhance_image.apply_async(args=[image_path])
#     return jsonify({"task_id": task.id, "status": "Task is processing"}), 202





# @app.route('/task-status/<task_id>', methods=['GET'])
# def task_status(task_id):
#     task = AsyncResult(task_id)
    
#     if task.state == 'PENDING':
#         return jsonify({"status": "Task is pending..."}), 202
#     elif task.state == 'PROGRESS':
#         return jsonify({"status": "Task is in progress..."}), 202
#     elif task.state == 'SUCCESS':
#         return jsonify({"status": "Task completed", "result": task.result}), 200
#     elif task.state == 'FAILURE':
#         return jsonify({"status": "Task failed", "error": str(task.info)}), 500
#     else:
#         return jsonify({"status": "Unknown state"}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)



from flask import Flask, request, jsonify
import os
import sys
from celery.result import AsyncResult
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks import enhance_image

app = Flask(__name__)

@app.route('/')
def index():
    return "Image Enhancement API"

@app.route('/enhance', methods=['POST'])
def enhance():
    if 'image' not in request.files:
        return jsonify({"error": "Image file is required"}), 400

    image = request.files['image']
    image_path = os.path.join('/tmp', image.filename)  # Simpan gambar ke /tmp volume

    try:
        image.save(image_path)
        print(f"Image saved to {image_path}")
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return jsonify({"error": "Failed to save image"}), 500
    
    task = enhance_image(image_path) 
    return jsonify({"task_id": task.id, "status": "Task is processing"}), 202


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
