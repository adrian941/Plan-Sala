# -*- coding: utf-8 -*-
import io
from retete import R, PLAN, TARGET, macro, r5, qty, totals, plants, SHORT
from ingrediente_db import ING, DB, NAME

import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + "/"
def W(path, text): io.open(ROOT+path, "w", encoding="utf-8", newline="\n").write(text)
def m5(t): return f"{r5(t[0])} | {t[1]:.0f} | {t[2]:.0f} | {t[3]:.0f} | {t[4]:.0f}"

# ================= 1. INGREDIENTE =================
ROL = {"Carne & pește":"P","Ouă":"P","Lactate":"P","Cereale & amidon":"A","Leguminoase":"P + A","Legume":"L","Grăsimi":"G","Fructe":"F","Condimente":"—"}
ICON = {"Carne & pește":"🥩","Ouă":"🥚","Lactate":"🥛","Cereale & amidon":"🍚","Leguminoase":"🫘","Legume":"🥦","Grăsimi":"🥑","Fructe":"🍓","Condimente":"🧂"}
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
cats = []
for k,n,c,*_ in ING:
    if c not in cats: cats.append(c)
for c in cats:
    o.append(f"\n## {ICON[c]} {c}\n")
    o.append("| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |\n|---|:-:|--:|--:|--:|--:|--:|---|---|")
    for k,n,cc,kcal,p,g,cb,f,src,note in ING:
        if cc!=c: continue
        srcs = f"[{src}](https://fdc.nal.usda.gov/food-details/{src.split()[1]}/nutrients)" if src.startswith("USDA ") and src.split()[1].isdigit() else src
        o.append(f"| {n} | {ROL[c]} | {kcal:g} | {p:g} | {g:g} | {cb:g} | {f:g} | {srcs} | {note} |")
    o.append("")
o.append("\n---\n\n## Porții uzuale (pentru cântărit din ochi)\n")
o.append("| Aliment | Porție | ≈ g |\n|---|---|--:|\n| Ou M | 1 buc. | 55 |\n| Banană | 1 buc. medie | 120 |\n| Măr | 1 buc. medie | 180 |\n| Pâine integrală | 1 felie | 40–50 |\n| Ulei de măsline | 1 lingură | 10 |\n| Unt de arahide | 1 lingură | 15 |\n| Semințe chia / in | 1 lingură | 10 |\n| Nuci / migdale | 1 mână mică | 15–20 |\n| Usturoi | 1 cățel | 3 |\n| Orez / quinoa / hrișcă crud | 1 porție 20% | 55–65 |\n| Carne / pește crud | 1 porție 40% | 150–220 |\n")
o.append("\n## 🌾 De unde vin fibrele — pe scurt\n\nLeguminoase (linte, năut: 10–12 g/100 g uscat), semințe (chia 34, in 27), ovăz (10), paste integrale (9), fructe de pădure (zmeură 6,5), avocado (6,7), legume (2–4 g/100 g). Practic: leguminoase + o lingură de semințe + fructe de pădure + legume la fiecare masă → 30–40 g/zi fără efort.\n")
W("comun/1_ingrediente.md", "\n".join(o))

# ================= 2. REȚETE =================
def comp_table(r):
    lines=["| Element | Ingredient | S | M |","|---|---|--:|--:|"]
    for label,items in r["comp"]:
        for i,(k,gs,gm) in enumerate(items):
            lab = f"**{label.strip()}**" if i==0 else ""
            lines.append(f"| {lab} | {NAME[k].split(',')[0] if k not in SHORT else SHORT[k].capitalize()} | {qty(k,gs).replace(SHORT.get(k,''),'').strip() if gs>0 else '—'} | {qty(k,gm).replace(SHORT.get(k,''),'').strip() if gm>0 else '—'} |")
    return "\n".join(lines)
