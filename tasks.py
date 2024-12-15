import numpy as np
from celery import Celery
import cv2

celery_app = Celery('image_processor', broker='redis://localhost:6379/0')

celery_app.conf.update(
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
)

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


@celery_app.task
def enhance_contrast_task(image_data, image_shape):
    image = np.frombuffer(image_data, dtype=np.uint8)
    height, width, channels = image_shape
    image = image.reshape((height, width, channels))

    # Meningkatkan kontras menggunakan histogram equalization
    enhanced_image = cv2.convertScaleAbs(image, alpha=2.0, beta=0)

    _, buffer = cv2.imencode('.png', enhanced_image)
    processed_image_data = buffer.tobytes()

    return processed_image_data


@celery_app.task
def combine_task(denoised_image_data, contrast_image_data):
    denoised_image = cv2.imdecode(np.frombuffer(denoised_image_data, np.uint8), cv2.IMREAD_COLOR)
    contrast_image = cv2.imdecode(np.frombuffer(contrast_image_data, np.uint8), cv2.IMREAD_COLOR)

    combined_image = cv2.addWeighted(denoised_image, 0.5, contrast_image, 0.5, 0)

    _, buffer = cv2.imencode('.png', combined_image)
    combined_image_data = buffer.tobytes()

    return combined_image_data

