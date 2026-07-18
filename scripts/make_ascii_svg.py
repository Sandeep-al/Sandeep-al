# scripts/make_ascii_svg.py
import cv2
import numpy as np

def main():
    img = cv2.imread("data/source-prepped.png", cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ Prepped photo not found! Run prep_photo.py first.")
        return

    # Resize to character grid (~100 columns wide, keeping aspect ratio)
    target_width = 100
    h, w = img.shape
    target_height = int((h / w) * target_width * 0.55) # 0.55 corrects terminal character stretch
    resized = cv2.resize(img, (target_width, target_height))

    # Sparse characters for bright areas, dense for dark
    RAMP = " `.-':_+*<=lxtzrcvnwOMW8#"
    num_chars = len(RAMP)

    svg_lines = []
    # Build lines row by row
    for y in range(target_height):
        row_str = ""
        for x in range(target_width):
            val = resized[y, x]
            char_idx = int((val / 255.0) * (num_chars - 1))
            char = RAMP[char_idx]
            # Escape HTML entities
            if char == '<': row_str += "&lt;"
            elif char == '>': row_str += "&gt;"
            elif char == '&': row_str += "&amp;"
            elif char == '"': row_str += "&quot;"
            else: row_str += char
        svg_lines.append(row_str)

    # Output Dimension Settings
    font_size = 13
    line_height = 15
    svg_width = target_width * 7.8
    svg_height = target_height * line_height + 20

    # Assemble SMIL self-typing SVG
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">\n'
    svg += '<style>\n'
    svg += '  .ascii { font-family: monospace; font-size: ' + str(font_size) + 'px; fill: #a6accd; white-space: pre; }\n'
    svg += '</style>\n'
    svg += '<rect width="100%" height="100%" fill="transparent"/>\n'
    svg += '<text x="10" y="20" class="ascii">\n'
    
    # Calculate staggered line typewriter delays
    for i, line in enumerate(svg_lines):
        delay = i * 0.06
        svg += f'  <tspan x="10" dy="{line_height if i > 0 else 0}">\n'
        svg += f'    {line}\n'
        svg += f'    <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{delay}s" fill="freeze" />\n'
        svg += '  </tspan>\n'
        
    svg += '</text>\n</svg>'

    with open("data/avi-ascii.svg", "w", encoding="utf-8") as f:
        f.write(svg)
        
    print("🎨 Animated ASCII SVG generated inside 'data/avi-ascii.svg'!")

if __name__ == "__main__":
    main()