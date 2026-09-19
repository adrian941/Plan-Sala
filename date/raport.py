# -*- coding: utf-8 -*-
"""Verificarea planului, fără să scrie nimic: ies zilele la țintă?

    python raport.py

Se rulează după o modificare în plan.db și înainte de `python genereaza.py`:
arată ce iese pe fiecare rețetă (S și M), totalurile fiecărei zile față de țintă
și câte plante diferite are fiecare săptămână.
"""
import io, sys

import db
from calcule import macro_reteta, r5, totals, medie, plants, saptamani

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
plan = db.incarca()

probleme = db.verifica()
if probleme:
    print("\n".join("⚠️  " + p for p in probleme) + "\n")

for rid, r in plan.retete.items():
    s, m = macro_reteta(plan, r, "S"), macro_reteta(plan, r, "M")
    print(f"{rid:4s} {r.scurt:34s} S {r5(s[0]):4d} P{s[1]:3.0f} G{s[2]:3.0f} C{s[3]:3.0f} F{s[4]:3.0f}"
          f"  M {r5(m[0]):4d} P{m[1]:3.0f} G{m[2]:3.0f} C{m[3]:3.0f} F{m[4]:3.0f}")

for p in plan.persoane:
    print(f"{p.nume} (porția {p.portie})")
    T = totals(plan, p.portie)
    avg = medie(T)
    for zi, t in zip(plan.zile, T):
        print(f"  {zi.nume:9s} {t[0]:5.0f} P{t[1]:4.0f} G{t[2]:3.0f} C{t[3]:4.0f} F{t[4]:3.0f}")
    print(f"  MEDIE     {avg[0]:5.0f} P{avg[1]:4.0f} G{avg[2]:3.0f} C{avg[3]:4.0f} F{avg[4]:3.0f}"
          f"   tinta {p.tinta}")

for w in saptamani(plan):
    pl = plants(plan, w)
    print(f"Plante săpt. {w}: {len(pl)}", sorted(pl))
