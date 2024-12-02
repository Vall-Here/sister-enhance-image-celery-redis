import cv2
import os
import numpy as np

from celery import Celery

app = Celery('tasks.sharpen', broker='redis://redis:6379/0')

def sharpen(image_path):
    image_path = os.path.abspath(image_path)
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image at {image_path}")
    
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, kernel)
    
    sharpened_path = os.path.join('/tmp', f"sharpened_{os.path.basename(image_path)}")
    cv2.imwrite(sharpened_path, sharpened_image)
    
    return sharpened_path
