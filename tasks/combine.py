from celery.result import AsyncResult
from celery import Celery
from workers.combine import combine_images

# Setup Celery untuk worker combine
celery_combine = Celery('tasks.combine', broker='redis://redis:6379/0')

@celery_combine.task
def combine_image(sharpened_id, denoised_id, contrasted_id):
    # Mengambil hasil task sebelumnya
    sharpened_result = AsyncResult(sharpened_id).result
    denoised_result = AsyncResult(denoised_id).result
    contrasted_result = AsyncResult(contrasted_id).result

    # Gabungkan gambar
    return combine_images(sharpened_result, denoised_result, contrasted_result)