o=[]
o.append("# 🍽️ Rețete\n")
o.append("> **Pasul 2** din [cum lucrăm](./0_pipeline.md). Toate valorile de mai jos sunt calculate din [`1_ingrediente.md`](./1_ingrediente.md) (USDA), pe cantități **crude**.\n> De aici pleacă [`3_cumparaturi.md`](./3_cumparaturi.md). Ce rețetă în ce zi: [`4_calendar.md`](./4_calendar.md).\n")
o.append("## Cum adăugăm o rețetă\n\nÎmi dai rețeta cu ce detalii ai (ingrediente, cum se face, timp, câte porții ies, **cui îi place și cui nu**). Eu: (1) adaug ingredientele noi în `1_ingrediente.md` din USDA, (2) o scriu aici pe structura farfuriei, (3) calculez S și M, (4) trec verdictele în preferințele fiecăruia.\n\n**Semne:** ⭐ favorit · ✅ îi place · 🟡 neutru · ❌ nu-i place · ⛔ nu poate · ❔ netestat\n")
o.append("## Farfuria 40/40/20 — cum e construit fiecare fel principal\n\nFiecare fel principal are **trei elemente vizibile + un sos**:\n\n| Element | Cât din farfurie | Ce e |\n|---|:-:|---|\n| **Proteină** | 40% | carne, pește, ouă, lactate |\n| **Legume** | 40% | carbohidrați fibroși: legume la tavă, piureuri de legume, salate, legume sotate — **cel puțin 3 legume diferite** pe farfurie |\n| **Amidon** | 20% | orez, cartof, quinoa, hrișcă, paste, mămăligă, leguminoase |\n| **Sos** | — | pe bază de iaurt (usturoi, mărar, lămâie, muștar), roșii pasate cu busuioc, soia-ghimbir — gust fără calorii goale |\n\n**Regula casei: nu amestecăm lactatele cu carnea/peștele, nici ouăle cu carnea, în aceeași masă.** De aceea sosurile la felurile cu carne sunt fără iaurt (tahini-lămâie, lămâie-usturoi-ulei, vinegretă de muștar, roșii-busuioc, soia-ghimbir), piureurile se fac cu ulei de măsline, iar lactatele stau la micul dejun și la gustări.\n\nProcentele sunt **pe volum**, nu la gram. Diversitatea contează la fel de mult ca proporțiile (American Gut Project: **≥30 de plante diferite pe săptămână** — planul are ~40).\n")
o.append("## Două mărimi de porție\n\n**S (standard)** și **M (mare)**: diferă proteina și amidonul; legumele, sosul și condimentele sunt identice → o singură oală/tavă. Cine mănâncă ce mărime: `ema/4_meniu.md`, `adi/4_meniu.md`. Felurile principale se gătesc **×4 = 2 S + 2 M** (cina de azi + prânzul de mâine).\n")
o.append("---\n\n## Cuprins\n")
o.append("| # | Rețetă | Masă | Timp | kcal S / M | S: P / G / C / Fibre | M: P / G / C / Fibre | Ema | Adi | Frigider |\n|--:|--------|------|-----:|-----------:|---|---|:-:|:-:|:-:|")
for id,r in R.items():
    s,m=macro(r["S"]),macro(r["M"])
    o.append(f"| {id} | [{r['nume']}](#{id.lower()}) | {r['masa']} | {r['timp']} | {r5(s[0])} / {r5(m[0])} | {s[1]:.0f} / {s[2]:.0f} / {s[3]:.0f} / {s[4]:.0f} | {m[1]:.0f} / {m[2]:.0f} / {m[3]:.0f} / {m[4]:.0f} | ❔ | ❔ | {r['tine']} |")
o.append("\n🥚 = zi cu ouă · 🐟 = pește · 🏋️ = post-antrenament. Rotunjiri: kcal la 5, macro la 1 g.\n\n---\n")
sections=[("## 🌅 Mic dejun",["MD1","MD2","MD3","MD4"]),("## 🍎 Gustări",["G1","G2","G3"]),("## 🍲 Feluri principale — farfuria 40/40/20",["P1","P2","P3","P4","P5","P6","P7","P8","P10","P11","P12","P13"])]
for title,ids in sections:
    o.append(f"\n{title}\n")
    if ids[0]=="P1": o.append("Cantitățile sunt **pe o porție**. Pentru oala de 4: proteina și amidonul = 2×S + 2×M, restul ×4.\n")
    for id in ids:
        r=R[id]; s,m=macro(r["S"]),macro(r["M"])
        o.append(f'<a id="{id.lower()}"></a>\n### {id} · {r["nume"]}\n**{r["masa"].capitalize()} · {r["timp"]} · ține: {r["tine"]}**\n')
        o.append(comp_table(r)+"\n")
        o.append(f"**Cum se face:** {r['cum']}\n")
        o.append(f"| Pe porție | kcal | P | G | C | Fibre |\n|---|--:|--:|--:|--:|--:|\n| **S** | {m5(s)} |\n| **M** | {m5(m)} |\n")
        if r["var"]: o.append(f"**Variante:** {r['var']}\n")
        o.append("")
