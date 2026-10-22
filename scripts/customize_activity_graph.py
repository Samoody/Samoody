
from pathlib import Path
import re

FILES = (
    Path("activity-graph.svg"),
    Path("activity-graph-mobile.svg"),
)

# Paleta Cyberpunk: roxo neon + ciano elétrico
CYBERPUNK_CSS = """
.level-0 { fill: transparent; stroke: none; }
.level-1 { fill: rgba(124, 58, 237, 0.35); }
.level-2 { fill: rgba(124, 58, 237, 0.65); }
.level-3 { fill: rgba(139, 92, 246, 0.90); }
.level-4 { fill: rgba(0, 229, 255, 1.0); }

.bg-star {
    fill: rgba(0, 229, 255, 0.65);
}
"""

def customize_svg(path):
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return

    svg = path.read_text(encoding="utf-8")

    # Substitui as regras de contribuição, independentemente
    # das cores verdes usadas pelo gerador.
    svg = re.sub(
        r"\.level-0\s*\{[^}]*\}"
        r"|\ .level-1\s*\{[^}]*\}"
        r"|\ .level-2\s*\{[^}]*\}"
        r"|\ .level-3\s*\{[^}]*\}"
        r"|\ .level-4\s*\{[^}]*\}",
        lambda m: m.group(0),
        svg,
    ) if False else svg

    # Atualiza cada classe de contribuição em todos os temas.
    levels = {
        0: "fill: transparent; stroke: none;",
        1: "fill: rgba(124, 58, 237, 0.35);",
        2: "fill: rgba(124, 58, 237, 0.65);",
        3: "fill: rgba(139, 92, 246, 0.90);",
        4: "fill: rgba(0, 229, 255, 1.0);",
    }

    for level, declaration in levels.items():
        pattern = rf"\.level-{level}\s*\{{[^}}]*\}}"
        replacement = f".level-{level} {{ {declaration} }}"
        svg = re.sub(pattern, replacement, svg)

    # Troca os verdes dos efeitos de brilho por roxo/ciano.
    svg = re.sub(
        r"rgba\(\s*0\s*,\s*123\s*,\s*58\s*,\s*[\d.]+\s*\)",
        "rgba(124, 58, 237, 0.55)",
        svg,
    )
    svg = re.sub(
        r"rgba\(\s*57\s*,\s*211\s*,\s*83\s*,\s*[\d.]+\s*\)",
        "rgba(0, 229, 255, 0.75)",
        svg,
    )

    # Textos em lilás para contrastar com o fundo escuro.
    svg = svg.replace("#656d76", "#c4b5fd")
    svg = svg.replace("#8b949e", "#b8a6d9")

    # Mantém um fundo escuro consistente.
    if 'fill="#080713"' not in svg:
        match = re.search(
            r'<rect\b(?=[^>]*\bwidth="([^"]+)")'
            r'(?=[^>]*\bheight="([^"]+)")'
            r'(?=[^>]*\bfill="url\(#bgGlow\)")'
            r'[^>]*/>',
            svg,
        )

        if match:
            width, height = match.group(1), match.group(2)
            background = (
                f'<rect width="{width}" height="{height}" '
                'fill="#080713"/>'
            )
            svg = svg[:match.start()] + background + "\n  " + svg[match.start():]

    # Reduz a altura apenas do gráfico desktop, sem cortar o viewBox.
    if path.name == "activity-graph.svg":
        svg = re.sub(
            r'(<svg\b[^>]*\bwidth="845"[^>]*\bheight=")135(")',
            r'\g<1>120\2',
            svg,
            count=1,
        )

    path.write_text(svg, encoding="utf-8")
    print(f"Cyberpunk aplicado: {path}")


for file in FILES:
    customize_svg(file)
