import os
import cv2
import numpy as np

def adjust_contrast(image_path):
    image = cv2.imread(image_path)
    
    alpha = 1.5  # Contrast factor
    beta = 0     # Brightness
    
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    result_path = os.path.join('/tmp', f"contrast_{os.path.basename(image_path)}")
    cv2.imwrite(result_path, adjusted_image)
    
    return result_path