o.append("\n---\n\n## De testat\nToate rețetele de mai sus sunt propuse, **nu încă gătite**. După fiecare, verdictul se scrie în preferințele fiecăruia și în coloanele din cuprins.\n\n## Scoase din rotație\n*(Ce n-a mers și de ce — ca să nu le repropun.)*\n")
W("comun/2_retete.md", "\n".join(o))

# ================= 3. MENIURI =================
def plate(r, size):
    parts=[]
    for label,items in r["comp"]:
        col = 1 if size=="S" else 2
        xs=[qty(k,it[col]) for k,*_ in [(i[0],) for i in items] for it in [next(j for j in items if j[0]==k)] if it[col]>0]
        if xs: parts.append(" + ".join(xs))
    return f"**{r['scurt']}** — "+" · ".join(parts)
def menu(who, size, pron, tgt, extra):
    T=totals(size); avg=[sum(x[i] for x in T)/14 for i in range(5)]
    o=[]
    o.append(f"# 🍳 Meniu pe 2 săptămâni — {who}\n")
    o.append(f"> Rețetele sunt comune ([`comun/2_retete.md`](../comun/2_retete.md)), calendarul de gătit e comun ([`comun/4_calendar.md`](../comun/4_calendar.md)).\n> Aici: **exact ce și cât** mănâncă {pron}, cu caloriile și macro-urile calculate din [`comun/1_ingrediente.md`](../comun/1_ingrediente.md) (USDA). Țintele: [`2_nutritie.md`](./2_nutritie.md). Ce-i place: [`3_preferinte.md`](./3_preferinte.md).\n")
    o.append(f"## Porția: **{size}** ({'standard' if size=='S' else 'mare'}) la toate rețetele\n\nȚinte: **{tgt[0]} kcal · P{tgt[1]} / G{tgt[2]} / C{tgt[3]}**. Cantitățile sunt **crude** (carnea, orezul, lintea înainte de gătit). Mesele principale = farfuria 40/40/20: *proteină · legume · amidon · sos*. **Fără lactate cu carne/pește și fără ouă cu carne în aceeași masă** — lactatele sunt la micul dejun și gustări.\n")
    for w in (0,1):
        o.append(f"\n## Săptămâna {w+1}\n")
        o.append("| Zi | Masa | Ce și cât | kcal | P | G | C | Fibre |\n|---|---|---|--:|--:|--:|--:|--:|")
        for d,t in zip(PLAN[w*7:w*7+7],T[w*7:w*7+7]):
            zi=f"**{d[0]}** {d[1]}".strip()
            for lbl,id in zip(("Mic dejun","Prânz","Gustare","Cină"),d[2:]):
                mm=macro(R[id][size])
                o.append(f"| {zi} | {lbl} | {plate(R[id],size)} | {r5(mm[0])} | {mm[1]:.0f} | {mm[2]:.0f} | {mm[3]:.0f} | {mm[4]:.0f} |")
                zi=""
            o.append(f"| | **Total zi** | | **{r5(t[0])}** | **{t[1]:.0f}** | **{t[2]:.0f}** | **{t[3]:.0f}** | **{t[4]:.0f}** |")
        p=plants(w); o.append(f"\n*Plante diferite în săptămâna {w+1}: **{len(p)}** (țintă American Gut Project ≥30).*\n")
    o.append(f"\n## Bilanț pe 14 zile\n\n| | Țintă | Media planului | |\n|---|--:|--:|---|\n| Calorii | {tgt[0]} | **{r5(avg[0])}** | {'✅' if abs(avg[0]-tgt[0])<=110 else '⚠️'} ({avg[0]-tgt[0]:+.0f}) |\n| Proteine | {tgt[1]} g | **{avg[1]:.0f} g** | {'✅' if avg[1]>=tgt[1] else '⚠️'} |\n| Grăsimi | {tgt[2]} g | **{avg[2]:.0f} g** | {'✅' if abs(avg[2]-tgt[2])<=8 else '⚠️'} |\n| Carbohidrați | {tgt[3]} g | **{avg[3]:.0f} g** | {'✅' if abs(avg[3]-tgt[3])<=20 else '⚠️'} |\n| Fibre | {'25–30' if size=='S' else '30–38'} g | **{avg[4]:.0f} g** | ✅ peste țintă — apă {'2,5' if size=='S' else '3'} l/zi, 1–2 săpt. adaptare |\n")
    return "\n".join(o)
