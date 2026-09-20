# -*- coding: utf-8 -*-
"""Scrie fișierele planului din plan.db. Sursa e baza; astea sunt doar ieșiri.

    python genereaza.py

Regenerează, dintr-o singură rulare:
    comun/1_ingrediente.md   comun/2_retete.md   comun/4_calendar.md
    ema/4_meniu.md + ema/4b_meniu_zilnic.md     adi/4_meniu.md + adi/4b_meniu_zilnic.md
    _site/data.js            (meniurile, rețetele și alimentele pentru site)
    date/plan.sql            (dump-ul text al bazei, pentru git)

Textul explicativ (regulile, cum e gândit calendarul, organizarea bucătăriei) stă aici,
în șabloane. Datele — alimente, rețete, cantități, calendar, ținte — stau exclusiv în plan.db.
"""
import io, json, os, sys

import db
from calcule import (macro_reteta, macro_suma, micro_suma, micro_zi, procent_dzr, mic, r5, r0, r1,
                     numar, qty, cant, parte_qty, nume_ing, totals, medie, plants, saptamani,
                     zile_din)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + "/"


def W(path, text):
    io.open(ROOT + path, "w", encoding="utf-8", newline="\n").write(text)


def m5(t):
    return f"{r5(t[0])} | {t[1]:.0f} | {t[2]:.0f} | {t[3]:.0f} | {t[4]:.0f}"


# ---------------------------------------------------------------------------
#  Micronutrienții care se afișează, în ordinea în care apar. Restul rămân în bază.
#  `VITAMINE` = linia scurtă de sub fiecare rețetă din caietul de print;
#  `VITAMINE_ZI` = rândul de pe banda zilei, la paginile Detaliat — toate vitaminele,
#      fiecare cu cât s-a strâns în ziua aia și cu cât la sută din DZR înseamnă (dzr
#      stă în bază, la nutrient). Etichetele sunt scurte: intră 13 într-un card îngust;
#  `MICRO` = tot ce se deschide din butonul „Vitamine & minerale" de la Alimente.
# ---------------------------------------------------------------------------
VITAMINE = [(1106, "A"), (1162, "C"), (1114, "D"), (1109, "E"),
            (1185, "K"), (1175, "B6"), (1177, "Folat"), (1178, "B12")]
VITAMINE_ZI = [(1106, "A"), (1162, "C"), (1114, "D"), (1109, "E"), (1185, "K"),
               (1165, "B1"), (1166, "B2"), (1167, "B3"), (1170, "B5"), (1175, "B6"),
               (1177, "Folat"), (1178, "B12"), (1180, "Colină")]
MICRO = [(1106, "Vitamina A"), (1162, "Vitamina C"), (1114, "Vitamina D"), (1109, "Vitamina E"),
         (1185, "Vitamina K"), (1165, "B1 tiamină"), (1166, "B2 riboflavină"), (1167, "B3 niacină"),
         (1170, "B5 pantotenic"), (1175, "Vitamina B6"), (1177, "Folat"), (1178, "Vitamina B12"),
         (1180, "Colină"),
         (1087, "Calciu"), (1089, "Fier"), (1090, "Magneziu"), (1091, "Fosfor"), (1092, "Potasiu"),
         (1093, "Sodiu"), (1095, "Zinc"), (1098, "Cupru"), (1101, "Mangan"), (1103, "Seleniu")]
UNITATI = {"MG": "mg", "UG": "µg", "IU": "UI", "G": "g", "KCAL": "kcal"}


plan = db.incarca()


def unit(nid):
    """Unitatea nutrientului, scrisă cum o citesc oamenii: MG → mg, UG → µg."""
    return UNITATI.get(plan.nutrienti[nid].unitate, plan.nutrienti[nid].unitate)


ING = list(plan.ingrediente.values())
R = plan.retete
SAPT = saptamani(plan)

