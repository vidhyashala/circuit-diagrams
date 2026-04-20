from pathlib import Path

OUT = Path('figures/schematics')
OUT.mkdir(parents=True, exist_ok=True)


def svg_header(w=1600, h=900):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fcfcfd"/>',
        '<defs>',
        '  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '    <polygon points="0 0, 10 3.5, 0 7" fill="#0f172a"/>',
        '  </marker>',
        '</defs>'
    ]


def wire(x1, y1, x2, y2, arr=False):
    marker = ' marker-end="url(#arrow)"' if arr else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111827" stroke-width="3"{marker}/>'


def box(x, y, w, h, label, fill="#ffffff"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10" fill="{fill}" stroke="#1f2937" stroke-width="2.5"/>'
        f'<text x="{x+w/2}" y="{y+h/2+6}" font-family="Arial" font-size="22" text-anchor="middle" fill="#111827">{label}</text>'
    )


def title(txt):
    return f'<text x="40" y="48" font-family="Arial" font-size="34" font-weight="bold" fill="#0f172a">{txt}</text>'


def note(x, y, txt):
    return f'<text x="{x}" y="{y}" font-family="Arial" font-size="20" fill="#374151">{txt}</text>'

# 1 Hybrid DAB + Boost
s = svg_header()
s += [title('Hybrid Dual Active Bridge + Interleaved Boost (Professional Schematic)')]
s += [box(60, 180, 160, 70, 'Vin\n24-48V', '#eef2ff')]
s += [box(280, 120, 190, 80, 'Lb1 + S1', '#f8fafc'), box(280, 250, 190, 80, 'Lb2 + S2', '#f8fafc')]
s += [box(530, 185, 180, 80, 'Cboost', '#fff7ed')]
s += [box(760, 150, 220, 150, 'Primary H-Bridge\nQ1 Q2 Q3 Q4', '#f0fdf4')]
s += [box(1030, 160, 180, 130, 'HF Transformer\nNp:Ns', '#fef3c7')]
s += [box(1260, 150, 220, 150, 'Secondary H-Bridge\nQ5 Q6 Q7 Q8', '#f0fdf4')]
s += [box(1310, 350, 120, 70, 'Lf', '#f8fafc'), box(1470, 350, 110, 70, 'Co', '#fff7ed'), box(1440, 470, 140, 70, 'Vbus 400V', '#eef2ff')]
s += [wire(220,215,280,160,True), wire(220,215,280,290,True), wire(470,160,530,225), wire(470,290,530,225), wire(710,225,760,225,True), wire(980,225,1030,225,True), wire(1210,225,1260,225,True), wire(1370,300,1370,350), wire(1430,385,1470,385), wire(1525,420,1525,470,True)]
s += [note(70, 620, 'Switching: 2-phase interleaved PWM (S1/S2, 180°) + DAB phase-shift modulation.'), note(70, 655, 'Current flow: Vin -> Boost stage -> DAB primary -> HF transformer -> active rectification -> Lf/Co -> 400V bus.')]
s += ['</svg>']
(OUT/'hybrid_dab_boost_schematic.svg').write_text('\n'.join(s), encoding='utf-8')

# 2 Interleaved high-gain coupled inductors
s = svg_header()
s += [title('Interleaved High-Gain Converter with Coupled Inductors')]
s += [box(60, 220, 170, 80, 'Vin', '#eef2ff')]
s += [box(290, 90, 180, 80, 'Lc1 + Sa', '#f8fafc'), box(290, 220, 180, 80, 'Lc2 + Sb', '#f8fafc'), box(290, 350, 180, 80, 'Lc3 + Sc', '#f8fafc')]
s += [box(540, 90, 170, 80, 'Cm1 + D1', '#fff7ed'), box(540, 220, 170, 80, 'Cm2 + D2', '#fff7ed'), box(540, 350, 170, 80, 'Cm3 + D3', '#fff7ed')]
s += [box(780, 200, 250, 120, 'Diode-Capacitor\nMultiplier Network', '#fef3c7')]
s += [box(1080, 220, 130, 80, 'Co', '#fff7ed'), box(1270, 220, 180, 80, 'Vbus 400V', '#eef2ff')]
s += [wire(230,260,290,130,True), wire(230,260,290,260,True), wire(230,260,290,390,True), wire(470,130,540,130), wire(470,260,540,260), wire(470,390,540,390), wire(710,130,780,240), wire(710,260,780,260), wire(710,390,780,280), wire(1030,260,1080,260,True), wire(1210,260,1270,260,True)]
s += [note(70, 610, 'Switching: 3-phase interleaving, 120° phase shift, adaptive duty for current sharing.'), note(70, 645, 'Flow: distributed phase currents through coupled inductors, then gain stacking via multiplier to regulated DC bus.')]
s += ['</svg>']
(OUT/'interleaved_coupled_schematic.svg').write_text('\n'.join(s), encoding='utf-8')