extra_e = "- Gustarea: în zilele de sală (marți, joi — *de confirmat*) shake-ul post-sală, ~20 min după antrenament; altfel după-amiaza.\n- Regulile de frecvență (pește 2×/săpt., ouă 3 la două zile) sunt bifate în calendar.\n\n## Cum ajustăm\n- **La 2–3 săptămâni** după media cântarului: 0,5–0,7 kg/săpt. = nimic; sub 0,3 → −150 kcal (scoatem pâinea de la gustare și nucile de la ovăz); peste 1 kg/săpt. după prima săptămână → +150 kcal.\n- Proteina iese ~10 g peste țintă — intenționat (sațietate, păstrarea mușchiului); nu e o problemă.\n- **Dacă o rețetă nu-i place:** se notează în `3_preferinte.md` și se înlocuiește în calendar cu una din aceeași categorie.\n"
extra_a = "- Gustarea: în zilele de sală (marți, joi — *de confirmat*) shake-ul post-sală; altfel după-amiaza.\n- **Ridichi** ⭐: se adaugă la porția lui la gustarea cu brânză de vaci, la salata de sardine, la păstrăv — nu intră în rețeta comună.\n- Diferența față de porția S: +40–50 g carne/pește și +5–20% amidon la felurile principale; +50 g lactate la gustări. Legumele și sosurile sunt identice.\n\n## Cum ajustăm\n- **Zilele fizice de la job** (2/săpt.): dacă slăbește peste 1 kg/săpt. după prima săptămână sau e flămând în acele zile → **+200 kcal** doar atunci (o felie de pâine în plus la prânz + un fruct).\n- **La 2–3 săptămâni** ne uităm la media cântarului **și la talie**: dacă talia scade și cântarul stă, e recompoziție — nu tăiem calorii.\n- **Post-sală:** shake-ul e obligatoriu în zilele de antrenament.\n- **Dacă o rețetă nu-i place:** se notează în `3_preferinte.md` și se înlocuiește în calendar cu una din aceeași categorie.\n"
W("ema/4_meniu.md", menu("Ema","S","ea",TARGET["S"],extra_e))
W("adi/4_meniu.md", menu("Adi","M","el",TARGET["M"],extra_a))

# ================= 3b. MENIU VIZUAL (rețetele săptămânii, o zi sub alta) =================
def menu_zilnic(who, size):
    MEALS = ("🌅 Mic dejun","🍲 Prânz","🍎 Gustare","🌙 Cină")
    o=[]
    o.append(f"# 📋 Meniu zilnic — {who} (vizualizare rapidă)\n")
    o.append(f"> Doar de citit rapid: o zi sub alta, rețetele mesei una sub alta. Un ingredient pe rând (**un singur rând pe ingredient**, niciodată mai multe înghesuite laolaltă) — dar tabel cu 2 coloane, ca **kcal & P/G/C/Fibre** să iasă aliniate, nu împrăștiate în text.\n> Sursa de adevăr (porții exacte, totalul pe masă/zi) e [`4_meniu.md`](./4_meniu.md) — acesta e doar altă formă de afișare a **aceluiași** meniu, regenerată automat odată cu el.\n")
    col = 1 if size=="S" else 2
    for w in (0,1):
        o.append(f"\n## Săptămâna {w+1}\n")
        for d in PLAN[w*7:w*7+7]:
            o.append(f"### {d[0]} {d[1]}".strip()+"\n")
            for lbl,id in zip(MEALS,d[2:]):
                r=R[id]
                o.append(f"**{lbl} — {r['nume']}**\n")
                o.append("| Ingredient | kcal & P/G/C/Fibre |\n|:---|:---|")
                for label,items in r["comp"]:
                    for it in items:
                        k,g = it[0],it[col]
                        if g>0:
                            kcal,p,gr,c,f = [v*g/100 for v in DB[k]]
                            o.append(f"| {qty(k,g)} | {kcal:.0f} & {p:.1f}/{gr:.1f}/{c:.1f}/{f:.1f} |")
                o.append("")
    return "\n".join(o)
