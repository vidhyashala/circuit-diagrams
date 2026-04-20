from pathlib import Path
import math

OUT = Path('figures')
OUT.mkdir(exist_ok=True)

profiles = [
    ('hybrid_dab_boost_pid', 2.8, 1.20, 95.8, 3.4),
    ('interleaved_coupled_fuzzy', 2.4, 0.92, 96.4, 2.9),
    ('multiport_droop', 3.1, 1.35, 95.1, 3.8),
    ('llc_mpc', 1.9, 0.80, 97.2, 2.4),
    ('ai_quadratic_nn', 2.1, 0.88, 96.0, 2.7),
]

W, H = 1200, 1500
MARGIN_X = 70
PLOT_W = 1020
PLOT_H = 220
GAP = 45
VREF = 400.0


def t_ms(i, n=1200):
    return 50.0 * i / (n - 1)


def load_pu(t):
    if t < 20:
        return 0.5
    if t < 35:
        return 1.0
    return 0.6


def polyline(points, color='#0b5', width=2):
    p = ' '.join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{width}" points="{p}" />'


def map_points(values, ymin, ymax, y0):
    pts = []
    n = len(values)
    for i, v in enumerate(values):
        x = MARGIN_X + PLOT_W * i / (n - 1)
        yy = y0 + PLOT_H - (v - ymin) * PLOT_H / (ymax - ymin + 1e-9)
        pts.append((x, yy))
    return pts


def rect_axes(y0, title):
    return (
        f'<rect x="{MARGIN_X}" y="{y0}" width="{PLOT_W}" height="{PLOT_H}" fill="white" stroke="#888" />'
        f'<text x="{MARGIN_X}" y="{y0-10}" font-size="20" font-family="Arial">{title}</text>'
    )

for name, tau_ms, ripple_pct, eff_peak, thd in profiles:
    n = 1200
    ts = [t_ms(i, n) for i in range(n)]

    vout = []
    iin = []
    iout = []
    ripple = []

    for t in ts:
        tau = tau_ms
        base = VREF * (1 - math.exp(-t / tau))
        if t >= 20:
            base -= 12 * math.exp(-(t - 20) / (tau * 0.9))
        if t >= 35:
            base += 6 * math.exp(-(t - 35) / (tau * 0.8))
        rip = VREF * (ripple_pct / 100.0) * (
            0.6 * math.sin(2 * math.pi * 2.0 * t) +
            0.4 * math.sin(2 * math.pi * 4.0 * t + 0.7)
        )
        vo = base + rip
        ld = load_pu(t)
        p = 1500 * ld
        vin = 36 + 4 * math.sin(2 * math.pi * 0.008 * t)
        eff = (eff_peak / 100.0) - 0.008 * (ld - 0.7) ** 2
        io = p / max(vo, 50)
        ii = p / max(vin * eff, 10)
        vout.append(vo)
        iout.append(io)
        iin.append(ii)
        ripple.append(rip)

    # Efficiency-vs-load points
    loads = [20 + i * 10 for i in range(9)]
    eff_curve = [eff_peak - 28 * ((l/100.0) - 0.82) ** 2 for l in loads]

    y0s = [60 + i * (PLOT_H + GAP) for i in range(5)]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
           '<rect width="100%" height="100%" fill="#f8fafc"/>',
           f'<text x="70" y="35" font-size="26" font-family="Arial" font-weight="bold">{name} - Simulation Graphs</text>']

    # Plot 1
    y0 = y0s[0]
    svg.append(rect_axes(y0, 'Output Voltage vs Time'))
    svg.append(polyline(map_points(vout, 360, 430, y0), '#2563eb', 1.8))

    # Plot 2
    y0 = y0s[1]
    svg.append(rect_axes(y0, 'Input/Output Current'))
    svg.append(polyline(map_points(iin, 5, 55, y0), '#dc2626', 1.6))
    svg.append(polyline(map_points(iout, 0, 6, y0), '#059669', 1.6))

    # Plot 3
    y0 = y0s[2]
    svg.append(rect_axes(y0, 'Efficiency vs Load'))
    pts = []
    for i, ev in enumerate(eff_curve):
        x = MARGIN_X + PLOT_W * i / (len(eff_curve) - 1)
        y = y0 + PLOT_H - (ev - 90) * PLOT_H / 8
        pts.append((x, y))
    svg.append(polyline(pts, '#7c3aed', 2))

    # Plot 4
    y0 = y0s[3]
    svg.append(rect_axes(y0, f'Voltage Ripple (THD proxy={thd:.1f}%)'))
    svg.append(polyline(map_points(ripple, -8, 8, y0), '#ea580c', 1.2))

    # Plot 5
    y0 = y0s[4]
    svg.append(rect_axes(y0, 'Transient Response under Load Change'))
    t_idx = [i for i, t in enumerate(ts) if 16 <= t <= 40]
    v_zoom = [vout[i] for i in t_idx]
    svg.append(polyline(map_points(v_zoom, 375, 410, y0), '#0f766e', 1.8))

    svg.append('</svg>')
    (OUT / f'{name}.svg').write_text('\n'.join(svg), encoding='utf-8')

print(f'Generated {len(profiles)} SVG figure sheets in {OUT.resolve()}')
