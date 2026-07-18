# scripts/make_info_card.py
import datetime

def main():
    # Card metadata based on your profile
    username = "sandeep-al"
    host = "github"
    title = f"{username}@{host}"
    underline = "-" * len(title)
    
    # Extract data from your profile layout
    info_rows = [
        ("Name", "Sandeep Kumar"),
        ("OS", "IIIT Delhi Undergraduate"),
        ("Focus", "DSA, Backend Development, Systems Programming"),
        ("Languages", "C, C++, Java, Python, JavaScript"),
        ("Web Dev", "HTML5, CSS3, Node.js"),
        ("Tools", "Git, GitHub, Java Swing"),
        ("Profiles", "LeetCode (asym_ptotic)")
    ]
    
    # SVG Configuration
    font_size = 14
    line_height = 22
    start_y = 35
    card_width = 490
    card_height = start_y + (len(info_rows) + 2) * line_height + 20

    # Build the Neofetch SVG template
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{card_width}" height="{card_height}">\n'
    svg += '<style>\n'
    svg += '  .terminal { font-family: monospace; font-size: ' + str(font_size) + 'px; white-space: pre; }\n'
    svg += '  .title { fill: #c792ea; font-weight: bold; }\n'
    svg += '  .divider { fill: #89ddff; }\n'
    svg += '  .key { fill: #addb67; font-weight: bold; }\n'
    svg += '  .val { fill: #a6accd; }\n'
    svg += '</style>\n'
    svg += '<rect width="100%" height="100%" fill="transparent"/>\n'
    svg += '<text x="15" y="' + str(start_y) + '" class="terminal">\n'
    
    # 1. Add Title (sandeep-al@github)
    svg += f'  <tspan class="title">{title}</tspan>\n'
    svg += f'  <tspan x="15" dy="{line_height}" class="divider">{underline}</tspan>\n'
    
    # 2. Add Info Rows with Staggered Fade-in Animations
    for i, (key, val) in enumerate(info_rows):
        delay = (i + 1) * 0.15
        svg += f'  <tspan x="15" dy="{line_height}">\n'
        svg += f'    <tspan class="key">{key}: </tspan><tspan class="val">{val}</tspan>\n'
        svg += f'    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{delay}s" fill="freeze" />\n'
        svg += f'  </tspan>\n'
        
    svg += '</text>\n</svg>'
    
    with open("data/info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
        
    print("📋 Neofetch info card SVG generated inside 'data/info-card.svg'!")

if __name__ == "__main__":
    main()