# 3 Multi-port bidirectional
s = svg_header()
s += [title('Multi-Port Bidirectional Converter (PV + Battery + Load)')]
s += [box(60,120,180,80,'PV Port\n24-48V','#eef2ff'), box(60,320,180,80,'Battery Port\n36-60V','#eef2ff')]
s += [box(300,120,220,90,'PV Half-Bridge\nQpv1,Qpv2','#f0fdf4'), box(300,320,220,90,'Bi-dir Bridge\nQb1,Qb2','#f0fdf4')]
s += [box(610,200,250,160,'Three-Winding\nHF Transformer','#fef3c7')]
s += [box(940,200,230,120,'Bus Active Rectifier\nQr1..Qr4','#f0fdf4')]
s += [box(1240,210,100,70,'Lout','#f8fafc'), box(1380,210,100,70,'Co','#fff7ed'), box(1330,360,200,80,'400V Bus/Load','#eef2ff')]
s += [wire(240,160,300,165,True), wire(240,360,300,365,True), wire(520,165,610,245,True), wire(520,365,610,285,True), wire(860,260,940,260,True), wire(1170,260,1240,245), wire(1340,245,1380,245), wire(1430,280,1430,360,True)]
s += [note(70, 610, 'Switching: phase-shifted bridges with synchronous bidirectional operation.'), note(70, 645, 'Power flow: PV -> bus, battery <-> bus (charge/discharge), autonomous support via droop control.')]
s += ['</svg>']
(OUT/'multiport_bidirectional_schematic.svg').write_text('\n'.join(s), encoding='utf-8')

# 4 LLC resonant
s = svg_header()
s += [title('LLC Resonant Converter with Soft Switching (ZVS/ZCS)')]
s += [box(60,220,170,80,'Vin','#eef2ff')]
s += [box(290,220,220,100,'Half-Bridge\nQ1,Q2','#f0fdf4')]
s += [box(560,180,120,70,'Lr','#f8fafc'), box(710,180,120,70,'Cr','#fff7ed'), box(860,180,150,70,'Lm','#f8fafc')]
s += [box(860,290,160,100,'HF Tx','#fef3c7')]
s += [box(1080,220,230,100,'Sync Rectifier\nQ3,Q4','#f0fdf4')]
s += [box(1360,230,100,70,'Co','#fff7ed'), box(1280,380,220,80,'Vout 400V','#eef2ff')]
s += [wire(230,260,290,270,True), wire(510,270,560,215), wire(680,215,710,215), wire(830,215,860,215), wire(935,250,935,290), wire(1020,340,1080,270,True), wire(1310,270,1360,265), wire(1410,300,1410,380,True)]
s += [note(70, 610, 'Switching: variable-frequency control around resonant frequency to sustain ZVS/ZCS region.'), note(70, 645, 'Flow: resonant sinusoidal tank current -> transformer -> synchronous rectification -> low-ripple DC output.')]
s += ['</svg>']
(OUT/'llc_resonant_schematic.svg').write_text('\n'.join(s), encoding='utf-8')

# 5 AI controlled
s = svg_header()
s += [title('AI-Controlled Reduced-Switch Quadratic Boost Converter')]
s += [box(60,240,170,80,'Vin','#eef2ff')]
s += [box(290,180,140,70,'L1','#f8fafc'), box(290,300,140,70,'S1','#f0fdf4')]
s += [box(490,240,150,80,'Cx','#fff7ed')]
s += [box(700,180,140,70,'L2','#f8fafc'), box(700,300,140,70,'S2','#f0fdf4')]
s += [box(900,240,120,80,'D1','#f8fafc')]
s += [box(1080,240,110,80,'Co','#fff7ed'), box(1250,240,180,80,'400V Bus','#eef2ff')]
s += [box(520,460,300,120,'NN + Safety Supervisor','#ede9fe')]
s += [wire(230,280,290,215,True), wire(230,280,290,335,True), wire(430,215,490,280), wire(430,335,490,280), wire(640,280,700,215), wire(640,280,700,335), wire(840,280,900,280,True), wire(1020,280,1080,280,True), wire(1190,280,1250,280,True), wire(670,460,360,370,True), wire(670,460,770,370,True)]
s += [note(70, 640, 'Switching: fixed-frequency PWM with dual-duty coordination and interlock constraints.'), note(70, 675, 'Control innovation: neural adaptive duty estimator with bounded fallback for safe operation under uncertainty.')]
s += ['</svg>']
(OUT/'ai_quadratic_schematic.svg').write_text('\n'.join(s), encoding='utf-8')

print(f'Generated 5 professional schematics in {OUT.resolve()}')
