# 🖼️ Image Batch Resizer & Compressor

A simple Python script that resizes and compresses multiple images at once. Drop your photos into a folder, run one command, and get optimized images ready for the web.

---

## Features

- Resizes images so the **maximum width is 1200px** (aspect ratio preserved)
- Compresses **JPEG** images at quality 85 (great balance of size vs. quality)
- Optimizes **PNG** images losslessly
- Supports `.jpg`, `.jpeg`, and `.png` files
- Shows clear progress with emojis for every image processed
- Gives a final count of successfully processed images

---

## Requirements

- Python 3.11+
- [Pillow](https://pillow.readthedocs.io/) library

Install Pillow if you haven't already:

```bash
pip install Pillow
```

---

## How to Use

### 1. Add your images

Put any `.jpg`, `.jpeg`, or `.png` images into the `input_images/` folder.  
(The folder is created automatically when you first run the script.)

### 2. Run the script

```bash
python3 main.py
```

### 3. Get your results

Processed images are saved to the `output_images/` folder, with the **same filenames** as the originals.

---

## Example Output

```
=======================================================
  🖼️  Image Batch Resizer & Compressor
=======================================================
  Max width   : 1200px
  JPEG quality: 85
  PNG optimize: True
=======================================================

📁 Folders ready:
   Input  → input_images/
   Output → output_images/

🔍 Found 3 image(s) to process...

   ✅ beach.jpg  (3840×2160 → 1200×675)
   ✅ logo.png   (800×600, no resize needed)
   ✅ portrait.jpeg  (2000×3000 → 1200×1800)

-------------------------------------------------------
🎉 Done! All 3 image(s) processed successfully.
📂 Output saved to: output_images/
-------------------------------------------------------
```

---

## Customizing Settings

Open `main.py` and edit the **SETTINGS** section near the top:

```python
MAX_WIDTH    = 1200   # Maximum output width in pixels
JPEG_QUALITY = 85     # JPEG quality: 1 (tiny/low quality) → 95 (large/high quality)
PNG_OPTIMIZE = True   # PNG optimization (lossless — always safe to leave on)
```

| Setting | Default | Description |
|---|---|---|
| `MAX_WIDTH` | `1200` | Images wider than this are resized down. Smaller images are left unchanged. |
| `JPEG_QUALITY` | `85` | Higher = better quality but larger file. Range: 1–95. |
| `PNG_OPTIMIZE` | `True` | Lossless PNG compression. No quality loss. |

---

## Folder Structure

```
project/
├── main.py           ← The script
├── README.md         ← This file
├── input_images/     ← Put your original images here
└── output_images/    ← Processed images appear here
```

---

## Notes

- Original files in `input_images/` are **never modified** — all output goes to `output_images/`.
- If a file with the same name already exists in `output_images/`, it will be **overwritten**.
- Images that are already smaller than `MAX_WIDTH` are compressed but **not enlarged**.
