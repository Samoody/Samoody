from pathlib import Path
import re

# Run after alexcerezo/activity-graph has generated the SVG files.
FILES = (Path("activity-graph.svg"), Path("activity-graph-mobile.svg"))

REPLACEMENTS = {
    "fill: #656d76;": "fill: #b8a6d9;",
    "fill: #8b949e;": "fill: #c4b5fd;",
    "rgba(0, 123, 58, 0.15)": "rgba(124, 58, 237, 0.45)",
    "rgba(0, 123, 58, 0.35)": "rgba(124, 58, 237, 0.70)",
    "rgba(0, 123, 58, 0.60)": "rgba(139, 92, 246, 0.92)",
    "rgba(0, 123, 58, 0.90)": "rgba(0, 229, 255, 1.0)",
    "rgba(57, 211, 83, 0.25)": "rgba(124, 58, 237, 0.50)",
    "rgba(57, 211, 83, 0.50)": "rgba(124, 58, 237, 0.75)",
    "rgba(57, 211, 83, 0.75)": "rgba(139, 92, 246, 0.95)",
    "rgba(57, 211, 83, 1.0)": "rgba(0, 229, 255, 1.0)",
    "rgba(57, 211, 83, 0.6)": "rgba(0, 229, 255, 0.75)",
    "rgba(0, 123, 58, 0.3)": "rgba(0, 229, 255, 0.5)",
    "rgba(0,123,58,0.25)": "rgba(124,58,237,0.35)",
    "rgba(0,123,58,0.35)": "rgba(124,58,237,0.50)",
    "rgba(0,123,58,0.2)": "rgba(124,58,237,0.30)",
    "rgba(0,123,58,0.4)": "rgba(0,229,255,0.45)",
    "rgba(0,123,58,0.05)": "rgba(124,58,237,0.06)",
    "rgba(0,123,58,0.03)": "rgba(124,58,237,0.04)",
    "rgba(0,123,58,0.5)": "rgba(0,229,255,0.55)",
    "rgba(0,123,58,0.07)": "rgba(0,229,255,0.08)",
    "rgba(57,211,83,0.4)": "rgba(124,58,237,0.55)",
    "rgba(57,211,83,0.5)": "rgba(124,58,237,0.65)",
    "rgba(57,211,83,0.3)": "rgba(0,229,255,0.35)",
    "rgba(57,211,83,0.6)": "rgba(0,229,255,0.70)",
    "rgba(57,211,83,0.7)": "rgba(0,229,255,0.80)",
    "rgba(57,211,83,0.55)": "rgba(0,229,255,0.60)",
}

for path in FILES:
    if not path.exists():
        continue

    svg = path.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        svg = svg.replace(old, new)

    # Use a dark base so the neon palette looks consistent in light and dark GitHub themes.
    if 'fill="#080713"' not in svg:
        match = re.search(r'(<rect\s+width="([^"]+)"\s+height="([^"]+)"\s+fill="url\(#bgGlow\)"\s*/>)', svg)
        if match:
            w, h = match.group(2), match.group(3)
            background = f'<rect width="{w}" height="{h}" fill="#080713"/>\n  '
            svg = svg[:match.start()] + background + svg[match.start():]

    path.write_text(svg, encoding="utf-8")
    print(f"Cyberpunk palette applied: {path}")
