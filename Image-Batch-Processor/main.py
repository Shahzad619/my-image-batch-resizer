"""
=============================================================
  Image Batch Resizer & Compressor
=============================================================
  Drop your images into the 'input_images' folder and run
  this script. It will resize and compress them, then save
  the results to 'output_images'.

  Supported formats: .jpg, .jpeg, .png
=============================================================
"""

import os
from pathlib import Path
from PIL import Image

# ─────────────────────────────────────────────
#  SETTINGS — Change these to suit your needs
# ─────────────────────────────────────────────

MAX_WIDTH = 1200        # Images wider than this will be resized (pixels)
JPEG_QUALITY = 85       # JPEG compression quality: 1 (worst) → 95 (best)
PNG_OPTIMIZE = True     # Run PNG optimizer (lossless, reduces file size)

# ─────────────────────────────────────────────
#  FOLDER PATHS
# ─────────────────────────────────────────────

INPUT_FOLDER = Path("input_images")
OUTPUT_FOLDER = Path("output_images")


def setup_folders() -> None:
    """Create the input and output folders if they don't exist yet."""
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    print("📁 Folders ready:")
    print(f"   Input  → {INPUT_FOLDER}/")
    print(f"   Output → {OUTPUT_FOLDER}/")


def find_images() -> list[Path]:
    """
    Scan the input folder for supported image files.

    Returns:
        A list of Path objects for every .jpg, .jpeg, and .png file found.
    """
    supported_extensions = {".jpg", ".jpeg", ".png"}
    images = [
        f for f in INPUT_FOLDER.iterdir()
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]
    return sorted(images)  # Sort alphabetically for consistent ordering


def resize_image(img: Image.Image) -> tuple[Image.Image, bool]:
    """
    Resize an image so its width does not exceed MAX_WIDTH.
    The aspect ratio is always preserved — the image is never stretched.

    Args:
        img: A PIL Image object.

    Returns:
        A tuple of (resized_image, was_resized).
        was_resized is False if the image was already small enough.
    """
    original_width, original_height = img.size

    # Only resize if the image is wider than the maximum allowed width
    if original_width <= MAX_WIDTH:
        return img, False

    # Calculate the new height to maintain the original aspect ratio
    scale_factor = MAX_WIDTH / original_width
    new_height = int(original_height * scale_factor)

    # LANCZOS gives the best quality when downscaling
    resized = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)
    return resized, True


def save_image(img: Image.Image, output_path: Path, original_format: str) -> None:
    """
    Save a processed image to the output folder with compression applied.

    JPEG images are saved with JPEG_QUALITY compression.
    PNG images are saved with lossless optimization.

    Args:
        img:             The PIL Image to save.
        output_path:     Where to write the file.
        original_format: The image format string (e.g. 'JPEG', 'PNG').
    """
    if original_format == "PNG":
        # PNG compression is lossless — optimize=True shrinks the file
        # without any quality loss
        img.save(output_path, format="PNG", optimize=PNG_OPTIMIZE)
    else:
        # JPEG: convert to RGB first (handles RGBA images, e.g. PNGs saved
        # as JPEG), then apply quality compression
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)


def process_image(image_path: Path) -> bool:
    """
    Open, resize, compress, and save a single image.

    Args:
        image_path: Path to the source image in the input folder.

    Returns:
        True if processing succeeded, False if an error occurred.
    """
    try:
        with Image.open(image_path) as img:
            original_format = img.format or "JPEG"
            original_width, original_height = img.size

            # Resize if needed
            img, was_resized = resize_image(img)
            new_width, new_height = img.size

            # Build the output path (keep the same filename)
            output_path = OUTPUT_FOLDER / image_path.name

            # Save with compression
            save_image(img, output_path, original_format)

        # Report what happened to this image
        if was_resized:
            print(
                f"   ✅ {image_path.name}  "
                f"({original_width}×{original_height} → {new_width}×{new_height})"
            )
        else:
            print(
                f"   ✅ {image_path.name}  "
                f"({original_width}×{original_height}, no resize needed)"
            )

        return True

    except Exception as error:
        print(f"   ❌ {image_path.name}  — Error: {error}")
        return False


def main() -> None:
    """
    Main entry point.
    Sets up folders, finds images, processes each one, and prints a summary.
    """
    print()
    print("=" * 55)
    print("  🖼️  Image Batch Resizer & Compressor")
    print("=" * 55)
    print(f"  Max width   : {MAX_WIDTH}px")
    print(f"  JPEG quality: {JPEG_QUALITY}")
    print(f"  PNG optimize: {PNG_OPTIMIZE}")
    print("=" * 55)
    print()

    # Make sure both folders exist
    setup_folders()
    print()

    # Find all supported images in the input folder
    images = find_images()

    if not images:
        print("⚠️  No images found in 'input_images'.")
        print("   Add some .jpg, .jpeg, or .png files and run the script again.")
        print()
        return

    print(f"🔍 Found {len(images)} image(s) to process...\n")

    # Process each image and track how many succeed
    success_count = 0
    for image_path in images:
        if process_image(image_path):
            success_count += 1

    # Final summary
    print()
    print("─" * 55)
    failed_count = len(images) - success_count
    if success_count == len(images):
        print(f"🎉 Done! All {success_count} image(s) processed successfully.")
    else:
        print(f"✅ {success_count} image(s) processed successfully.")
        print(f"❌ {failed_count} image(s) failed — check the errors above.")
    print(f"📂 Output saved to: {OUTPUT_FOLDER}/")
    print("─" * 55)
    print()


if __name__ == "__main__":
    main()
