import numpy as np
from celery import Celery
import cv2

# Inisialisasi Celery dengan Redis sebagai brokerc
celery_app = Celery('image_processor', broker='redis://localhost:6379/0')

# Konfigurasi Celery
celery_app.conf.update(
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
)

# Task untuk Enhance dan Denoise Gambar
@celery_app.task
def enhance_and_denoise_task(image_data, image_shape):
    image = np.frombuffer(image_data, dtype=np.uint8)
    height, width, channels = image_shape

    image = image.reshape((height, width, channels))

    denoised_image = cv2.bilateralFilter(image, 9, 75, 75)
    enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=0)

    _, buffer = cv2.imencode('.png', enhanced_image)
    processed_image_data = buffer.tobytes()

    return processed_image_data
