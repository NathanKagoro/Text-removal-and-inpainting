import easyocr
import numpy as np

reader = easyocr.Reader(['en'])

def detect_text_boxes(image_path):
    results = reader.readtext(image_path)
    return results

def extract_polygons(results):
    polygons = [np.array(box, dtype=np.int32) for box, _, _ in results]
    return polygons

def extract_text(results):
    return [text for _, text, _ in results]
