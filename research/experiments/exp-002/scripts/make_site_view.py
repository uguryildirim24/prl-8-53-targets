#!/usr/bin/env python3
"""Generate a simple XY site-frame schematic from deposited coordinates."""
from __future__ import annotations
import pathlib
import gemmi

ROOT = pathlib.Path(__file__).resolve().parents[1]
s = gemmi.read_structure(str(ROOT / "inputs/raw/3TDC-assembly2.cif.gz"))
lig = next(r for r in s[0]["A"] if r.name == "0EU")
lig_atoms = [a for a in lig if a.element.name != "H"]
contacts = []
for chain in [s[0]["A"], s[0]["A-2"]]:
    for res in chain:
        if res.het_flag != "A": continue
        ds = [((a.pos.x-l.pos.x)**2+(a.pos.y-l.pos.y)**2+(a.pos.z-l.pos.z)**2)**0.5 for a in res if a.element.name != "H" for l in lig_atoms]
        if ds and min(ds) <= 4.5:
            ca = next((a for a in res if a.name == "CA"), None)
            if ca: contacts.append(("A" if chain.name == "A" else "B", res.name+str(res.seqid.num), ca.pos.x, ca.pos.y))
points = [(a.pos.x,a.pos.y) for a in lig_atoms] + [(x,y) for _,_,x,y in contacts]
lo_x,hi_x=min(x for x,y in points)-2,max(x for x,y in points)+2
lo_y,hi_y=min(y for x,y in points)-2,max(y for x,y in points)+2
def xy(x,y): return (60+(x-lo_x)/(hi_x-lo_x)*680, 540-(y-lo_y)/(hi_y-lo_y)*460)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">',
'<rect width="800" height="600" fill="white"/>',
'<text x="40" y="30" font-family="sans-serif" font-size="18">3TDC 0EU pocket: deposited XY projection</text>',
'<text x="40" y="570" font-family="sans-serif" font-size="12">Schematic only; labels are residues within 4.5 Å in 3D. No density validation.</text>']
for a in lig_atoms:
    x,y=xy(a.pos.x,a.pos.y); svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#222"/>')
for ch,label,x0,y0 in contacts:
    x,y=xy(x0,y0); color='#2673b8' if ch=='A' else '#d55e00'
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}"/><text x="{x+7:.1f}" y="{y+4:.1f}" font-family="monospace" font-size="11">{ch}:{label}</text>')
svg += ['<circle cx="620" cy="30" r="5" fill="#2673b8"/><text x="630" y="34" font-family="sans-serif" font-size="12">chain A</text>',
'<circle cx="700" cy="30" r="5" fill="#d55e00"/><text x="710" y="34" font-family="sans-serif" font-size="12">symmetry mate B</text>', '</svg>']
(ROOT / "derived/site_view.svg").write_text('\n'.join(svg)+'\n')
