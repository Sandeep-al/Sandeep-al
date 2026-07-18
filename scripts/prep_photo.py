# scripts/prep_photo.py
import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <path_to_photo>")
        return
        
    input_path = sys.argv[1]
    output_path = "data/source-prepped.png"
    
    print("⏳ Removing background...")
    input_img = Image.open(input_path)
    no_bg = remove(input_img)
    
    # Convert PIL Image back to OpenCV format
    img_np = np.array(no_bg)
    
    # Extract channels
    if img_np.shape[2] == 4:
        r, g, b, alpha = cv2.split(img_np)
        gray = cv2.cvtColor(cv2.merge([r, g, b]), cv2.COLOR_RGB2GRAY)
        
        # Composite onto pure white background where alpha is 0
        white_bg = np.ones_like(gray) * 255
        mask = alpha / 255.0
        gray = (gray * mask + white_bg * (1.0 - mask)).astype(np.uint8)
    else:
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
    print("✨ Optimizing contrast...")
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    prepped = clahe.apply(gray)
    
    cv2.imwrite(output_path, prepped)
    print(f"✅ Prepped photo saved to: {output_path}")

if __name__ == "__main__":
    main()