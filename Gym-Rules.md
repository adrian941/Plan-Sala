# Gym-Rules.md — Planul VIU

> Acesta este documentul „viu": se updatează la fiecare sesiune de brainstorming.
> Regulile de fond și persona sunt în **[CLAUDE.md](./CLAUDE.md)** (fișier stabil).
> Cum lucrăm la mâncare, în 3 pași: **[`comun/0_pipeline.md`](./comun/0_pipeline.md)**.
>
> **Status curent:** 🟡 Ema are profilul și țintele gata. Mâncarea și cumpărăturile se fac la comun;
> **Adi se completează ulterior**.

---

## 🍽️ Mâncare — comun (Ema + Adi)

| Pas | Fișier | Ce conține | Status |
|-----|--------|-----------|--------|
| Cum lucrăm | [`comun/0_pipeline.md`](./comun/0_pipeline.md) | Cei 3 pași + ce înseamnă semnele | 🟢 |
| 1️⃣ Alimente | [`comun/1_ingrediente.md`](./comun/1_ingrediente.md) | **Sursa unică**: ~100 alimente cu kcal/P/G/C/fibre per 100 g, din USDA (cu ID) | 🟢 USDA SR Legacy |
| 2️⃣ Rețete | [`comun/2_retete.md`](./comun/2_retete.md) | Rețetele + ce iese pe porție | 🟢 19 rețete pe farfuria 40/40/20 (proteină · legume · amidon · sos), porții S/M, calculate din USDA — toate ❔ netestate |
| 📅 Calendar | [`comun/4_calendar.md`](./comun/4_calendar.md) | Ce rețetă în ce zi, când se gătește, pe 2 săptămâni (generat din `date/`) | 🟢 ciclu de 2 săpt. · sală marți+joi (de confirmat) |
| 🧮 Baza de date | [`date/`](./date/README.md) | `ingrediente_db.py` (USDA) + `retete.py` + `genereaza.py` → regenerează ingredientele, rețetele și meniurile | 🟢 |
| 3️⃣ Cumpărături | [`comun/3_cumparaturi.md`](./comun/3_cumparaturi.md) | Lista + magazinele | ⚪ blocat: lipsesc magazinele |

## 🧍 Ema

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| Profil & obiective | [`ema/1_profil.md`](./ema/1_profil.md) | Date, activitate, sănătate, obiectiv | 🟡 lipsesc talie/șold, job, somn, loc antrenament |
| Nutriție | [`ema/2_nutritie.md`](./ema/2_nutritie.md) | Calorii, macro, fibre | 🟢 2200 kcal · P150/G65/C255 · fibre 25–30 g |
| Preferințe | [`ema/3_preferinte.md`](./ema/3_preferinte.md) | Ce-i place, ce nu, frecvențe | 🟡 lipsesc preferințele culinare (metode, condimentare) |
| Meniu | [`ema/4_meniu.md`](./ema/4_meniu.md) | Meniul pe 2 săpt. + porțiile | 🟢 porție S · cantități exacte · medie 2150 kcal · P158/G67/C246 · 40 plante/săpt. |
| Meniu (vizual) | [`ema/4b_meniu_zilnic.md`](./ema/4b_meniu_zilnic.md) | Aceleași rețete, o zi sub alta, ingrediente pe rânduri — doar de citit rapid | 🟢 generat automat odată cu `4_meniu.md` |
| Sală | [`ema/5_sala.md`](./ema/5_sala.md) | Split, exerciții, progresie | ⚪ blocat: unde antrenează |
| Sănătate | [`ema/6_sanatate.md`](./ema/6_sanatate.md) | Somn, stres, mobilitate, monitorizare | ⚪ după profil |

## 🧍 Adi (doar mâncare)

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| Profil | [`adi/1_profil.md`](./adi/1_profil.md) | Date, activitate, sănătate, obiectiv | 🟢 complet (opțional: talie, pași, somn) |
| Nutriție | [`adi/2_nutritie.md`](./adi/2_nutritie.md) | Calorii, macro, fibre | 🟢 2400 kcal · P180/G75/C250 · fibre 30–38 g |
| Preferințe | [`adi/3_preferinte.md`](./adi/3_preferinte.md) | Ce-i place, ce nu, ce nu poate | 🟡 lipsesc preferințele culinare (ore, metode, condimentare) |
| Meniu | [`adi/4_meniu.md`](./adi/4_meniu.md) | Meniul pe 2 săpt. + porțiile | 🟢 porție M · cantități exacte · medie 2420 kcal · P186/G76/C263 · 40 plante/săpt. |
| Meniu (vizual) | [`adi/4b_meniu_zilnic.md`](./adi/4b_meniu_zilnic.md) | Aceleași rețete, o zi sub alta, ingrediente pe rânduri — doar de citit rapid | 🟢 generat automat odată cu `4_meniu.md` |

