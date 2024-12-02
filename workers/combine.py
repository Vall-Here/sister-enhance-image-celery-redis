import os
import cv2
import numpy as np

from celery import Celery

app = Celery('task.combine_images', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


def combine_images(sharpened_path, denoised_path, contrasted_path):
    # Membaca hasil masing-masing worker
    sharpened = cv2.imread(sharpened_path)
    denoised = cv2.imread(denoised_path)
    contrasted = cv2.imread(contrasted_path)
    
    if sharpened is None:
        raise ValueError(f"Failed to read sharpened image at {sharpened_path}")
    if denoised is None:
        raise ValueError(f"Failed to read denoised image at {denoised_path}")
    if contrasted is None:
        raise ValueError(f"Failed to read contrasted image at {contrasted_path}")
    
    combined_image = (sharpened / 3 + denoised / 3 + contrasted / 3).astype(np.uint8)
    
    result_path = f"/tmp/combined_{os.path.basename(sharpened_path)}"
    cv2.imwrite(result_path, combined_image)
    
    return result_path
