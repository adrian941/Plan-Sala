# Gym-Rules.md — Planul VIU al Emei (sală + nutriție + sănătate)

> Acesta este documentul „viu": se updatează la fiecare sesiune de brainstorming.
> Regulile de fond și persona sunt în **[CLAUDE.md](./CLAUDE.md)** (fișier stabil).
>
> **Status curent:** 🟡 *Intake* — colectăm datele reale ale Emei. Vechile date sunt obsolete.

---

## Module (click pentru detalii)

### Ema (plan complet)

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| 🧍 Profil & obiective | [`ema/1_profil.md`](./ema/1_profil.md) | Date, analize, restricții, obiectiv | 🟡 în lucru |
| 🥗 Nutriție | [`ema/2_nutritie.md`](./ema/2_nutritie.md) | Calorii, macro, principii, suplimente | 🟡 calorii calculate |
| 🍳 Plan mese | [`ema/3_plan-mese.md`](./ema/3_plan-mese.md) | Meniuri, meal prep (rețetele: `comun/2_retete.md`) | ⚪ după nutriție |
| 🏋️ Sală / antrenament | [`ema/4_sala.md`](./ema/4_sala.md) | Split, exerciții, progresie | ⚪ după profil |
| ❤️ Sănătate & recuperare | [`ema/5_sanatate.md`](./ema/5_sanatate.md) | Somn, stres, mobilitate, monitorizare | ⚪ după profil |

### Comun (mâncare, pentru amândoi)

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| 🔄 Pipeline | [`comun/0_pipeline.md`](./comun/0_pipeline.md) | Cum lucrăm la mâncare, cei 3 pași | 🟢 |
| 🥦 Alimente | [`comun/1_ingrediente.md`](./comun/1_ingrediente.md) | Liste pe categorii + lista de fibre | 🟢 |
| 🍽️ Rețete | [`comun/2_retete.md`](./comun/2_retete.md) | Rețetele, cu ce iese pe porție | ⚪ *(gol — aștept prima rețetă)* |
| 🛒 Cumpărături | [`comun/3_cumparaturi.md`](./comun/3_cumparaturi.md) | Listă + magazine | ⚪ blocat pe magazine |

### Adi (de completat)

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| 🧍 Profil | [`adi/1_profil.md`](./adi/1_profil.md) | Date, activitate, sănătate, obiectiv | ⚪ șablon gol |
| 🥗 Nutriție | [`adi/2_nutritie.md`](./adi/2_nutritie.md) | Calorii, macro, fibre pe zi | ⚪ șablon gol |
| 🍽️ Preferințe | [`adi/3_preferinte.md`](./adi/3_preferinte.md) | Ce-i place, ce nu, ce nu poate | ⚪ șablon gol |
| 🍳 Meniu | [`adi/4_meniu.md`](./adi/4_meniu.md) | Meniul lui din rețetele comune | ⚪ șablon gol |

Legendă: 🟢 stabil · 🟡 în lucru · ⚪ neînceput

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

## Ordinea de lucru propusă

1. **Profil** — completăm `ema/profil.md` cu datele reale. ⬅️ *suntem aici*
2. **Nutriție** — calculăm ținte calorice/macro pe baza profilului.
3. **Plan mese** — transformăm țintele în meniuri și rețete reale.
4. **Sală** — construim programul de antrenament.
5. **Sănătate** — somn/stres/mobilitate/monitorizare.
6. **Cumpărături** — liste pe magazinele indicate de utilizator.

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
| 2026-09-12 | **Refăcute `comun/` și `adi/`** (la cererea utilizatorului) — restaurate din istoricul git dinainte de ștergere. `comun/1_ingrediente.md` e acum referința curentă pentru lista de alimente (include piersici, nectarine, portocale); `ema/7_alimente.md` rămâne ca istoric, nu se mai actualizează. `adi/` conține șabloanele goale, de completat. | structură, comun, adi |