# ================= 1. INGREDIENTE =================
o = []
o.append("# 🥦 Lista de alimente — sursa unică de adevăr pentru valori nutriționale\n")
o.append("> **Pasul 1** din [cum lucrăm](./0_pipeline.md). **Toate calculele din rețete și meniuri pleacă din tabelul de mai jos** — nicio valoare nu se ia din altă parte.\n>\n> Aici nu scriem cui îi place ce. Gusturile fiecăruia stau la el: [`ema/3_preferinte.md`](../ema/3_preferinte.md), [`adi/3_preferinte.md`](../adi/3_preferinte.md).\n")
o.append("## Regula\n")
o.append("1. **Sursa:** [USDA FoodData Central](https://fdc.nal.usda.gov/) — baza de date oficială a Departamentului Agriculturii SUA (setul *SR Legacy*), referința standard folosită de aplicațiile de nutriție. Fiecare rând are ID-ul alimentului (căutabil pe site). Unde USDA nu are produsul (ex. lapte 1,5%, lapte de cocos light), se ia **eticheta producătorului** și se notează.\n")
o.append("2. **Valorile sunt per 100 g de aliment crud / uscat** (carnea, peștele, orezul, pastele, lintea se cântăresc înainte de gătit). Excepții marcate: conservele (scurse), pâinea.\n")
o.append("3. **Ingredient nou = rând nou aici, înainte să intre într-o rețetă.** Când apare o rețetă cu un ingredient care nu e în tabel, se caută în USDA și se adaugă.\n")
o.append("4. Produsele românești de lactate (brânză de vaci, telemea, skyr) variază între producători — valoarea USDA e referința, dar dacă eticheta ta diferă mult, o folosim pe aceea.\n")
o.append("\n**Rolul pe farfurie** (regula 40/40/20): `P` = proteină (40%) · `L` = legume / carbohidrați fibroși (40%) · `A` = amidon (20%) · `G` = grăsime (nu ocupă felie) · `F` = fruct\n")
o.append("\n---\n")
for cat in plan.categorii:
    o.append(f"\n## {cat.icon} {cat.nume}\n")
    o.append("| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |\n|---|:-:|--:|--:|--:|--:|--:|---|---|")
    for i in cat.ingrediente:
        srcs = f"[{i.sursa}](https://fdc.nal.usda.gov/food-details/{i.fdc_id}/nutrients)" if i.fdc_id else i.sursa
        o.append(f"| {i.nume} | {cat.rol} | {i.kcal:g} | {i.proteine:g} | {i.grasimi:g} | {i.carbo:g} | {i.fibre:g} | {srcs} | {i.nota} |")
    o.append("")
o.append("\n---\n\n## Porții uzuale (pentru cântărit din ochi)\n")
o.append("| Aliment | Porție | ≈ g |\n|---|---|--:|\n| Ou M | 1 buc. | 55 |\n| Banană | 1 buc. medie | 120 |\n| Măr | 1 buc. medie | 180 |\n| Pâine integrală | 1 felie | 40–50 |\n| Ulei de măsline | 1 lingură | 10 |\n| Unt de arahide | 1 lingură | 15 |\n| Semințe chia / in | 1 lingură | 10 |\n| Nuci / migdale | 1 mână mică | 15–20 |\n| Usturoi | 1 cățel | 3 |\n| Orez / quinoa / hrișcă crud | 1 porție 20% | 55–65 |\n| Carne / pește crud | 1 porție 40% | 150–220 |\n")
o.append("\n## 🌾 De unde vin fibrele — pe scurt\n\nLeguminoase (linte, năut: 10–12 g/100 g uscat), semințe (chia 34, in 27), ovăz (10), paste integrale (9), fructe de pădure (zmeură 6,5), avocado (6,7), legume (2–4 g/100 g). Practic: leguminoase + o lingură de semințe + fructe de pădure + legume la fiecare masă → 30–40 g/zi fără efort.\n")
W("comun/1_ingrediente.md", "\n".join(o))

# ================= 2. REȚETE =================
GRUPE = [("Mic dejun", "## 🌅 Mic dejun"), ("Gustări", "## 🍎 Gustări"),
         ("Feluri principale", "## 🍲 Feluri principale — farfuria 40/40/20")]


def comp_table(r):
    lines = ["| Element | Ingredient | S | M |", "|---|---|--:|--:|"]
    for label, items in r.comp:
        for i, (k, gs, gm) in enumerate(items):
            ing = plan.ingrediente[k]
            lab = f"**{label.strip()}**" if i == 0 else ""
            cs = qty(ing, gs).replace(ing.scurt, "").strip() if gs > 0 else "—"
            cm = qty(ing, gm).replace(ing.scurt, "").strip() if gm > 0 else "—"
            lines.append(f"| {lab} | {nume_ing(ing)} | {cs} | {cm} |")
    return "\n".join(lines)


