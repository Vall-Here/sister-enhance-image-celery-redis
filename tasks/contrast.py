from celery import Celery
from workers.contrast import adjust_contrast

# Setup Celery untuk worker contrast
celery_contrast = Celery('tasks.contrast', broker='redis://redis:6379/0')

@celery_contrast.task
def adjust_contrast_image(image_path):
    return adjust_contrast(image_path)
