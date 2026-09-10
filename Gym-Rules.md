# Gym-Rules.md — Planul VIU

> Acesta este documentul „viu": se updatează la fiecare sesiune de brainstorming.
> Regulile de fond și persona sunt în **[CLAUDE.md](./CLAUDE.md)** (fișier stabil).
> Procesul culinar în 3 pași + principiile de arhitectură: **[`comun/0_pipeline.md`](./comun/0_pipeline.md)**.
>
> **Status curent:** 🟡 Ema are profilul și țintele gata. Mâncarea și cumpărăturile sunt comune;
> **Adi se configurează ulterior** — arhitectura îl acceptă fără rescriere.

---

## 👥 Persoane

| Persoană | Folder | Scop | Status |
|----------|--------|------|--------|
| **Ema** | [`persoane/ema/`](./persoane/ema/) | plan complet (mâncare + sală + sănătate) | 🟡 în lucru |
| **Adi** | *(neconfigurat)* | doar mâncare — la comun cu Ema | ⚪ ulterior |

> Adăugarea unei persoane: [`persoane/README.md`](./persoane/README.md) — `cp -r persoane/_sablon persoane/<nume>`.

## 🔄 Pipeline culinar (comun, neutru)

| Pas | Fișier | Ce conține | Status |
|-----|--------|-----------|--------|
| Proces | [`comun/0_pipeline.md`](./comun/0_pipeline.md) | Cei 3 pași, legenda verdictelor, principiile de arhitectură | 🟢 |
| 1️⃣a Catalog ingrediente | [`comun/1_ingrediente.md`](./comun/1_ingrediente.md) | Alimente pe grupe, rol pe farfurie, fibre | 🟢 |
| 2️⃣a Rețete | [`comun/2_retete.md`](./comun/2_retete.md) · [`comun/retete/`](./comun/retete/) | Index derivat + fișe neutre cu macro/porție | ⚪ aștept prima rețetă |
| 3️⃣ Cumpărături | [`comun/3_cumparaturi.md`](./comun/3_cumparaturi.md) · [`comun/liste/`](./comun/liste/) | Generator + magazine → liste săptămânale | ⚪ blocat: lipsesc magazinele |

## 🧍 Module Ema

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| Profil & obiective | [`persoane/ema/1_profil.md`](./persoane/ema/1_profil.md) | Corp, activitate, medical, obiectiv | 🟡 lipsesc talie/șold, job, somn, loc antrenament |
| Nutriție | [`persoane/ema/2_nutritie.md`](./persoane/ema/2_nutritie.md) | Ținte: kcal, macro, fibre | 🟢 2100 kcal · P150/G65/C230 · fibre 25–30 g |
| 1️⃣b Preferințe | [`persoane/ema/3_preferinte.md`](./persoane/ema/3_preferinte.md) | Favorite, restricții, frecvențe, verdicte rețete | 🟡 lipsesc preferințele culinare (metode, condimentare) |
| 2️⃣b Meniu | [`persoane/ema/4_meniu.md`](./persoane/ema/4_meniu.md) | Meniu săptămânal + porții | ⚪ după rețete |
| Sală | [`persoane/ema/5_sala.md`](./persoane/ema/5_sala.md) | Split, exerciții, progresie | ⚪ blocat: unde antrenează |
| Sănătate | [`persoane/ema/6_sanatate.md`](./persoane/ema/6_sanatate.md) | Somn, stres, mobilitate, monitorizare | ⚪ după profil |

Legendă: 🟢 stabil · 🟡 în lucru · ⚪ neînceput · 🔴 blocat

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

1. **Ingrediente + preferințe + ținte macro/fibre.** ⬅️ *suntem aici* — catalogul e gata, Ema e configurată; Adi urmează.
2. **Rețete / farfurii** — utilizatorul dă rețete cu detalii + cui îi place; eu le fișez, le calculez macro și le indexez.
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
| 2026-09-10 | **Stabilit pipeline-ul culinar în 3 pași** (ingrediente+preferințe+macro/fibre → rețete → cumpărături). Creat `comun/` cu `0_pipeline.md`, `1_ingrediente.md` (mutat din `ema/7_alimente.md`), `2_retete.md` + `retete/_sablon.md`, `3_cumparaturi.md` (mutat din `ema/6_cumparaturi.md`). Fibrele promovate la macro de rang egal. | toate |
| 2026-09-10 | **Refactor de arhitectură — modular, extensibil la N persoane.** Prima variantă avea preferințele ca *coloane per persoană* în fișierele comune (catalog, fișe de rețetă): adăugarea unui om cerea editarea tuturor fișierelor comune. Normalizat: `comun/` devine complet **neutru** (catalog de fapte + fișe de rețetă fără nume), iar preferințele trec în `persoane/<x>/3_preferinte.md` ca **excepții** (implicit ✅). Introduse `persoane/` cu `_sablon/` (o persoană = `cp -r`), `comun/liste/` pentru listele generate, ingrediente marcabile drept *opționale* (variante „la farfurie"), indexul de rețete marcat ca **vedere derivată**. Șterse scheletele goale `adi/` — se creează din șablon când vine configurarea. Cele 4 reguli de arhitectură scrise în CLAUDE.md §2.1. | toate |
