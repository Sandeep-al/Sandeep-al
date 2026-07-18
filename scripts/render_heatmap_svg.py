# scripts/render_heatmap_svg.py
import json
from datetime import datetime

def main():
    try:
        with open("data/contributions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Contribution data file not found! Run fetch_contributions.py first.")
        return

    if not data:
        print("❌ Data file is empty.")
        return

    # Filter down to just the last 53 weeks (approx 371 days) to keep standard grid size
    grid_data = data[-371:]
    
    # Calculate stats summary
    total_contribs = sum(day['count'] for day in grid_data)
    
    # GitHub Classic Theme Palette Matrix
    PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    
    # Dimensions configuration
    box_size = 10
    box_gap = 3
    header_height = 30
    footer_height = 35
    
    columns = 53
    rows = 7
    width = columns * (box_size + box_gap) + 30
    height = rows * (box_size + box_gap) + header_height + footer_height

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'
    svg += '<style>\n'
    svg += '  .text { font-family: monospace; font-size: 12px; fill: #a6accd; }\n'
    svg += '  .title-grid { font-weight: bold; fill: #89ddff; }\n'
    svg += '  .rect-box { rx: 2px; ry: 2px; opacity: 0; }\n'
    svg += '</style>\n'
    svg += '<rect width="100%" height="100%" fill="transparent"/>\n'
    
    # Title text segment
    svg += f'<text x="10" y="20" class="text title-grid">sandeep-al ~ $ ./contributions.sh</text>\n'

    # Build the calendar grid
    for col in range(columns):
        for row in range(rows):
            idx = col * rows + row
            if idx >= len(grid_data):
                break
                
            day_info = grid_data[idx]
            level = min(day_info['level'], 4)
            color = PALETTE[level]
            
            x = 15 + col * (box_size + box_gap)
            y = header_height + row * (box_size + box_gap)
            
            # Diagonal structural fade-in loading effect (SMIL)
            delay = (col + row) * 0.02
            
            svg += f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" class="rect-box">\n'
            svg += f'    <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay}s" fill="freeze"/>\n'
            svg += f'  </rect>\n'

    # Add interactive live metrics summary footer
    footer_y = height - 15
    svg += f'<text x="15" y="{footer_y}" class="text">📊 Total Contributions (Past Year): {total_contribs} submissions</text>\n'
    svg += '</svg>'

    with open("data/contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)
        
    print("📈 Animated live contribution calendar rendered inside 'data/contrib-heatmap.svg'!")

if __name__ == "__main__":
    main()