o = []
o.append("# 🍽️ Rețete\n")
o.append("> **Pasul 2** din [cum lucrăm](./0_pipeline.md). Toate valorile de mai jos sunt calculate din [`1_ingrediente.md`](./1_ingrediente.md) (USDA), pe cantități **crude**.\n> De aici pleacă [`3_cumparaturi.md`](./3_cumparaturi.md). Ce rețetă în ce zi: [`4_calendar.md`](./4_calendar.md).\n")
o.append("## Cum adăugăm o rețetă\n\nÎmi dai rețeta cu ce detalii ai (ingrediente, cum se face, timp, câte porții ies, **cui îi place și cui nu**). Eu: (1) adaug ingredientele noi în `1_ingrediente.md` din USDA, (2) o scriu aici pe structura farfuriei, cu **modul de preparare pas cu pas**, (3) calculez S și M, (4) trec verdictele în preferințele fiecăruia.\n\n**Semne:** ⭐ favorit · ✅ îi place · 🟡 neutru · ❌ nu-i place · ⛔ nu poate · ❔ netestat\n")
o.append("## Farfuria 40/40/20 — cum e construit fiecare fel principal\n\nFiecare fel principal are **trei elemente vizibile + un sos**:\n\n| Element | Cât din farfurie | Ce e |\n|---|:-:|---|\n| **Proteină** | 40% | carne, pește, ouă, lactate |\n| **Legume** | 40% | carbohidrați fibroși: legume la tavă, piureuri de legume, salate, legume sotate — **cel puțin 3 legume diferite** pe farfurie |\n| **Amidon** | 20% | orez, cartof, quinoa, hrișcă, paste, mămăligă, leguminoase |\n| **Sos** | — | pe bază de iaurt (usturoi, mărar, lămâie, muștar), roșii pasate cu busuioc, soia-ghimbir — gust fără calorii goale |\n\n**Regula casei: nu amestecăm lactatele cu carnea/peștele, nici ouăle cu carnea, în aceeași masă.** De aceea sosurile la felurile cu carne sunt fără iaurt (tahini-lămâie, lămâie-usturoi-ulei, vinegretă de muștar, roșii-busuioc, soia-ghimbir), piureurile se fac cu ulei de măsline, iar lactatele stau la micul dejun și la gustări.\n\nProcentele sunt **pe volum**, nu la gram. Diversitatea contează la fel de mult ca proporțiile (American Gut Project: **≥30 de plante diferite pe săptămână** — planul are ~40).\n")
o.append("## Două mărimi de porție\n\n**S (standard)** și **M (mare)**: diferă proteina și amidonul; legumele, sosul și condimentele sunt identice → o singură oală/tavă. Cine mănâncă ce mărime: `ema/4_meniu.md`, `adi/4_meniu.md`. Felurile principale se gătesc **×4 = 2 S + 2 M** (cina de azi + prânzul de mâine).\n")
o.append("---\n\n## Cuprins\n")
o.append("| # | Rețetă | Masă | Timp | kcal S / M | S: P / G / C / Fibre | M: P / G / C / Fibre | Ema | Adi | Frigider |\n|--:|--------|------|-----:|-----------:|---|---|:-:|:-:|:-:|")
for rid, r in R.items():
    s, m = macro_reteta(plan, r, "S"), macro_reteta(plan, r, "M")
    o.append(f"| {rid} | [{r.nume}](#{rid.lower()}) | {r.masa} | {r.timp} | {r5(s[0])} / {r5(m[0])} | {s[1]:.0f} / {s[2]:.0f} / {s[3]:.0f} / {s[4]:.0f} | {m[1]:.0f} / {m[2]:.0f} / {m[3]:.0f} / {m[4]:.0f} | ❔ | ❔ | {r.tine} |")
