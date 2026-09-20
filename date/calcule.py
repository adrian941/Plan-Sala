# -*- coding: utf-8 -*-
"""Calculele pe planul citit din plan.db: macro-uri, cantități scrise frumos, totaluri pe zi.

Nimic de aici nu citește direct baza — primește `plan` de la `db.incarca()`.
Toate valorile nutriționale vin din coloanele ingredientului (per 100 g).
"""

# ordinea în care umblă peste tot cele cinci valori
VALORI = ("kcal", "proteine", "grăsimi", "carbohidrați", "fibre")


def macro(plan, items):
    """items = [(cheie, grame), …] → [kcal, P, G, C, fibre]."""
    t = [0.0] * 5
    for cheie, g in items:
        v = plan.ingrediente[cheie].valori
        for i in range(5):
            t[i] += v[i] * g / 100
    return t


def macro_reteta(plan, reteta, portie):
    return macro(plan, reteta.ingrediente(portie))


def r5(x):
    """Caloriile se rotunjesc la 5 — sub atât e oricum zgomot."""
    return int(round(x / 5.0) * 5)


def r0(x):
    """Întreg, rotunjit exact ca în fișierele .md (`{x:.0f}`)."""
    return int(f"{x:.0f}")


def r1(x):
    """O zecimală, ca macro-urile din meniu."""
    return float(f"{x:.1f}")


def numar(x):
    """Pentru JSON: 120.0 → 120, 22.5 rămâne 22.5 (baza ține totul ca REAL)."""
    return int(x) if float(x).is_integer() else x


def macro_rot(m):
    """Macro rotunjit exact cum se scrie pe pagină: kcal la 5, restul la întreg.
    Totalul zilei se adună mereu din ACESTE valori (per masă), nu din suma brută
    rotunjită separat — altfel «Total zi» nu iese egal cu suma meselor de pe pagină."""
    return [r5(m[0])] + [r0(x) for x in m[1:]]


def _bucati(ing, g):
    """Câte bucăți întregi (sau jumătăți) ies din gramaj; None dacă nu iese rotund."""
    if not ing.gram_bucata:
        return None
    n = g / ing.gram_bucata
    if round(n * 2, 6) % 1 != 0:      # nici întreg, nici jumătate → rămânem la grame
        return None
    return f"{n:g}".replace(".5", "½"), n


def qty(ing, g):
    """Cantitatea cu numele alimentului: «3 ouă», «50 g spanac», «100 ml lapte 1,5%»."""
    n_s, unitate, nume = parte_qty(ing, g)
    return f"{n_s} {nume}" if not unitate else f"{n_s} {unitate} {nume}"


def parte_qty(ing, g):
    """Aceeași cantitate, spartă în cele trei bucăți pe care site-ul le pune în coloane:
    («3», «», «ouă») · («50», «g», «spanac») · («100», «ml», «lapte 1,5%»)."""
    b = _bucati(ing, g)
    if b:
        n_s, n = b
        return n_s, "", (ing.bucata_sg if n == 1 else ing.bucata_pl)
    return f"{g:g}", ing.unitate, ing.scurt


def cant(ing, g):
    """Doar cantitatea, fără numele alimentului (numele stă în coloana lui)."""
    if g <= 0:
        return ""
    b = _bucati(ing, g)
    if b:
        return b[0] + " buc."
    return f"{g:g} {ing.unitate}"


def nume_ing(ing):
    """Cum se scrie alimentul într-un tabel de rețetă."""
    return ing.nume_scurt.capitalize() if ing.nume_scurt else ing.nume.split(",")[0]


def totals(plan, portie):
    """Totalul fiecărei zile din calendar, în ordine: [[kcal, P, G, C, fibre], …]."""
    out = []
    for zi in plan.zile:
        s = [0.0] * 5
        for rid in zi.retete:
            t = macro_reteta(plan, plan.retete[rid], portie)
            for i in range(5):
                s[i] += t[i]
        out.append(s)
    return out


def medie(T):
    return [sum(x[i] for x in T) / len(T) for i in range(5)]


def plants(plan, saptamana):
    """Plantele diferite dintr-o săptămână (țintă American Gut Project: ≥30)."""
    ks = set()
    for zi in plan.zile:
        if zi.saptamana != saptamana:
            continue
        for rid in zi.retete:
            for cheie, _g in plan.retete[rid].ingrediente("S"):
                if plan.ingrediente[cheie].e_planta:
                    ks.add(cheie)
    return ks


def saptamani(plan):
    """[1, 2] — câte săptămâni are calendarul."""
    return sorted({z.saptamana for z in plan.zile})


def zile_din(plan, saptamana):
    return [z for z in plan.zile if z.saptamana == saptamana]


# ---------------------------------------------------------------------------
#  Micronutrienții (minerale, vitamine) — aceeași socoteală ca la macro-uri,
#  doar că valorile vin din `ingredient.micro` (importate din USDA), nu din
#  cele cinci de pe farfurie. Trei alimente n-au corespondent în USDA
#  (lapte 1,5%, lapte de cocos light, mix de fructe de pădure), deci fiecare
#  total spune și câte ingrediente au lipsit din socoteală.
# ---------------------------------------------------------------------------

def micro(plan, items, ids):
    """items = [(cheie, grame), …] → ({nutrient_id: total}, câte ingrediente n-au date)."""
    t = {i: 0.0 for i in ids}
    fara = 0
    for cheie, g in items:
        ing = plan.ingrediente[cheie]
        if not ing.micro:
            fara += 1
            continue
        for i in ids:
            t[i] += ing.micro.get(i, 0.0) * g / 100
    return t, fara


def micro_reteta(plan, reteta, portie, ids):
    return micro(plan, reteta.ingrediente(portie), ids)


def micro_suma(plan, reteta, ids):
    """Cât iese din oală pentru amândoi: cantitățile S (Ema) + M (Adi), la un loc."""
    items = reteta.ingrediente("S") + reteta.ingrediente("M")
    return micro(plan, items, ids)


def macro_suma(plan, reteta):
    """Macro-urile pe cantitățile adunate: porția S + porția M."""
    return macro(plan, reteta.ingrediente("S") + reteta.ingrediente("M"))


def mic(x):
    """Cum se scrie o valoare de micronutrient: zecimală doar unde chiar contează."""
    if x >= 100:
        return f"{x:.0f}"
    if x >= 10:
        return f"{x:.1f}".replace(".0", "")
    return f"{x:.2f}".rstrip("0").rstrip(".") or "0"
