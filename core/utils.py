import numpy as np
import cv2
from PIL import Image

def build_mask_from_polygons(polygons, size):
    mask = np.zeros(size, dtype=np.uint8)
    for poly in polygons:
        poly = np.array(poly, dtype=np.int32)
        cv2.fillPoly(mask, [poly], 255)
    return mask

def load_image(path):
    return Image.open(path).convert("RGB")