o.append("\n🥚 = zi cu ouă · 🐟 = pește · 🏋️ = post-antrenament. Rotunjiri: kcal la 5, macro la 1 g.\n\n---\n")
for grup, titlu in GRUPE:
    o.append(f"\n{titlu}\n")
    if grup == "Feluri principale":
        o.append("Cantitățile sunt **pe o porție**. Pentru oala de 4: proteina și amidonul = 2×S + 2×M, restul ×4.\n")
    for rid, r in R.items():
        if r.grup != grup:
            continue
        s, m = macro_reteta(plan, r, "S"), macro_reteta(plan, r, "M")
        o.append(f'<a id="{rid.lower()}"></a>\n### {rid} · {r.nume}\n**{r.masa.capitalize()} · {r.timp} · ține: {r.tine}**\n')
        o.append(comp_table(r) + "\n")
        o.append(f"**Cum se face (pe scurt):** {r.cum}\n")
        if r.pasi:
            o.append("**Mod de preparare**\n")
            o.append("\n".join(f"{i}. {pas}" for i, pas in enumerate(r.pasi, 1)) + "\n")
        if r.sfat:
            o.append(f"**De ce așa:** {r.sfat}\n")
        o.append(f"| Pe porție | kcal | P | G | C | Fibre |\n|---|--:|--:|--:|--:|--:|\n| **S** | {m5(s)} |\n| **M** | {m5(m)} |\n")
        if r.varianta:
            o.append(f"**Variante:** {r.varianta}\n")
        o.append("")
o.append("\n---\n\n## De testat\nToate rețetele de mai sus sunt propuse, **nu încă gătite**. După fiecare, verdictul se scrie în preferințele fiecăruia și în coloanele din cuprins.\n\n## Scoase din rotație\n*(Ce n-a mers și de ce — ca să nu le repropun.)*\n")
W("comun/2_retete.md", "\n".join(o))


# ================= 3. MENIURI =================
def plate(r, portie):
    col = 1 if portie == "S" else 2
    parts = []
    for _label, items in r.comp:
        xs = [qty(plan.ingrediente[it[0]], it[col]) for it in items if it[col] > 0]
        if xs:
            parts.append(" + ".join(xs))
    return f"**{r.scurt}** — " + " · ".join(parts)


def menu(p):
    T = totals(plan, p.portie)
    avg = medie(T)
    tgt = p.tinta
    o = []
    o.append(f"# 🍳 Meniu pe 2 săptămâni — {p.nume}\n")
    o.append(f"> Rețetele sunt comune ([`comun/2_retete.md`](../comun/2_retete.md)), calendarul de gătit e comun ([`comun/4_calendar.md`](../comun/4_calendar.md)).\n> Aici: **exact ce și cât** mănâncă {p.pronume}, cu caloriile și macro-urile calculate din [`comun/1_ingrediente.md`](../comun/1_ingrediente.md) (USDA). Țintele: [`2_nutritie.md`](./2_nutritie.md). Ce-i place: [`3_preferinte.md`](./3_preferinte.md).\n")
    o.append(f"## Porția: **{p.portie}** ({p.portie_nume}) la toate rețetele\n\nȚinte: **{tgt[0]} kcal · P{tgt[1]} / G{tgt[2]} / C{tgt[3]}**. Cantitățile sunt **crude** (carnea, orezul, lintea înainte de gătit). Mesele principale = farfuria 40/40/20: *proteină · legume · amidon · sos*. **Fără lactate cu carne/pește și fără ouă cu carne în aceeași masă** — lactatele sunt la micul dejun și gustări.\n")
    for w in SAPT:
        o.append(f"\n## Săptămâna {w}\n")
        o.append("| Zi | Masa | Ce și cât | kcal | P | G | C | Fibre |\n|---|---|---|--:|--:|--:|--:|--:|")
        for zi in zile_din(plan, w):
            t = T[zi.id]
            eticheta = f"**{zi.nume}** {zi.semne}".strip()
            for tip, _icon, rid in zi.mese:
                mm = macro_reteta(plan, R[rid], p.portie)
                o.append(f"| {eticheta} | {tip} | {plate(R[rid], p.portie)} | {r5(mm[0])} | {mm[1]:.0f} | {mm[2]:.0f} | {mm[3]:.0f} | {mm[4]:.0f} |")
                eticheta = ""
            o.append(f"| | **Total zi** | | **{r5(t[0])}** | **{t[1]:.0f}** | **{t[2]:.0f}** | **{t[3]:.0f}** | **{t[4]:.0f}** |")
        pl = plants(plan, w)
        o.append(f"\n*Plante diferite în săptămâna {w}: **{len(pl)}** (țintă American Gut Project ≥30).*\n")
    o.append(f"\n## Bilanț pe 14 zile\n\n| | Țintă | Media planului | |\n|---|--:|--:|---|\n| Calorii | {tgt[0]} | **{r5(avg[0])}** | {'✅' if abs(avg[0]-tgt[0])<=110 else '⚠️'} ({avg[0]-tgt[0]:+.0f}) |\n| Proteine | {tgt[1]} g | **{avg[1]:.0f} g** | {'✅' if avg[1]>=tgt[1] else '⚠️'} |\n| Grăsimi | {tgt[2]} g | **{avg[2]:.0f} g** | {'✅' if abs(avg[2]-tgt[2])<=8 else '⚠️'} |\n| Carbohidrați | {tgt[3]} g | **{avg[3]:.0f} g** | {'✅' if abs(avg[3]-tgt[3])<=20 else '⚠️'} |\n| Fibre | {p.fibre_tinta} g | **{avg[4]:.0f} g** | ✅ peste țintă — apă {p.apa} l/zi, 1–2 săpt. adaptare |\n")
    return "\n".join(o)


