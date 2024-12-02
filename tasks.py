# # from celery import Celery  # type: ignore
# # from workers.sharpening import sharpen
# # from workers.denoising import denoise
# # from workers.contrast import adjust_contrast
# # from workers.combine import combine_images

# # # Inisialisasi Celery dengan Redis sebagai broker
# # celery = Celery('tasks', broker='redis://redis:6379/0')

# # @celery.task  # Perbaiki decorator ini
# # def enhance_image(image_path):
# #     sharpened = sharpen(image_path)
# #     denoised = denoise(image_path)
# #     contrasted = adjust_contrast(image_path)
    
# #     final_image = combine_images(sharpened, denoised, contrasted)
    
# #     return final_image


# from celery import Celery  # type: ignore
# import os
# import cv2
# from workers.sharpening import sharpen
# from workers.denoising import denoise
# from workers.contrast import adjust_contrast
# from workers.combine import combine_images

# celery = Celery('tasks', broker='redis://redis:6379/0')

# @celery.task(bind=True) 
# def enhance_image(self, image_path):
#     try:
#         sharpened = sharpen(image_path)
        
#         denoised = denoise(image_path)
        
#         contrasted = adjust_contrast(image_path)
        
#         final_image_path = combine_images(sharpened, denoised, contrasted)
        
#         final_image = cv2.imread(final_image_path)
#         if final_image is None:
#             raise ValueError(f"Final combined image could not be read from {final_image_path}")
        
#         # Simpan gambar ke /tmp menggunakan OpenCV (cv2.imwrite)
#         final_image_path = '/tmp/enhanced_image.jpg'
#         cv2.imwrite(final_image_path, final_image)  
        
#         return final_image_path 
    
#     except Exception as e:
#         self.retry(exc=e)  
#         return {"error": str(e)}


from celery import Celery
from workers.sharpening import sharpen
from workers.denoising import denoise
from workers.contrast import adjust_contrast
from workers.combine import combine_images

# Setup Celery untuk masing-masing worker
celery_sharpen = Celery('tasks.sharpen', broker='redis://redis:6379/0')
celery_denoise = Celery('tasks.denoise', broker='redis://redis:6379/0')
celery_contrast = Celery('tasks.contrast', broker='redis://redis:6379/0')
celery_combine = Celery('tasks.combine', broker='redis://redis:6379/0')

# Task untuk sharpen
@celery_sharpen.task
def sharpen_image(image_path):
    return sharpen(image_path)

# Task untuk denoise
@celery_denoise.task
def denoise_image(image_path):
    return denoise(image_path)

# Task untuk adjust contrast
@celery_contrast.task
def adjust_contrast_image(image_path):
    return adjust_contrast(image_path)

# Task untuk combine image
@celery_combine.task
def combine_image(sharpened_path, denoised_path, contrasted_path):
    return combine_images(sharpened_path, denoised_path, contrasted_path)
