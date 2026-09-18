#!/usr/bin/env python3
"""Iconița aplicației — sursa de adevăr. Rulează:  python _site/icons/genereaza_icon.py

Desenul: o farfurie albă pe fundal verde (culoarea --acc a site-ului), cu o halteră
și un fir verde care crește din ea — sală + nutriție într-un singur semn.
Din SVG se scriu toate PNG-urile din manifest. Nu edita PNG-urile de mână.

Nevoie de: pip install cairosvg
"""
import pathlib
import cairosvg

AICI = pathlib.Path(__file__).parent

VERDE_INCHIS = "#0C6257"   # haltera + nervura frunzei
FRUNZA_1 = "#2FB877"
FRUNZA_2 = "#45D08C"

DEFS = """
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#22CBA6"/>
      <stop offset=".52" stop-color="#0E8A7A"/>
      <stop offset="1" stop-color="#075F55"/>
    </linearGradient>
    <radialGradient id="glow" cx=".28" cy=".2" r=".85">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".30"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="plate" x1=".2" y1="0" x2=".8" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#E9F4F1"/>
    </linearGradient>
  </defs>"""


def _frunza(cx, cy, unghi, lung, lat, umplere):
    d = (f"M 0 0 C {-lat} {-lung*0.3:.0f}, {-lat*0.88:.0f} {-lung*0.74:.0f}, 0 {-lung} "
         f"C {lat*0.88:.0f} {-lung*0.74:.0f}, {lat} {-lung*0.3:.0f}, 0 0 Z")
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({unghi})">'
            f'<path d="{d}" fill="{umplere}"/>'
            f'<path d="M 0 {-lung*0.08:.0f} L 0 {-lung*0.82:.0f}" stroke="{VERDE_INCHIS}" '
            f'stroke-width="{max(3, lung*0.055):.0f}" stroke-linecap="round" fill="none" opacity=".55"/>'
            f'</g>')


def _emblema(scala=1.0, cx=256, cy=256):
    """Farfuria cu haltera și firul verde. scala=1 → farfurie cu raza 168."""
    g = []
    r = 168 * scala
    g.append(f'<ellipse cx="{cx}" cy="{cy + 10*scala:.1f}" rx="{r:.1f}" ry="{r:.1f}" fill="#04443C" opacity=".28"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="url(#plate)"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.845:.1f}" fill="none" stroke="#0E8A7A" '
             f'stroke-opacity=".16" stroke-width="{6*scala:.1f}"/>')

    # haltera, ușor înclinată
    by = cy + 56 * scala

    def bara(x, y, w, h, rd):
        return (f'<rect x="{x - w/2:.1f}" y="{y - h/2:.1f}" width="{w:.1f}" height="{h:.1f}" '
                f'rx="{rd:.1f}" fill="{VERDE_INCHIS}"/>')

    g.append(f'<g transform="rotate(-12 {cx} {by:.1f})">')
    g.append(bara(cx, by, 176*scala, 30*scala, 15*scala))
    for dx, w, h in ((-66, 36, 104), (66, 36, 104), (-104, 26, 68), (104, 26, 68)):
        g.append(bara(cx + dx*scala, by, w*scala, h*scala, min(w, h)*0.42*scala))
    g.append("</g>")

    # firul verde care crește din bară
    ly = cy - 32 * scala
    g.append(f'<path d="M {cx} {ly:.1f} q {-6*scala:.1f} {28*scala:.1f} {4*scala:.1f} {52*scala:.1f}" '
             f'stroke="{VERDE_INCHIS}" stroke-width="{10*scala:.1f}" stroke-linecap="round" fill="none"/>')
    g.append(_frunza(cx - 5*scala, ly, -36, 70*scala, 31*scala, FRUNZA_1))
    g.append(_frunza(cx + 5*scala, ly,  36, 86*scala, 35*scala, FRUNZA_2))
    return "\n  ".join(g)


def svg(fel):
    """fel: 'any' (colțuri rotunde, pentru browser) | 'maskable' | 'apple'."""
    if fel == "any":
        fundal = ('<rect width="512" height="512" rx="112" fill="url(#bg)"/>'
                  '<rect width="512" height="512" rx="112" fill="url(#glow)"/>')
        scala = 1.0
    else:
        # fundal plin: masca o dă sistemul. „maskable" cere emblema în cercul de 60% din centru.
        fundal = ('<rect width="512" height="512" fill="url(#bg)"/>'
                  '<rect width="512" height="512" fill="url(#glow)"/>')
        scala = 0.76 if fel == "maskable" else 0.92
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
            f'{DEFS}\n  {fundal}\n  {_emblema(scala)}\n</svg>\n')


# ce se scrie: (nume fișier, fel, latură)
FISIERE = (
    [(f"icon-{n}.png", "any", n) for n in (72, 96, 128, 144, 152, 192, 384, 512)]
    + [("icon-maskable-192.png", "maskable", 192), ("icon-maskable-512.png", "maskable", 512)]
    + [("apple-touch-icon.png", "apple", 180), ("favicon-32.png", "any", 32), ("favicon-16.png", "any", 16)]
)


def main():
    (AICI / "icon.svg").write_text(svg("any"), encoding="utf-8")
    (AICI / "icon-maskable.svg").write_text(svg("maskable"), encoding="utf-8")
    for nume, fel, latura in FISIERE:
        cairosvg.svg2png(bytestring=svg(fel).encode("utf-8"), write_to=str(AICI / nume),
                         output_width=latura, output_height=latura)
        print("scris", nume)


if __name__ == "__main__":
    main()