for p in plan.persoane:
    W(f"{p.cheie}/4_meniu.md", menu(p))


# ================= 3b. MENIU VIZUAL (rețetele săptămânii, o zi sub alta) =================
def menu_zilnic(p):
    col = 1 if p.portie == "S" else 2
    T = totals(plan, p.portie)
    o = []
    o.append(f"# 📋 Meniu zilnic — {p.nume} (vizualizare rapidă)\n")
    o.append(f"> Doar de citit rapid: o zi sub alta, rețetele mesei una sub alta. Sub numele fiecărui fel: **totalul mesei** (kcal, P/G/C/Fibre — identic cu `4_meniu.md`). Dedesubt, un ingredient pe rând (**un singur rând pe ingredient**, niciodată mai multe înghesuite laolaltă), cu **P/G/C/Fibre** și **kcal** pe coloane separate.\n> Sursa de adevăr (porții exacte) e [`4_meniu.md`](./4_meniu.md) — acesta e doar altă formă de afișare a **aceluiași** meniu, regenerată automat odată cu el.\n")
    for w in SAPT:
        o.append(f"\n## Săptămâna {w}\n")
        for zi in zile_din(plan, w):
            t = T[zi.id]
            o.append(f"## {f'{zi.nume} {zi.semne}'.strip()}\n")
            for tip, icon, rid in zi.mese:
                r = R[rid]
                mm = macro_reteta(plan, r, p.portie)
                o.append(f"**{icon} {tip} — {r.nume}**\n")
                o.append(f"**Total masă — {r5(mm[0])} kcal** (P:{mm[1]:.0f}g, G:{mm[2]:.0f}g, C:{mm[3]:.0f}g, Fibre:{mm[4]:.0f}g)\n")
                o.append("| Ingredient | P/G/C/Fibre | kcal |\n|:---|:---|:---|")
                for _label, items in r.comp:
                    for it in items:
                        ing, g = plan.ingrediente[it[0]], it[col]
                        if g > 0:
                            kcal, pr, gr, cb, fi = [v * g / 100 for v in ing.valori]
                            o.append(f"| {qty(ing, g)} | {pr:.1f}/{gr:.1f}/{cb:.1f}/{fi:.1f} | {kcal:.0f} |")
                o.append("")
            o.append(f"**Total zi — {r5(t[0])} kcal** (P:{t[1]:.0f}g, G:{t[2]:.0f}g, C:{t[3]:.0f}g, Fibre:{t[4]:.0f}g)\n")
    return "\n".join(o)


for p in plan.persoane:
    W(f"{p.cheie}/4b_meniu_zilnic.md", menu_zilnic(p))


# ================= 4. CALENDAR =================
def cal_rows(w):
    rows = []
    for zi in zile_din(plan, w):
        md, pr, gu, ci = zi.retete
        cina, pranz = R[ci].scurt, R[pr].scurt
        # prânzul de azi = cina de ieri, reîncălzită
        if zi.id > 0:
            if plan.zile[zi.id - 1].retete[3] == pr:
                pranz += " (rest)"
        elif R[pr].congelator:      # prima zi: felul scos din congelator, gătit înainte de start
            pranz += " (rest)"
        if R[pr].semn:
            pranz += " " + R[pr].semn
        if R[ci].semn:
            cina += " " + R[ci].semn
        if zi.gatit_override:
            gat = zi.gatit_override
        else:
            gat = f"**{R[ci].scurt} {'×2' if R[ci].proaspat else '×4'}**" + (" (proaspăt)" if R[ci].proaspat else "")
            if R[ci].nota_gatit:
                gat += " " + R[ci].nota_gatit
        gat += " " + (zi.nota_gatit or "")
        rows.append(f"| **{zi.nume[:3]}** {zi.semne} | {R[md].scurt} | {pranz} | {R[gu].scurt} | {cina} | {gat.strip()} |")
    return "\n".join(rows)