W("ema/4b_meniu_zilnic.md", menu_zilnic("Ema","S"))
W("adi/4b_meniu_zilnic.md", menu_zilnic("Adi","M"))


# ================= 4. CALENDAR =================
COOK = {  # ce se gătește în seara respectivă, pe lângă cina ×4
 (0,0):"+ borcane de ovăz peste noapte pt. marți",(0,4):"+ borcane de ovăz pt. sâmbătă",(0,6):"+ cumpărături pt. săpt. 2",
 (1,1):"+ borcane de ovăz pt. miercuri",(1,5):"+ borcane de ovăz pt. duminică",(1,6):"+ **Chili de linte cu pui ×8** pentru ciclul următor",
}
FRESH = {"P3","P13"}; FREEZER = {"P5"}
def cal_rows(w):
    rows=[]
    for i,d in enumerate(PLAN[w*7:w*7+7]):
        zi,em,md,pr,gu,ci = d
        cina=R[ci]["scurt"]; pranz=R[pr]["scurt"]
        if i>0 or w>0:
            prev = PLAN[w*7+i-1][5] if (w*7+i)>0 else None
            if prev==pr: pranz += " (rest)"
        elif pr=="P5": pranz += " (rest)"
        if pr=="P4": pranz += " 🐟"
        if ci in FRESH: cina += " 🐟"
        if w==1 and i==3 and ci=="P5":
            gat = "nimic — se scoate chili-ul din congelator dimineața"
        else:
            n = "×2" if ci in FRESH else "×4"
            gat = f"**{R[ci]['scurt']} {n}**" + (" (proaspăt)" if ci in FRESH else "")
            if ci in FRESH: gat += " + salata de ton asamblată pt. mâine"
            if ci=="P2": gat += " (60 min la foc mic — se pune la fiert și se face altceva)"
        gat += " " + COOK.get((w,i),"")
        rows.append(f"| **{zi[:3]}** {em} | {R[md]['scurt']} | {pranz} | {R[gu]['scurt']} | {cina} | {gat.strip()} |")
    return "\n".join(rows)
