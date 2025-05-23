from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint
import numpy as np
from PIL import Image
import cv2
import os

class ManualEditor(QWidget):
    def __init__(self, image_path, on_apply_callback):
        super().__init__()
        self.setWindowTitle("Manual Text Remover")
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")
        self.image_np = np.array(self.image)
        self.mask = np.zeros(self.image_np.shape[:2], dtype=np.uint8)
        self.drawing = False
        self.last_point = QPoint()
        self.on_apply_callback = on_apply_callback

        self.canvas = QLabel()
        self.update_canvas()

        self.btn_apply = QPushButton("Apply Inpainting")
        self.btn_apply.clicked.connect(self.apply_inpainting)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_apply)
        self.setLayout(layout)

    def update_canvas(self):
        preview = self.image_np.copy()
        preview[self.mask == 255] = [255, 0, 0]  # Red overlay on mask
        h, w, _ = preview.shape
        qimage = QImage(preview.data, w, h, 3 * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.canvas.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            x1, y1 = self.last_point.x(), self.last_point.y()
            x2, y2 = event.pos().x(), event.pos().y()
            cv2.line(self.mask, (x1, y1), (x2, y2), 255, 15)  # thick brush
            self.last_point = event.pos()
            self.update_canvas()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def apply_inpainting(self):
        from core.inpaint import inpaint_image
        result = inpaint_image(self.image, self.mask)

        name = os.path.splitext(os.path.basename(self.image_path))[0]
        os.makedirs("outputs/manual", exist_ok=True)
        save_path = os.path.join("outputs/manual", f"{name}_manual_cleaned.jpg")
        result.save(save_path)
        print(f"✅ Manual image saved as {save_path}")
        
        self.on_apply_callback(result)