def reds(w):
    return " + ".join(R[z.retete[3]].carne_rosie for z in zile_din(plan, w) if R[z.retete[3]].carne_rosie)


def fish(w):
    zile = zile_din(plan, w)
    return " + ".join([R[z.retete[3]].peste for z in zile if R[z.retete[3]].peste] +
                      [R[z.retete[1]].peste for z in zile if R[z.retete[1]].peste])


o = []
o.append("# 📅 Calendarul comun — 2 săptămâni\n")
o.append("> Ce rețetă în ce zi și **când se gătește**, pentru amândoi. Rețetele: [`2_retete.md`](./2_retete.md).\n> Porțiile fiecăruia (S sau M), cantitățile exacte și totalurile zilnice sunt în `ema/4_meniu.md` și `adi/4_meniu.md`.\n> De aici iese lista din [`3_cumparaturi.md`](./3_cumparaturi.md). Generat din `date/plan.db`.\n")
o.append("## Cum e gândit\n")
o.append("- **Se mănâncă la fel, la toate mesele.** Diferă doar mărimea porției (S / M) — carnea și amidonul. Legumele, sosul, condimentele: identice.\n- **Cina de azi = prânzul de mâine.** Fiecare fel principal se gătește o dată, ×4 porții (2 S + 2 M). Se gătește doar seara, 25–45 min activ.\n- **Fiecare fel principal = farfuria 40/40/20**: proteină · legume (min. 3 feluri, la tavă / piure / salată) · amidon + un sos. **Fără lactate cu carne/pește, fără ouă cu carne** în aceeași masă.\n- **Carnea:** pui, porc (mușchi, cotlet), vită — max. 2 feluri de carne roșie pe săptămână. **Peștele:** doradă, păstrăv, chefal la cuptor (marți, proaspăt) + ton la salată (miercuri). Somon mai rar, ca variantă.\n- **Ouă: o zi da, o zi nu** — 3 ouă de persoană în ziua cu ouă (🥚), lactate în cealaltă.\n- **Micul dejun fără ouă se pregătește seara** (borcanele de ovăz) sau în 5 min (bolul de iaurt).\n- **Sală: marți și joi** *(presupus — de confirmat)* → gustarea e shake-ul post-sală. În celelalte zile skyr cu măr / brânză de vaci cu pâine la ~16:00.\n- **Diversitate (American Gut Project):** ~40 de plante diferite pe săptămână (țintă ≥30).\n- **Ciclul se repetă** după 2 săptămâni. Ce nu place se scoate din rotație și se înlocuiește.\n")
HDR = "| Zi | Mic dejun | Prânz | Gustare | Cină | Ce se gătește seara |\n|----|-----------|-------|---------|------|---------------------|"
o.append("## Săptămâna 1\n\n" + HDR + "\n| **Dum 0** | — | — | — | Chili de linte cu pui | **Chili de linte cu pui ×8** (4 la congelator pt. săpt. 2) |\n" + cal_rows(1) + "\n")
o.append("## Săptămâna 2\n\n" + HDR + "\n" + cal_rows(2) + "\n")
o.append("## Verificare pe săptămână\n\n| Regulă | Săpt. 1 | Săpt. 2 |\n|---|:-:|:-:|")
o.append(f"| Pește 2× (cuptor + salată) | {fish(1)} ✅ | {fish(2)} ✅ |")
o.append("| Ouă alternate, 3/zi cu ouă | Lun, Mie, Vin, Dum ✅ | Mar, Joi, Sâm ✅ |")
o.append("| Lactate zilnic (skyr / iaurt / brânză de vaci) — doar la mic dejun și gustări | ✅ | ✅ |")
o.append("| Fără lactate cu carne/pește, fără ouă cu carne | ✅ | ✅ |")
o.append(f"| Carne roșie: max 2 feluri/săpt. | {reds(1)} ✅ | {reds(2)} ✅ |")
o.append("| Legume: min. 3 feluri pe farfurie, grupe rotite | ✅ | ✅ |")
o.append(f"| Plante diferite (AGP ≥30) | {len(plants(plan, 1))} ✅ | {len(plants(plan, 2))} ✅ |\n")
o.append("## Organizare bucătărie\n\n- **Cutii:** 8 cutii de 1 L cu capac (4 pentru prânzurile de a doua zi, 4 pentru congelator). Se marchează S / M pe capac.\n- **Congelator:** chili-ul și tocănița de vită se congelează perfect. Se scot dimineața, se reîncălzesc seara.\n- **Staples de ținut în casă mereu:** ovăz, orez basmati, orez brun, paste integrale, quinoa, hrișcă, linte, năut conservă, ton conservă, roșii pasate, mălai, ulei de măsline, tahini, muștar, chia, in, nuci/migdale/caju, semințe de dovleac, condimente (boia afumată, chimion, curry, oregano, turmeric, cimbru), fructe de pădure congelate, fasole verde congelată, spanac congelat.\n- **Proaspăt, de 2× pe săptămână:** carne/pește, lactate, legume, fructe, pâine.\n- **Cântar de bucătărie** — obligatoriu primele 2 săptămâni, până se învață porțiile din ochi.\n")
W("comun/4_calendar.md", "\n".join(o))


