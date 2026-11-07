"""Deterministic SVG research figures; no third-party plotting dependencies."""
from html import escape
from math import log2

from .feature_coordinates import coordinate_groups

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
    """Aggregate exact order-fraction coincidences; encode multiplicity in glyph size.

    SVG geometry uses floats only after rational equivalence has been established.
    """
    by_p: dict[int, dict[int, dict]] = {}
    for record in rows:
        by_p.setdefault(record["p"], {})[record["base"]] = record
    groups = coordinate_groups(rows)
    growth_primes = [p for p in ([7] + focus_primes) if p in by_p and 2 in by_p[p]]
    growth_primes = list(dict.fromkeys(growth_primes))
    width = 1120
    panel_height = max(472, 168 + 84 * len(growth_primes) + 35)
    height = max(662, 135 + panel_height + 52)
    px0, px1, py0, py1 = 90, 603, 150, 550
    total = sum(g["multiplicity"] for g in groups)
    max_count = max((g["multiplicity"] for g in groups), default=0)
    shared = sum(1 for g in groups if g["multiplicity"] > 1)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Prime order feature space and exact intersection multiplicity</title>',
        '<desc id="chart-desc">A circle is one exact pair of reduced order fractions. Circle size represents the number of primes sharing the coordinate. Focus vectors locate selected primes. The right panel shows how base-2 cycle lengths grow over prime powers.</desc>',
        _rect(0, 0, width, height, BG, 0),
        _txt(48, 46, "02 / PRIME FEATURE SPACE", size=15, color=TEAL, weight="700"),
        _txt(48, 89, "Where do the exceptional primes intersect?", size=29, weight="700"),
        _txt(48, 114, "Exact rational coordinates · circle size shows shared-prime count", size=14, color=MUTED),
        _rect(36, 135, 624, 472, PANEL),
        _rect(676, 135, 407, panel_height, PANEL),
    ]
    for tick in (0, 0.25, 0.5, 0.75, 1):
        x = px0 + (px1 - px0) * tick
        y = py1 - (py1 - py0) * tick
        parts.append(f'<line x1="{x:.2f}" y1="{py0}" x2="{x:.2f}" y2="{py1}" stroke="{GRID}" stroke-dasharray="3 5"/>')
        parts.append(f'<line x1="{px0}" y1="{y:.2f}" x2="{px1}" y2="{y:.2f}" stroke="{GRID}" stroke-dasharray="3 5"/>')
        parts.append(_txt(x, py1 + 20, f"{tick:g}", size=11, color=MUTED, anchor="middle"))
        parts.append(_txt(px0 - 13, y + 4, f"{tick:g}", size=11, color=MUTED, anchor="end"))
    parts.append(_txt((px0 + px1) / 2, py1 + 43, "ordₚ(2) / (p − 1)", size=15, anchor="middle"))
    parts.append(f'<text x="51" y="350" fill="{TEXT}" font-family="sans-serif" font-size="15" text-anchor="middle" transform="rotate(-90 51 350)">ordₚ(3) / (p − 1)</text>')
    # Exactly one plotted glyph per distinct rational coordinate, with a tooltip giving
    # all prime identifiers. This preserves coincidences even if two floats round alike.
    for g in groups:
        x = px0 + (px1 - px0) * g["order2_num"] / g["order2_den"]
        y = py1 - (py1 - py0) * g["order3_num"] / g["order3_den"]
        radius = 2.3 + 1.65 * log2(g["multiplicity"])
        title = (f'{g["order2_num"]}/{g["order2_den"]}, '
                 f'{g["order3_num"]}/{g["order3_den"]}: '
                 f'{g["multiplicity"]} primes ({", ".join(map(str, g["primes"]))})')
        parts.append(f'<g class="intersection" data-multiplicity="{g["multiplicity"]}">'
                     f'<title>{escape(title)}</title>'
                     + _circle(x, y, radius, MUTED, 0.28 + 0.06 * min(4, log2(g["multiplicity"])))
                     + '</g>')
    focus_colors = (AMBER, TEAL, LILAC)
    for index, p in enumerate(focus_primes):
        values = by_p.get(p)
        if not values or 2 not in values or 3 not in values:
            continue
        x = px0 + (px1 - px0) * values[2]["orders"][0] / (p - 1)
        y = py1 - (py1 - py0) * values[3]["orders"][0] / (p - 1)
        color = focus_colors[index % len(focus_colors)]
        parts.append(f'<path d="M {px0} {py1} L {x:.2f} {y:.2f}" fill="none" stroke="{color}" stroke-width="2.3" opacity="0.85"/>')
        parts.append(_circle(x, y, 8, color, 0.20))
        parts.append(_circle(x, y, 4, color))
        # Offset labels as the focus count grows, without altering mathematical coordinates.
        parts.append(_txt(x + 12, y - 9 - index % 2 * 15, str(p), size=15, color=color, weight="700"))
    parts.append(_txt(55, 613, f"{total:,} primes at {len(groups)} exact coordinates · {shared} shared coordinates · max {max_count} primes per coordinate", size=11, color=MUTED))
    parts.extend([
        _txt(701, 169, "LIFT GROWTH / BASE 2", size=15, color=TEAL, weight="700"),
        _txt(701, 195, "Cycle period from p to p² to p³", size=14, color=MUTED),
        _txt(826, 243, "p → p²", size=13, color=MUTED, anchor="middle"),
        _txt(969, 243, "p² → p³", size=13, color=MUTED, anchor="middle"),
    ])
    for i, p in enumerate(growth_primes):
        y = 265 + 84 * i
        ratios = by_p[p][2]["growth_ratios"]
        parts.append(_txt(701, y + 31, f"p={p}", size=16, weight="600", color=AMBER if p in focus_primes else TEXT))
        for j, ratio in enumerate(ratios):
            x = 779 + j * 143
            flat = ratio == 1
            parts.append(_rect(x, y, 94, 42, "#173e44" if flat else "#4a3032", 9))
            parts.append(_txt(x + 47, y + 27, f"×{ratio}", size=17, anchor="middle", color=TEAL if flat else AMBER, weight="700"))
    parts.extend([
        _txt(700, 135 + panel_height - 23, "Flat lift (×1) is the defining base-2 anomaly.", size=12, color=MUTED),
        _txt(48, height - 20, "Coordinates are arithmetic order ratios, not physical dimensions or evidence of new theorems.", size=13, color=MUTED),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


def harmonic_intersections_svg(rows: list[dict], focus_primes: list[int], neighbors: int) -> str:
    """Render *all* selected primes with panels sized to their actual neighborhoods."""
    by_p = {row["p"]: row for row in rows}
    primes = sorted(by_p)
    width = 1100
    x0, x1 = 240, 1022
    row_h = 10.5
    panels: list[tuple[int, list[int], float, float]] = []
    top = 144.0
    for focus in focus_primes:
        if focus not in by_p:
            raise ValueError(f"focus prime {focus} absent from harmonic dataset")
        pos = primes.index(focus)
        subset = primes[max(0, pos - neighbors):min(len(primes), pos + neighbors + 1)]
        # 62px header, N data rows, 42px for axis, and 16px lower padding.
        panel_h = 62 + len(subset) * row_h + 52
        panels.append((focus, subset, top, panel_h))
        top += panel_h + 20
    legend_y = top + 5
    height = int(legend_y + 36)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Harmonic zero-return intersections for selected primes</title>',
        '<desc id="chart-desc">Each horizontal row represents one odd prime. A point indicates a discrete modular harmonic sum equal to zero; diamonds indicate positions forced by known congruences for a base-2 Wieferich prime. The SVG has one dynamically sized panel per focus prime.</desc>',
        _rect(0, 0, width, height, BG, 0),
        _txt(46, 45, "02 / MODULAR INTERSECTIONS", size=15, color=TEAL, weight="700"),
        _txt(46, 85, "When does a harmonic walk hit zero?", size=29, weight="700"),
        _txt(46, 111, "Discrete modular intersections, normalized by half-walk length · nearby-prime comparisons", size=14, color=MUTED),
    ]
    for focus, subset, panel_top, panel_h in panels:
        parts.append(f'<g data-focus="{focus}">')
        parts.append(_rect(35, panel_top, width - 70, panel_h, PANEL))
        parts.append(_txt(60, panel_top + 32, f"FOCUS {focus}", size=18, color=AMBER, weight="700"))
        parts.append(_txt(287, panel_top + 30, f"{len(subset)} nearby primes · Hₖ = 0 (mod p)", size=14, color=MUTED))
        axis_top = panel_top + 62
        bottom = axis_top + len(subset) * row_h
        for tick, label in [(0, "0"), (0.25, "¼"), (0.5, "½"), (0.75, "¾"), (1, "1")]:
            x = x0 + tick * (x1 - x0)
            parts.append(f'<line x1="{x:.2f}" y1="{axis_top:.2f}" x2="{x:.2f}" y2="{bottom:.2f}" stroke="{GRID}" stroke-dasharray="3 6"/>')
            parts.append(_txt(x, bottom + 18, label, size=12, color=MUTED, anchor="middle"))
        for row_num, p in enumerate(subset):
            y = axis_top + row_num * row_h + row_h / 2
            data = by_p[p]
            is_focus = p == focus
            if is_focus:
                parts.append(_rect(48, y - row_h/2, 1000, row_h, "#30404d", 3))
            if row_num % 4 == 0 or is_focus:
                parts.append(_txt(198, y + 3, str(p), size=11, color=AMBER if is_focus else MUTED,
                                  anchor="end", weight="700" if is_focus else "400"))
            for k in data["zero_indices"]:
                x = x0 + (x1 - x0) * k / data["half_length"]
                forced = k in data["forced_zero_indices"]
                if forced:
                    points = f'{x:.2f},{y-5:.2f} {x+5:.2f},{y:.2f} {x:.2f},{y+5:.2f} {x-5:.2f},{y:.2f}'
                    parts.append(f'<polygon points="{points}" fill="{AMBER}"/>')
                else:
                    parts.append(_circle(x, y, 3 if is_focus else 2.4, TEAL, 0.95 if is_focus else 0.55))
        parts.append(_txt((x0 + x1) / 2, panel_top + panel_h - 12, "Relative step k / ((p−1)/2)",
                          size=12, color=MUTED, anchor="middle"))
        parts.append('</g>')
    parts.extend([
        _circle(50, legend_y, 4, TEAL), _txt(64, legend_y + 5, "Observed zero return", size=12, color=MUTED),
        f'<polygon points="264,{legend_y-5:.2f} 269,{legend_y:.2f} 264,{legend_y+5:.2f} 259,{legend_y:.2f}" fill="{AMBER}"/>',
        _txt(284, legend_y + 5, "Known theorem-forced crossing for a Wieferich prime", size=12, color=MUTED),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"