Legendă: 🟢 stabil · 🟡 în lucru · ⚪ neînceput · 🔴 blocat

## 📚 Wiki — ghiduri generale de antrenament

| Fișier | Ce conține | Status |
|--------|-----------|--------|
| [`wiki/fesieri.md`](./wiki/fesieri.md) | Anatomie + exerciții pentru izolarea fesierilor fără hipertrofierea picioarelor | 🟢 |
| [`wiki/calorii.md`](./wiki/calorii.md) | Cum se calculează BMR (Mifflin-St Jeor, Katch-McArdle), factorii de activitate → TDEE, deficit/surplus, recalibrare | 🟢 |

---

## Principii de fond (le rafinăm împreună)

Acestea sunt reguli generale de plecare; le personalizăm pe măsură ce apar datele Emei.

### Nutriție
- Deficit/surplus **moderat și sustenabil** (fără diete-șoc).
- Proteină suficientă pentru păstrarea masei musculare.
- Legume și fibre la majoritatea meselor; micronutrienți acoperiți.
- Hidratare corectă; minim de ultra-procesate și zahăr adăugat.

### Antrenament
- Prioritate: tehnică corectă și progresie graduală, nu greutăți mari prea repede.
- Antrenament de forță ca bază; cardio adaptat obiectivului și sănătății.
- Recuperare = parte din plan (somn, zile de odihnă).

### Sănătate
- Orice semnal medical → consult, nu improvizație (vezi [CLAUDE.md §4](./CLAUDE.md)).
- Măsurăm progresul pe mai mulți indicatori, nu doar cântarul.

---

## Ordinea de lucru

**Pipeline culinar (cele 3 etape cerute de utilizator):**

1. **Alimente + preferințe + ținte (calorii, macro, fibre).** 🟢 gata pentru amândoi.
2. **Rețete + meniu** ⬅️ *suntem aici* — 19 rețete propuse și puse în calendar pe 2 săptămâni; urmează testarea lor (verdicte în preferințe). Rețete noi de la utilizator se adaugă oricând.
3. **Lista de cumpărături** — generată din meniuri, grupată pe magazine.

**În paralel, doar pentru Ema:**

4. **Sală** — programul de antrenament (blocat: unde antrenează).
5. **Sănătate** — somn/stres/mobilitate/monitorizare.

---

## Jurnal iterații

