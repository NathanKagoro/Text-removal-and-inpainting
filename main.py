import sys
import os
from glob import glob
from PyQt5.QtWidgets import QApplication, QFileDialog
from core.ocr import detect_text_boxes, extract_polygons, extract_text
from core.utils import load_image, build_mask_from_polygons
from core.inpaint import inpaint_image
from ui.manual_editor import ManualEditor

app = QApplication(sys.argv)
editor_window = None  # Keeps manual editor alive


def run_auto_on_single_image(image_path):
    print(f"⚙️ Auto-processing single image: {image_path}")
    image = load_image(image_path)
    results = detect_text_boxes(image_path)
    polygons = extract_polygons(results)
    mask = build_mask_from_polygons(polygons, image.size[::-1])
    texts = extract_text(results)

    result = inpaint_image(image, mask)

    base = os.path.basename(image_path)
    name, _ = os.path.splitext(base)

    os.makedirs("outputs/auto", exist_ok=True)
    os.makedirs("outputs/extracted_text", exist_ok=True)

    result_path = os.path.join("outputs/auto", f"{name}_auto_cleaned.jpg")
    result.save(result_path)
    print(f"✅ Saved image: {result_path}")

    # Save extracted text
    texts = [text for _, text, _ in detect_text_boxes(image_path)]
    text_path = os.path.join("outputs/extracted_text", f"{name}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        for line in texts:
            f.write(line + "\n")
    print(f"📄 Saved text: {text_path}")

def run_auto_on_folder(folder_path):
    print(f"⚙️ Auto-processing folder: {folder_path}")
    os.makedirs("outputs", exist_ok=True)
    image_paths = glob(os.path.join(folder_path, "*.jpg")) + glob(os.path.join(folder_path, "*.png"))
    if not image_paths:
        print("❌ No images found in folder.")
        return

    for img_path in image_paths:
        print(f"🖼️ Processing: {img_path}")
        image = load_image(img_path)
        results = detect_text_boxes(img_path)
        polygons = extract_polygons(results)
        mask = build_mask_from_polygons(polygons, image.size[::-1])
        texts = extract_text(results)

        result = inpaint_image(image, mask)

        name, _ = os.path.splitext(os.path.basename(img_path))
        result_path = os.path.join("outputs/auto", f"{name}_auto_cleaned.jpg")

        os.makedirs("outputs/auto", exist_ok=True)
        os.makedirs("outputs/extracted_text", exist_ok=True)
        result.save(result_path)

        texts = [text for _, text, _ in detect_text_boxes(img_path)]
        text_path = os.path.join("outputs/extracted_text", f"{name}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            for line in texts:
                f.write(line + "\n")

def run_manual_on_single_image(image_path):
    global editor_window

    if not image_path:
        print("❌ No image selected.")
        return

    print(f"🖼️ Opening manual editor for: {image_path}")
    editor_window = ManualEditor(image_path, lambda result: print("✅ Manual inpainting done."))
    editor_window.setWindowTitle("Manual Editor")
    editor_window.resize(1000, 700)
    editor_window.show()


def run_manual_on_folder(folder_path):
    global editor_window

    image_paths = glob(os.path.join(folder_path, "*.jpg")) + glob(os.path.join(folder_path, "*.png"))
    if not image_paths:
        print("❌ No images found in folder.")
        return

    print(f"📂 Found {len(image_paths)} images for manual editing.")

    def process_next(index=0):
        if index >= len(image_paths):
            print("✅ All images processed.")
            app.quit()
            return

        image_path = image_paths[index]
        print(f"🖼️ Editing {index + 1}/{len(image_paths)}: {image_path}")

        def on_done(_):
            print(f"✅ Done: {image_path}")
            process_next(index + 1)

        global editor_window
        editor_window = ManualEditor(image_path, on_done)
        editor_window.setWindowTitle(f"Manual Editor ({index + 1}/{len(image_paths)})")
        editor_window.resize(1000, 700)
        editor_window.show()

    process_next()
    app.exec_()


if __name__ == "__main__":
    print("🎛️ Welcome to the Text Removal Tool")
    mode = input("Choose editing mode (manual/auto): ").strip().lower()
    scope = input("Choose input type (single/folder): ").strip().lower()

    if mode not in ["manual", "auto"] or scope not in ["single", "folder"]:
        print("❌ Invalid mode or scope. Please use 'manual/auto' and 'single/folder'.")
        sys.exit()

    if scope == "single":
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Image")
        if not file_path:
            print("❌ No file selected.")
            sys.exit()

        if mode == "auto":
            run_auto_on_single_image(file_path)
            sys.exit()

        elif mode == "manual":
            run_manual_on_single_image(file_path)
            sys.exit(app.exec_())

    elif scope == "folder":
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if not folder_path:
            print("❌ No folder selected.")
            sys.exit()

        if mode == "auto":
            run_auto_on_folder(folder_path)
            sys.exit()

        elif mode == "manual":
            run_manual_on_folder(folder_path)
