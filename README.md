# 🖼️ AutoMEE – Text Removal Tool (Local AI Inpainting)

## ✅ Setup Instructions (First Time Only)

### 1. **Install Python 3.10**
Download and install Python 3.10.11 from the official website:  
👉 https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

During installation:
- ✅ Check **"Add Python to PATH"**
- ✅ Use "Customize installation" and enable `pip` and `environment variables`

---

### 2. **Create and activate a virtual environment**

Open PowerShell in the project folder and run:

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

---

### 3. **Install dependencies**

Make sure you have a file named `requirements.txt` in the project folder.

Run:

```powershell
pip install -r requirements.txt
```

---

## 🚀 Running the App

To launch the app, just run:

```powershell
python main.py
```

You’ll be prompted with two options:

1. **Choose editing mode**:  
   - `manual` – You draw on the image to remove specific text  
   - `auto` – The app automatically detects and removes text

2. **Choose input type**:  
   - `single` – Edit just one image  
   - `folder` – Process all images in a folder

---

## ✍️ Manual Mode

- You’ll draw over the text you want removed using your mouse
- Click **"Apply Inpainting"** to fill in the marked regions
- If using `folder` mode, it will move to the next image automatically

---

## ⚙️ Auto Mode

- The app uses OCR to detect text boxes automatically
- Those areas are masked and inpainted automatically without user input

---

## 📁 Output Files

Cleaned and processed images will be saved to:

```
outputs/
├── auto/           ← Auto-processed images
├── manual/         ← Manual-processed images
└── extracted_text/ ← Text recognized from auto mode (one .txt per image)
```
