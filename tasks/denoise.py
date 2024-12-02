from celery import Celery
from workers.denoising import denoise

# Setup Celery untuk worker denoise
celery_denoise = Celery('tasks.denoise', broker='redis://redis:6379/0')

@celery_denoise.task
def denoise_image(image_path):
    return denoise(image_path)