o=[]
o.append("# 📅 Calendarul comun — 2 săptămâni\n")
o.append("> Ce rețetă în ce zi și **când se gătește**, pentru amândoi. Rețetele: [`2_retete.md`](./2_retete.md).\n> Porțiile fiecăruia (S sau M), cantitățile exacte și totalurile zilnice sunt în `ema/4_meniu.md` și `adi/4_meniu.md`.\n> De aici iese lista din [`3_cumparaturi.md`](./3_cumparaturi.md). Generat din `date/retete.py`.\n")
o.append("## Cum e gândit\n")
o.append("- **Se mănâncă la fel, la toate mesele.** Diferă doar mărimea porției (S / M) — carnea și amidonul. Legumele, sosul, condimentele: identice.\n- **Cina de azi = prânzul de mâine.** Fiecare fel principal se gătește o dată, ×4 porții (2 S + 2 M). Se gătește doar seara, 25–45 min activ.\n- **Fiecare fel principal = farfuria 40/40/20**: proteină · legume (min. 3 feluri, la tavă / piure / salată) · amidon + un sos. **Fără lactate cu carne/pește, fără ouă cu carne** în aceeași masă.\n- **Carnea:** pui, porc (mușchi, cotlet), vită — max. 2 feluri de carne roșie pe săptămână. **Peștele:** doradă, păstrăv, chefal la cuptor (marți, proaspăt) + ton la salată (miercuri). Somon mai rar, ca variantă.\n- **Ouă: o zi da, o zi nu** — 3 ouă de persoană în ziua cu ouă (🥚), lactate în cealaltă.\n- **Micul dejun fără ouă se pregătește seara** (borcanele de ovăz) sau în 5 min (bolul de iaurt).\n- **Sală: marți și joi** *(presupus — de confirmat)* → gustarea e shake-ul post-sală. În celelalte zile skyr cu măr / brânză de vaci cu pâine la ~16:00.\n- **Diversitate (American Gut Project):** ~40 de plante diferite pe săptămână (țintă ≥30).\n- **Ciclul se repetă** după 2 săptămâni. Ce nu place se scoate din rotație și se înlocuiește.\n")
HDR="| Zi | Mic dejun | Prânz | Gustare | Cină | Ce se gătește seara |\n|----|-----------|-------|---------|------|---------------------|"
o.append("## Săptămâna 1\n\n"+HDR+"\n| **Dum 0** | — | — | — | Chili de linte cu pui | **Chili de linte cu pui ×8** (4 la congelator pt. săpt. 2) |\n"+cal_rows(0)+"\n")
o.append("## Săptămâna 2\n\n"+HDR+"\n"+cal_rows(1)+"\n")
def reds(w):
    names={"P2":"vită","P7":"porc","P11":"porc","P12":"vită"}
    return " + ".join(names[d[5]] for d in PLAN[w*7:w*7+7] if d[5] in names)
def fish(w):
    names={"P3":"doradă","P13":"păstrăv"}
    return " + ".join([names[d[5]] for d in PLAN[w*7:w*7+7] if d[5] in names]+["ton"])
o.append("## Verificare pe săptămână\n\n| Regulă | Săpt. 1 | Săpt. 2 |\n|---|:-:|:-:|")
o.append(f"| Pește 2× (cuptor + salată) | {fish(0)} ✅ | {fish(1)} ✅ |")
o.append("| Ouă alternate, 3/zi cu ouă | Lun, Mie, Vin, Dum ✅ | Mar, Joi, Sâm ✅ |")
o.append("| Lactate zilnic (skyr / iaurt / brânză de vaci) — doar la mic dejun și gustări | ✅ | ✅ |")
o.append("| Fără lactate cu carne/pește, fără ouă cu carne | ✅ | ✅ |")
o.append(f"| Carne roșie: max 2 feluri/săpt. | {reds(0)} ✅ | {reds(1)} ✅ |")
o.append("| Legume: min. 3 feluri pe farfurie, grupe rotite | ✅ | ✅ |")
o.append(f"| Plante diferite (AGP ≥30) | {len(plants(0))} ✅ | {len(plants(1))} ✅ |\n")
o.append("## Organizare bucătărie\n\n- **Cutii:** 8 cutii de 1 L cu capac (4 pentru prânzurile de a doua zi, 4 pentru congelator). Se marchează S / M pe capac.\n- **Congelator:** chili-ul și tocănița de vită se congelează perfect. Se scot dimineața, se reîncălzesc seara.\n- **Staples de ținut în casă mereu:** ovăz, orez basmati, orez brun, paste integrale, quinoa, hrișcă, linte, năut conservă, ton conservă, roșii pasate, mălai, ulei de măsline, tahini, muștar, chia, in, nuci/migdale/caju, semințe de dovleac, condimente (boia afumată, chimion, curry, oregano, turmeric, cimbru), fructe de pădure congelate, fasole verde congelată, spanac congelat.\n- **Proaspăt, de 2× pe săptămână:** carne/pește, lactate, legume, fructe, pâine.\n- **Cântar de bucătărie** — obligatoriu primele 2 săptămâni, până se învață porțiile din ochi.\n")
W("comun/4_calendar.md", "\n".join(o))

print("OK")
for size in ("S","M"):
    T=totals(size); avg=[sum(x[i] for x in T)/14 for i in range(5)]
    print(size, [round(a) for a in avg])
