from PIL import Image
import numpy as np
from simple_lama_inpainting import SimpleLama

model = SimpleLama()

def inpaint_image(image_pil, mask_np):
    image_np = np.array(image_pil.convert("RGB"))
    result_image = model(image_np, mask_np)  
    return result_image 
