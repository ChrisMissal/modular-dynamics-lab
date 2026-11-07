"""Dependency-free SVG visualizations. Figures are illustrative, not statistical tests."""
from html import escape


def growth_svg(rows: list[dict], selected_primes: list[int], base: int = 2) -> str:
    rows = [r for r in rows if r["base"] == base and r["p"] in selected_primes]
    if not rows:
        return ""
    panel_h, width = 145, 690
    height = 60 + panel_h * len(rows)
    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Cycle growth by prime power">',
        '<rect width="100%" height="100%" fill="#0e1726"/>',
        '<text x="28" y="32" fill="#f6f9ff" font-family="sans-serif" font-size="21">'
        f'Cycle growth for base {base}</text>',
    ]
    for i, row in enumerate(rows):
        y = 50 + i * panel_h
        p = row["p"]
        order = row["orders"]
        ratios = row["growth_ratios"]
        items.extend([
            f'<text x="28" y="{y+22}" fill="#f6f9ff" font-family="sans-serif" font-size="17">p = {p}</text>',
            f'<text x="28" y="{y+45}" fill="#a4b6c9" font-family="sans-serif" font-size="12">'
            f'Orders: {escape(" → ".join(map(str, order)))}</text>',
        ])
        for j, factor in enumerate(ratios):
            x = 65 + j * 240
            bar_width = 170 if factor == p else 10
            color = '#efad5c' if factor == p else '#48c8bb'
            label = f'×{factor} ({"grows" if factor == p else "flat"})'
            items.extend([
                f'<text x="{x}" y="{y+70}" fill="#cfdbe9" font-family="sans-serif" font-size="12">'
                f'p^{j+1} → p^{j+2}</text>',
                f'<rect x="{x}" y="{y+80}" width="{bar_width}" height="22" rx="4" fill="{color}"/>',
                f'<text x="{x}" y="{y+120}" fill="#f6f9ff" font-family="sans-serif" font-size="12">{label}</text>',
            ])
    items.append('</svg>')
    return '\n'.join(items) + '\n'


def harmonic_svg(walks: dict[int, list[int]], selected_primes: list[int]) -> str:
    targets = [(p, walks[p]) for p in selected_primes if p in walks]
    if not targets:
        return ""
    width, panel_h = 730, 200
    height = 60 + panel_h * len(targets)
    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Modular harmonic-sum walks">',
        '<rect width="100%" height="100%" fill="#0e1726"/>',
        '<text x="28" y="30" fill="#f6f9ff" font-family="sans-serif" font-size="21">'
        'Harmonic walks: normalized residues H_k mod p</text>',
    ]
    for index, (p, walk) in enumerate(targets):
        top = 56 + index * panel_h
        x0, x1 = 60, 690
        y0, y1 = top + 30, top + 153
        items.extend([
            f'<text x="28" y="{top+16}" fill="#f6f9ff" font-family="sans-serif" font-size="16">p = {p}</text>',
            f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#44556b"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#44556b"/>',
        ])
        points = ' '.join(f'{x0+(x1-x0)*j/(len(walk)-1):.2f},'
                          f'{y1-(y1-y0)*v/p:.2f}' for j, v in enumerate(walk))
        items.append(f'<polyline points="{points}" fill="none" stroke="#48c8bb" '
                     'stroke-width="1.4" opacity="0.90"/>')
        for j, v in enumerate(walk[1:], 1):
            if v == 0:
                x = x0 + (x1 - x0) * j / (len(walk) - 1)
                items.append(f'<circle cx="{x:.2f}" cy="{y1}" r="5" fill="#efad5c"/>')
        zeros = [j for j, v in enumerate(walk) if j > 0 and v == 0]
        items.append(f'<text x="{x1}" y="{top+16}" text-anchor="end" '
                     'fill="#efad5c" font-family="sans-serif" font-size="12">'
                     f'zero returns: {escape(str(zeros))}</text>')
    items.append('</svg>')
    return '\n'.join(items) + '\n'
