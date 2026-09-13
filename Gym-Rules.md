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
| 1️⃣ Alimente | [`comun/1_ingrediente.md`](./comun/1_ingrediente.md) | Lista pe categorii, rol pe farfurie, fibre | 🟢 |
| 2️⃣ Rețete | [`comun/2_retete.md`](./comun/2_retete.md) | Rețetele + ce iese pe porție | ⚪ aștept prima rețetă |
| 3️⃣ Cumpărături | [`comun/3_cumparaturi.md`](./comun/3_cumparaturi.md) | Lista + magazinele | ⚪ blocat: lipsesc magazinele |

## 🧍 Ema

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| Profil & obiective | [`ema/1_profil.md`](./ema/1_profil.md) | Date, activitate, sănătate, obiectiv | 🟡 lipsesc talie/șold, job, somn, loc antrenament |
| Nutriție | [`ema/2_nutritie.md`](./ema/2_nutritie.md) | Calorii, macro, fibre | 🟢 2100 kcal · P150/G65/C230 · fibre 25–30 g |
| Preferințe | [`ema/3_preferinte.md`](./ema/3_preferinte.md) | Ce-i place, ce nu, frecvențe | 🟡 lipsesc preferințele culinare (metode, condimentare) |
| Meniu | [`ema/4_meniu.md`](./ema/4_meniu.md) | Meniul săptămânal + porții | ⚪ după rețete |
| Sală | [`ema/5_sala.md`](./ema/5_sala.md) | Split, exerciții, progresie | ⚪ blocat: unde antrenează |
| Sănătate | [`ema/6_sanatate.md`](./ema/6_sanatate.md) | Somn, stres, mobilitate, monitorizare | ⚪ după profil |

## 🧍 Adi (doar mâncare)

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| Profil | [`adi/1_profil.md`](./adi/1_profil.md) | Datele de care am nevoie | 🔴 gol |
| Nutriție | [`adi/2_nutritie.md`](./adi/2_nutritie.md) | Calorii, macro, fibre | 🔴 blocat de profil |
| Preferințe | [`adi/3_preferinte.md`](./adi/3_preferinte.md) | Ce-i place, ce nu, ce nu poate | 🔴 gol |
| Meniu | [`adi/4_meniu.md`](./adi/4_meniu.md) | Meniul săptămânal + porții | ⚪ după rețete |

Legendă: 🟢 stabil · 🟡 în lucru · ⚪ neînceput · 🔴 blocat

## 📚 Wiki — ghiduri generale de antrenament

| Fișier | Ce conține | Status |
|--------|-----------|--------|
| [`wiki/fesieri.md`](./wiki/fesieri.md) | Anatomie + exerciții pentru izolarea fesierilor fără hipertrofierea picioarelor | 🟢 |

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

1. **Alimente + preferințe + ținte (calorii, macro, fibre).** ⬅️ *suntem aici* — lista de alimente e gata, Ema e completă; Adi urmează.
2. **Rețete** — utilizatorul dă rețete cu detalii + cui îi place; eu le scriu, le calculez pe porție și le trec în cuprins.
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
