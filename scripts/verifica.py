#!/usr/bin/env python3
"""Verifică regulile de arhitectură din CLAUDE.md §2.1.

Rulează: python3 scripts/verifica.py
Ieșire 0 = totul ok; 1 = s-au găsit probleme.
"""
import os, re, sys

RADACINA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FISIERE_PERSOANA = ["1_profil.md", "2_nutritie.md", "3_preferinte.md", "4_meniu.md"]
# Singura vedere derivată care are voie să conțină nume de persoane (regula 4).
EXCEPTII_NEUTRALITATE = {"comun/2_retete.md"}

probleme = []


def fisiere_md():
    for dosar, subdosare, fisiere in os.walk(RADACINA):
        subdosare[:] = [d for d in subdosare if d != ".git"]
        for f in fisiere:
            if f.endswith(".md"):
                yield os.path.join(dosar, f)


def rel(cale):
    return os.path.relpath(cale, RADACINA).replace(os.sep, "/")


def persoane():
    dosar = os.path.join(RADACINA, "persoane")
    if not os.path.isdir(dosar):
        return []
    return sorted(d for d in os.listdir(dosar)
                  if os.path.isdir(os.path.join(dosar, d)) and not d.startswith("_"))


def verifica_linkuri():
    for cale in fisiere_md():
        text = open(cale, encoding="utf-8").read()
        for m in re.finditer(r"\]\((\.{1,2}/[^)#]*)(#[^)]*)?\)", text):
            tinta = os.path.normpath(os.path.join(os.path.dirname(cale), m.group(1)))
            if not os.path.exists(tinta):
                probleme.append(f"link rupt: {rel(cale)} -> {m.group(1)}")


# Sufixe de declinare românească (Ema -> Emei, Adi -> lui Adi, Ioana -> Ioanei).
SUFIXE = ["", "i", "a", "ei", "ii", "ele", "lui", "ului"]


def forme(nume):
    """Toate formele sub care poate aparea un nume: Ema -> Ema, Emei, Emii..."""
    f = {nume + s for s in SUFIXE}
    if nume[-1].lower() in "aeiou":          # genitivul taie vocala finala: Ema -> Em+ei
        f |= {nume[:-1] + s for s in SUFIXE if s}
    return f


def verifica_neutralitate(nume_persoane):
    """Regula 1: niciun fișier din comun/ nu conține nume de persoane."""
    if not nume_persoane:
        return
    toate = sorted({f for n in nume_persoane for f in forme(n)}, key=len, reverse=True)
    tipar = re.compile(r"\b(" + "|".join(re.escape(f) for f in toate) + r")\b", re.I)
    for cale in fisiere_md():
        r = rel(cale)
        if not r.startswith("comun/") or r in EXCEPTII_NEUTRALITATE:
            continue
        for nr, linie in enumerate(open(cale, encoding="utf-8"), 1):
            if tipar.search(linie):
                probleme.append(f"nume de persoana in comun/: {r}:{nr}")


def verifica_structura_persoane(nume_persoane):
    """Regula 3: fiecare persoană are aceeași structură ca șablonul."""
    sablon = os.path.join(RADACINA, "persoane", "_sablon")
    if not os.path.isdir(sablon):
        probleme.append("lipseste persoane/_sablon/ (template-ul de persoana)")
    else:
        for f in FISIERE_PERSOANA:
            if not os.path.exists(os.path.join(sablon, f)):
                probleme.append(f"sablonul nu are {f}")
    for p in nume_persoane:
        for f in FISIERE_PERSOANA:
            if not os.path.exists(os.path.join(RADACINA, "persoane", p, f)):
                probleme.append(f"persoana '{p}' nu are {f}")


def main():
    p = persoane()
    verifica_linkuri()
    verifica_neutralitate(p)
    verifica_structura_persoane(p)
    print(f"Persoane configurate: {', '.join(p) if p else '(niciuna)'}")
    if probleme:
        print(f"\n{len(probleme)} probleme:")
        for x in probleme:
            print("  ✗", x)
        return 1
    print("✓ link-uri valide · comun/ neutru · structura persoanelor consistenta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
