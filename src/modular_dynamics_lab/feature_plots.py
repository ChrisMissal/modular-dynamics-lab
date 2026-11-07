"""Deterministic SVG research figures; no third-party plotting dependencies."""
from html import escape

BG = "#0b1325"
PANEL = "#111f35"
GRID = "#32445e"
TEXT = "#edf4fc"
MUTED = "#a6bad1"
TEAL = "#45ddc7"
AMBER = "#ffbb69"
LILAC = "#b5a2ff"


def _txt(x: float, y: float, value: object, *, size: int = 14,
         color: str = TEXT, anchor: str = "start", weight: str = "400") -> str:
    return (f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" '
            f'font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')


def _rect(x: float, y: float, w: float, h: float, fill: str, radius: int = 12,
          stroke: str | None = None) -> str:
    outline = f' stroke="{stroke}"' if stroke else ""
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{radius}" fill="{fill}"{outline}/>')


def _circle(x: float, y: float, r: float, fill: str, opacity: float = 1) -> str:
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{fill}" opacity="{opacity}"/>'


def feature_space_svg(rows: list[dict], focus_primes: list[int]) -> str:
    """Exact cross-base order fractions are points; focus vectors run from origin.

    Axes are order_p(2)/(p-1) and order_p(3)/(p-1), not PCA nor distances.
    """
    by_p: dict[int, dict[int, dict]] = {}
    for record in rows:
        by_p.setdefault(record["p"], {})[record["base"]] = record
    pairs = {p: v for p, v in by_p.items() if 2 in v and 3 in v}
    width, height = 1120, 662
    px0, px1, py0, py1 = 90, 603, 150, 550
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Prime order feature space and lift signature</title>',
        '<desc id="chart-desc">Each dot is a prime with x equal to the normalized order of 2 and y to the normalized order of 3. Highlighted arrows locate Wieferich primes 1093 and 3511. A right panel compares growth over prime powers.</desc>',
        _rect(0, 0, width, height, BG, 0),
        _txt(48, 46, "02 / PRIME FEATURE SPACE", size=15, color=TEAL, weight="700"),
        _txt(48, 89, "Where do the exceptional primes intersect?", size=29, weight="700"),
        _txt(48, 114, "Exact order fractions across bases 2 and 3 · visual comparison, not a statistical claim", size=14, color=MUTED),
        _rect(36, 135, 624, 472, PANEL),
        _rect(676, 135, 407, 472, PANEL),
    ]
    for tick in (0, 0.25, 0.5, 0.75, 1):
        x = px0 + (px1 - px0) * tick
        y = py1 - (py1 - py0) * tick
        parts.append(f'<line x1="{x:.2f}" y1="{py0}" x2="{x:.2f}" y2="{py1}" stroke="{GRID}" stroke-dasharray="3 5"/>')
        parts.append(f'<line x1="{px0}" y1="{y:.2f}" x2="{px1}" y2="{y:.2f}" stroke="{GRID}" stroke-dasharray="3 5"/>')
        parts.append(_txt(x, py1 + 20, f"{tick:g}", size=11, color=MUTED, anchor="middle"))
        parts.append(_txt(px0 - 13, y + 4, f"{tick:g}", size=11, color=MUTED, anchor="end"))
    parts.append(_txt((px0 + px1) / 2, py1 + 43, "ordₚ(2) / (p − 1)", size=15, color=TEXT, anchor="middle"))
    parts.append(f'<text x="51" y="350" fill="{TEXT}" font-family="sans-serif" font-size="15" text-anchor="middle" transform="rotate(-90 51 350)">ordₚ(3) / (p − 1)</text>')
    for p, values in sorted(pairs.items()):
        if p in focus_primes:
            continue
        x = px0 + (px1 - px0) * values[2]["orders"][0] / (p - 1)
        y = py1 - (py1 - py0) * values[3]["orders"][0] / (p - 1)
        parts.append(_circle(x, y, 2.1, MUTED, 0.28))
    parts.insert(4, '<defs><marker id="vector-head" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#ffbb69"/></marker></defs>')
    focus_colors = (AMBER, TEAL, LILAC)
    for index, p in enumerate(focus_primes):
        values = pairs.get(p)
        if not values:
            continue
        x = px0 + (px1 - px0) * values[2]["orders"][0] / (p - 1)
        y = py1 - (py1 - py0) * values[3]["orders"][0] / (p - 1)
        color = focus_colors[index % len(focus_colors)]
        parts.append(f'<path d="M {px0} {py1} L {x:.2f} {y:.2f}" fill="none" stroke="{color}" stroke-width="2.3" opacity="0.85"/>')
        parts.append(_circle(x, y, 9, color, 0.19))
        parts.append(_circle(x, y, 4.2, color))
        parts.append(_txt(x + 11, y - 9, str(p), size=16, color=color, weight="700"))
    parts.extend([
        _txt(701, 169, "LIFT GROWTH / BASE 2", size=15, color=TEAL, weight="700"),
        _txt(701, 195, "Cycle period from p to p² to p³", size=14, color=MUTED),
        _txt(826, 243, "p → p²", size=13, color=MUTED, anchor="middle"),
        _txt(969, 243, "p² → p³", size=13, color=MUTED, anchor="middle"),
    ])
    for i, p in enumerate([7] + [p for p in focus_primes if p != 7]):
        y = 265 + 84 * i
        if p not in by_p or 2 not in by_p[p]:
            continue
        ratios = by_p[p][2]["growth_ratios"]
        parts.append(_txt(701, y + 31, f"p={p}", size=17, weight="600", color=AMBER if p in focus_primes else TEXT))
        for j, ratio in enumerate(ratios):
            x = 779 + j * 143
            flat = ratio == 1
            parts.append(_rect(x, y, 94, 42, "#173e44" if flat else "#4a3032", 9))
            parts.append(_txt(x + 47, y + 27, f"×{ratio}", size=17, anchor="middle", color=TEAL if flat else AMBER, weight="700"))
    parts.extend([
        _txt(700, 557, "Flat lift (×1) is the defining base-2 anomaly.", size=12, color=MUTED),
        _txt(48, 640, "Vectors show exact fractions, not independent dimensions; qₚ(2)=0 is already encoded by the flat lift.", size=13, color=MUTED),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


def harmonic_intersections_svg(rows: list[dict], focus_primes: list[int], neighbors: int) -> str:
    """Zero-return intersection strip charts for equally sized prime neighborhoods."""
    by_p = {row["p"]: row for row in rows}
    primes = sorted(by_p)
    width, height = 1100, 930
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Harmonic zero-return intersections near Wieferich primes</title>',
        '<desc id="chart-desc">Each line is a prime. Marks indicate k where the discrete harmonic sum H_k equals zero modulo that prime. Known theorem-forced crossings are highlighted only for the two Wieferich primes.</desc>',
        _rect(0, 0, width, height, BG, 0),
        _txt(46, 45, "02 / MODULAR INTERSECTIONS", size=15, color=TEAL, weight="700"),
        _txt(46, 85, "When does a harmonic walk hit zero?", size=29, weight="700"),
        _txt(46, 111, "Discrete modular intersections, normalized by the half-walk length · nearby-prime comparisons", size=14, color=MUTED),
    ]
    x0, x1 = 240, 1022
    for panel_index, focus in enumerate(focus_primes[:2]):
        if focus not in by_p:
            continue
        pos = primes.index(focus)
        subset = primes[max(0, pos - neighbors):min(len(primes), pos + neighbors + 1)]
        top = 144 + panel_index * 385
        parts.append(_rect(35, top, width - 70, 365, PANEL))
        parts.append(_txt(60, top + 32, f"FOCUS {focus}", size=18, color=AMBER, weight="700"))
        parts.append(_txt(287, top + 30, f"{len(subset)} nearby primes · Hₖ = 0 (mod p)", size=14, color=MUTED))
        axis_top = top + 62
        row_h = 9.0
        # 29 rows at 9 px = 261 px, leaving room for axis labels.
        for tick, label in [(0, "0"), (0.25, "¼"), (0.5, "½"), (0.75, "¾"), (1, "1")]:
            x = x0 + tick * (x1 - x0)
            parts.append(f'<line x1="{x:.2f}" y1="{axis_top}" x2="{x:.2f}" y2="{axis_top + (len(subset)-1)*row_h + 6:.2f}" stroke="{GRID}" stroke-dasharray="3 6"/>')
            parts.append(_txt(x, top + 347, label, size=12, color=MUTED, anchor="middle"))
        for row_num, p in enumerate(subset):
            y = axis_top + row_num * row_h + 5
            d = by_p[p]
            is_focus = p == focus
            if is_focus:
                parts.append(_rect(48, y - 4.7, 1000, 9.4, "#30404d", 3))
            if row_num % 4 == 0 or is_focus:
                parts.append(_txt(198, y + 3, str(p), size=11, color=AMBER if is_focus else MUTED,
                                  anchor="end", weight="700" if is_focus else "400"))
            for k in d["zero_indices"]:
                x = x0 + (x1 - x0) * k / d["half_length"]
                forced = k in d["forced_zero_indices"]
                color = AMBER if forced else TEAL
                if forced:
                    points = f'{x:.2f},{y-5:.2f} {x+5:.2f},{y:.2f} {x:.2f},{y+5:.2f} {x-5:.2f},{y:.2f}'
                    parts.append(f'<polygon points="{points}" fill="{color}"/>')
                else:
                    parts.append(_circle(x, y, 3.0 if is_focus else 2.4, color, .95 if is_focus else .55))
        parts.append(_txt((x0 + x1) / 2, top + 363, "Relative step k / ((p−1)/2)", size=12,
                          color=MUTED, anchor="middle"))
    parts.extend([
        _circle(50, 916, 4, TEAL), _txt(64, 921, "Observed zero return", size=12, color=MUTED),
        f'<polygon points="264,911 269,916 264,921 259,916" fill="{AMBER}"/>',
        _txt(284, 921, "Known theorem-forced crossing for a Wieferich prime", size=12, color=MUTED),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"