# ================= 5. SITE (_site/data.js) =================
# Site-ul (index.html + _site/) nu are conținut propriu: tot ce arată vine de aici, adică
# din plan.db. Înainte citea meniurile din fișierele .md și le spărgea cu regex-uri; acum
# primește direct structura, aceeași pe care o desenează (zile → mese → ingrediente).
# Fișierul se scrie la FIECARE rulare — meniul și site-ul nu pot rămâne desincronizate
# (regulă în CLAUDE.md §3).

def meniu_site(p):
    col = 1 if p.portie == "S" else 2
    T = totals(plan, p.portie)
    sapt = []
    for w in SAPT:
        zile = []
        for zi in zile_din(plan, w):
            t = T[zi.id]
            mese = []
            for tip, icon, rid in zi.mese:
                r = R[rid]
                mm = macro_reteta(plan, r, p.portie)
                ing = []
                for _label, items in r.comp:
                    for it in items:
                        al, g = plan.ingrediente[it[0]], it[col]
                        if g <= 0:
                            continue
                        kcal, pr, gr, cb, fi = [v * g / 100 for v in al.valori]
                        q, u, nume = parte_qty(al, g)
                        ing.append({"qty": q, "unit": u, "name": nume, "p": r1(pr), "g": r1(gr),
                                    "c": r1(cb), "f": r1(fi), "k": r0(kcal)})
                mese.append({"icon": icon, "type": tip, "name": r.nume,
                             "total": {"k": r5(mm[0]), "p": r0(mm[1]), "g": r0(mm[2]),
                                       "c": r0(mm[3]), "f": r0(mm[4])},
                             "ing": ing})
            # Vitaminele zilei, pentru banda verde de la paginile Detaliat. Cele două cifre
            # care contează: `v` = cât a strâns ziua și `dzr` = cât e referința, în aceeași
            # unitate — se scriu ca „1692/800µg". Procentul NU se scrie (ar fi exact v/dzr,
            # adică o a treia cifră derivată din primele două); el pleacă doar ca `pct`,
            # pentru cât se umple liniuța. Rotunjirile se fac abia aici, la scris.
            vit, fara_date = micro_zi(plan, zi, p.portie, [i for i, _e in VITAMINE_ZI])
            zile.append({"name": zi.nume, "tags": zi.semne,
                         "total": {"k": r5(t[0]), "p": r0(t[1]), "g": r0(t[2]),
                                   "c": r0(t[3]), "f": r0(t[4])},
                         "vit": [{"n": et, "v": mic(vit[i]), "dzr": mic(plan.nutrienti[i].dzr),
                                  "u": unit(i), "pct": r0(procent_dzr(plan, i, vit[i]))}
                                 for i, et in VITAMINE_ZI],
                         "vitPartial": fara_date,   # câte ingrediente n-au valori în USDA
                         "meals": mese})
        sapt.append({"n": w, "days": zile})
    return sapt


