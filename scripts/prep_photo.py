import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prepare_photo(input_path: str):
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Image not found: {input_file}")

    print(f"Loading: {input_file}")

    # Remove background
    image = Image.open(input_file).convert("RGBA")
    print("Removing background...")

    foreground = remove(image)

    # White background
    background = Image.new("RGBA", foreground.size, (255, 255, 255, 255))
    combined = Image.alpha_composite(background, foreground)

    # Convert to RGB
    rgb = np.array(combined.convert("RGB"))

    # Convert to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Light smoothing
    enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

    output_path = input_file.parent / "source-prepped.png"

    cv2.imwrite(
        str(output_path),
        enhanced
    )

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    prepare_photo(sys.argv[1])