| Data | Ce am stabilit | Module atinse |
|------|----------------|---------------|
| 2026-09-08 | Restructurare: `CLAUDE.md` (stabil) + `Gym-Rules.md` (viu) + module. Vechile planuri Ema arhivate ca obsolete. Start faza *intake*. | toate (schelet) |
| 2026-09-08 | Date reale Ema: F, 29 ani, 185 cm, 110 kg, % grăsime mare. Ales **Mifflin-St Jeor** → BMR ≈ 1950 kcal. Țintă provizorie ~2100 kcal (deficit 500–650). Rămâne de fixat nivelul de activitate. | 1_profil, 2_nutritie |
| 2026-09-08 | Fișierele din `ema/` prefixate numeric (1–6) în ordinea de lucru. Link-uri actualizate peste tot. | toate |
| 2026-09-08 | Activitate = ușoară (2–3 antrenamente/săpt., 1h). TDEE fixat ≈ 2680 → **țintă 2100 kcal**. Double-check formulă (coef. originali vs rotunjiți → ambele ~1950). Macro: **P 150 / G 65 / C 230**. | 1_profil, 2_nutritie |
| 2026-09-08 | Profil completat: fără probleme medicale/alergii; omnivor cu preferință lactate; ouă 3/2 zile; **pește 2×/săpt. (omega-3)**; obiectiv slăbit (secundar mușchi). Adoptat **regula farfuriei 40/40/20** (aprobată). Creat **7_alimente.md** (liste pe categorii + lista de fibre). Mese: **3 + 1 gustare post-sală**, orele TBD. Gătit la comun cu Adi. | 1_profil, 2_nutritie, 3_plan-mese, 7_alimente |
| 2026-09-08 | Șterse definitiv planurile vechi (arhiva Ema `_arhiva/` + folderul `adi/`). Repo dedicat exclusiv Emei. Curățate referințele din CLAUDE.md / README. | structură |
| 2026-09-10 | Explicat de ce cer **talia și șoldul** (grăsime viscerală, WHR, progres când cântarul stagnează, estimare % grăsime pt. Katch-McArdle). Rămân opționale. | 1_profil |
| 2026-09-10 | **Stabilit pipeline-ul culinar în 3 pași** (ingrediente+preferințe+macro/fibre → rețete → cumpărături). Creat `comun/` cu `0_pipeline.md`, `1_ingrediente.md` (mutat din `ema/7_alimente.md`), `2_retete.md` și `3_cumparaturi.md` (mutat din `ema/6_cumparaturi.md`). Fibrele promovate la macro de rang egal. | toate |
| 2026-09-10 | **Separate lucrurile care se amestecau:** lista de alimente și rețetele rămân comune și fără nume de oameni, iar gusturile trec la fiecare, în `3_preferinte.md`, scrise scurt (doar ce iese din tipar — restul se înțelege că e ok). Motivul: altfel, la fiecare om nou trebuia rescris tot. Preferințele alimentare scoase din profil (se dublau). | toate |
| 2026-09-10 | **Simplificare.** Prima variantă a acestei separări o dusesem în zona tehnică — foldere `persoane/`, șabloane de copiat, script de verificare. Scoase toate: rămân trei foldere citibile — `comun/`, `ema/`, `adi/` — și fișiere .md scrise pe înțelesul oricui. Rețetele stau într-un singur fișier (`comun/2_retete.md`) până se adună multe. | toate |
| 2026-09-13 | Adăugat folder **`wiki/`** pentru ghiduri de antrenament generale (nu personalizate, valabile pentru oricine antrenează). Primul fișier: `wiki/fesieri.md` — anatomie + exerciții pentru izolarea fesierilor fără hipertrofierea picioarelor. Linkat din `ema/5_sala.md`. | wiki |
| 2026-09-14 | **Corecție greutate Ema: 110 → 118 kg.** Recalculat: BMR ≈ 2030 · TDEE ≈ 2790 · **țintă 2200 kcal** (deficit ~590). Macro: **P 150 / G 65 / C 255**. Date de bază Adi: M, 32 ani, 192 cm, 108 kg → **BMR ≈ 2125**; TDEE și țintă blocate până aflăm activitatea și obiectivul. | ema/1_profil, ema/2_nutritie, ema/4_meniu, adi/1_profil, adi/2_nutritie |
| 2026-09-14 | Confirmat: amândoi **2 antrenamente/săpt.** → factor 1.375. Adi: TDEE ≈ **2920**; ținta rămâne blocată de obiectiv. Creat **`wiki/calorii.md`** — formulele BMR, tabelul factorilor de activitate, deficit/surplus, recalibrare. | adi/1_profil, adi/2_nutritie, wiki |
| 2026-09-14 | **Obiectiv Adi**: slăbit max 15 kg (108 → ~93) + dezvoltare musculară → recompoziție. Deficit moderat ~520 → **țintă 2400 kcal**. Macro: **P 180 / G 75 / C 250**, fibre 30–38 g. Proteina pe greutatea-țintă. Orizont ~6–8 luni. | adi/1_profil, adi/2_nutritie |
| 2026-09-14 | Profil Adi închis: fără probleme medicale, fără alergii, fără accidentări. Job mixt (2 zile fizice + acasă) → păstrăm 1.375 (conservator la greutate mare), cu opțiunea +200 kcal în zilele fizice dacă slăbește prea repede. | adi/1_profil |
| 2026-09-14 | Preferințe Adi: fără restricții, fără dezgusturi; **ouă și pește la fel ca Ema** (3 la 2 zile / 2×/săpt.). Singura divergență: **ridichile** — ⭐ Adi, ❌ Ema → se adaugă doar la porția lui. Notat în ambele `3_preferinte.md`. | adi/3_preferinte, ema/3_preferinte |
| 2026-09-14 | **Plan alimentar pe 2 săptămâni, gătit la comun.** 19 rețete propuse în `comun/2_retete.md` (4 mic dejun, 3 gustări, 12 principale), fiecare cu porție **S** (Ema) și **M** (Adi) — diferă doar carnea și amidonul, legumele/sosul identice → o singură oală. Creat `comun/4_calendar.md`: cina de azi = prânzul de mâine (×4 porții), pește marți (cuptor) + miercuri (conservă), ouă alternate, chili ×8 cu jumătate la congelator. Meniuri: Ema ≈ 2105 kcal · P156/G61/C231 · fibre 42; Adi ≈ 2440 · P188/G72/C257 · fibre 46 (medii pe 14 zile, calculate din cantități). Presupus sală marți+joi. | comun/2_retete, comun/4_calendar, ema/4_meniu, adi/4_meniu |
| 2026-09-14 | **Corecție greutate Ema: 118 → 116 kg.** BMR ≈ 2010 · TDEE ≈ 2765. **Ținta rămâne 2200 kcal** (deficit ~565, tot în intervalul 500–650) → macro și meniul neschimbate. Actualizat exemplul din `wiki/calorii.md`. | ema/1_profil, ema/2_nutritie, ema/4_meniu, wiki |
| 2026-09-14 | **`comun/1_ingrediente.md` devine sursa unică de adevăr.** Tabel cu ~100 alimente (kcal, P, G, C, fibre per 100 g) din **USDA FoodData Central SR Legacy**, fiecare cu ID și link; regulă permanentă în CLAUDE.md: ingredient nou → întâi în tabel, apoi în rețetă. La verificare a ieșit că valorile de carne folosite înainte erau pentru carne **gătită** — recalculat tot pe crud (porțiile de carne au crescut ~40 g). **Rețetele refăcute pe farfuria 40/40/20**: proteină · legume (min. 3, la tavă / piure / salată) · amidon + sos; piureuri de legume (conopidă-morcov, broccoli-dovlecel), ratatouille, salate cu dressing de iaurt. American Gut Project: **40 plante/săpt.** Meniurile arată acum **cantitatea exactă a fiecărui ingredient** și caloriile calculate: Ema 2170 · P161/G67/C246; Adi 2440 · P188/G78/C264. | comun/1_ingrediente, comun/2_retete, comun/4_calendar, ema/4_meniu, adi/4_meniu, CLAUDE.md, 0_pipeline |
| 2026-09-14 | **Regula casei: fără lactate cu carne/pește, fără ouă cu carne în aceeași masă** (notată în CLAUDE.md, ambele `3_preferinte.md`, rețete, meniuri). Sosurile la carne refăcute fără iaurt: tahini-lămâie, lămâie-usturoi-ulei, vinegretă de muștar; piureurile cu ulei de măsline; scoase telemeaua și parmezanul din felurile cu carne; avocado peste chili. **Recalculat tot**: Ema 2160 · P155/G70/C245 · fibre 42; Adi 2430 · P182/G80/C263 · fibre 45; 41 plante/săpt. **Regulă permanentă în CLAUDE.md:** profilul e sursa de adevăr pentru nevoi → la orice schimbare se recalculează și se regenerează. Creat **`date/`** (baza de ingrediente USDA, rețetele cu cantități, generatorul de fișiere, zip-ul USDA) — copie a scratchpad-ului, acum în repo. | CLAUDE.md, date/, comun/2_retete, ema+adi/3_preferinte, ema+adi/4_meniu |
| 2026-09-14 | **Fișier nou de vizualizare rapidă a meniului**, pentru fiecare: `ema/4b_meniu_zilnic.md`, `adi/4b_meniu_zilnic.md` — aceleași rețete și cantități din `4_meniu.md`, dar o zi sub alta, cu ingredientele pe rânduri separate (nu în tabel), fără calorii/macro. Doar de citit rapid pe telefon. Generate din `date/genereaza.py` (funcție `menu_zilnic`). **Regulă permanentă (notată în CLAUDE.md §3):** `4_meniu.md` și `4b_meniu_zilnic.md` descriu același meniu și se regenerează mereu împreună — orice schimbare la meniul cuiva înseamnă rulare de `genereaza.py`, niciodată editare manuală a unuia singur. | date/genereaza.py, date/README.md, comun/0_pipeline, CLAUDE.md, ema+adi/4b_meniu_zilnic (noi) |
| 2026-09-14 | **Carnea și peștele restrânse la ce gătesc ei:** pui, porc (mușchi, cotlet; ceafă rar), vită · chefal, păstrăv, doradă, ton, somon rar. Scoase din bază și rețete: curcan, sardine, macrou, cod, creveți. Rețete: chili → **piept de pui tocat**; „curcan cu piure" → **mușchi de porc la grătar**; somon → **doradă la cuptor** (USDA n-are doradă → sea bass ca proxy, notat); salată de sardine → **salată de ton**. Calendar reordonat ca să rămână max. 2 feluri de carne roșie/săpt. Recalculat: Ema 2150 · P158/G67/C246; Adi 2420 · P186/G76/C263; 40 plante/săpt. `4_calendar.md` se generează acum din `date/`. `copiaza.cmd` nu mai copiază `date/` și e urmărit de git. | date/, comun/*, ema+adi/3_preferinte, ema+adi/4_meniu, copiaza.cmd |