_meniu = {p.cheie: meniu_site(p) for p in plan.persoane}

# în ce zile apare fiecare rețetă (Lu…Du, săpt. 1 / 2) — reper pe pagina de rețete
_zile = {}
for zi in plan.zile:
    for rid in zi.retete:
        _zile.setdefault(rid, []).append(f"{zi.nume_scurt}{zi.saptamana}")

_retete = []
for rid, r in R.items():
    s_, m_ = macro_reteta(plan, r, "S"), macro_reteta(plan, r, "M")
    # oala pentru amândoi: cantitățile S (Ema) + M (Adi) adunate. Din ele ies și linia
    # de macro-uri, și vitaminele de pe pagina de rețete din caietul de print.
    t_ = macro_suma(plan, r)
    vit, fara_date = micro_suma(plan, r, [i for i, _e in VITAMINE])
    _retete.append({
        "id": rid, "nume": r.nume, "scurt": r.scurt, "grup": r.grup,
        "masa": r.masa, "timp": r.timp, "tine": r.tine,
        "kcal": {"s": r5(s_[0]), "m": r5(m_[0])},
        "macro": {"s": {"p": r0(s_[1]), "g": r0(s_[2]), "c": r0(s_[3]), "f": r0(s_[4])},
                  "m": {"p": r0(m_[1]), "g": r0(m_[2]), "c": r0(m_[3]), "f": r0(m_[4])}},
        "comp": [{"eticheta": lbl.strip(),
                  "items": [{"nume": nume_ing(plan.ingrediente[k]),
                             "s": cant(plan.ingrediente[k], gs), "m": cant(plan.ingrediente[k], gm),
                             "sm": cant(plan.ingrediente[k], gs + gm)}
                            for k, gs, gm in items if gs > 0 or gm > 0]}
                 for lbl, items in r.comp],
        "pasi": r.pasi,
        "sfat": r.sfat,
        "varianta": r.varianta,
        "total": {"k": r5(t_[0]), "p": r0(t_[1]), "g": r0(t_[2]), "c": r0(t_[3]), "f": r0(t_[4])},
        "vit": [{"n": et, "v": mic(vit[i]), "u": unit(i)} for i, et in VITAMINE],
        "vitPartial": fara_date,   # câte ingrediente n-au valori în USDA (deci lipsesc din sumă)
        "zile": _zile.get(rid, []),
    })

# alimentele folosite efectiv în plan — marcate pe pagina de alimente
_in_plan = {k for r in R.values() for portie in ("S", "M") for k, _g in r.ingrediente(portie)}
_alimente = [{
    "cat": cat.nume, "icon": cat.icon, "rol": cat.rol,
    "items": [{"nume": i.nume, "kcal": numar(i.kcal), "p": numar(i.proteine), "g": numar(i.grasimi),
               "c": numar(i.carbo), "f": numar(i.fibre), "plan": i.cheie in _in_plan,
               # valorile din coloanele MICRO, în aceeași ordine; null la cele trei alimente
               # care n-au corespondent în USDA (laptele 1,5%, cocosul light, mixul de fructe)
               "micro": [mic(i.micro.get(nid, 0.0)) for nid, _e in MICRO] if i.micro else None}
              for i in cat.ingrediente],
} for cat in plan.categorii]

# capul de tabel al micronutrienților: o singură dată, nu la fiecare aliment
_micro_cap = [{"n": et, "u": unit(nid),
               "g": "vitamina" if nid in (1106, 1162, 1114, 1109, 1185, 1165, 1166, 1167,
                                          1170, 1175, 1177, 1178, 1180) else "mineral"}
              for nid, et in MICRO]

W("_site/data.js",
  "// generat de date/genereaza.py din date/plan.db — nu se editează manual\n"
  "window.MENIU = " + json.dumps(_meniu, ensure_ascii=False) + ";\n"
  "window.RETETE = " + json.dumps(_retete, ensure_ascii=False) + ";\n"
  "window.ALIMENTE = " + json.dumps(_alimente, ensure_ascii=False) + ";\n"
  "window.MICRO = " + json.dumps(_micro_cap, ensure_ascii=False) + ";\n")

# ================= 6. DUMP-UL BAZEI (pentru git) =================
db.scrie_dump()

print("OK")
for p in plan.persoane:
    print(p.portie, [round(a) for a in medie(totals(plan, p.portie))])
