# Gym-Rules.md — Planul VIU (Ema: complet · Adi: bucătărie)

> Acesta este documentul „viu": se updatează la fiecare sesiune de brainstorming.
> Regulile de fond și persona sunt în **[CLAUDE.md](./CLAUDE.md)** (fișier stabil).
> Procesul culinar în 3 pași: **[`comun/0_pipeline.md`](./comun/0_pipeline.md)**.
>
> **Status curent:** 🟡 *Intake* — Ema are profilul și țintele gata; **lipsesc complet datele lui Adi**.

---

## Pipeline culinar — comun (Ema + Adi)

| Pas | Fișier | Ce conține | Status |
|-----|--------|-----------|--------|
| 🔄 Proces | [`comun/0_pipeline.md`](./comun/0_pipeline.md) | Definiția celor 3 pași + legenda verdictelor | 🟢 |
| 1️⃣ Ingrediente & preferințe | [`comun/1_ingrediente.md`](./comun/1_ingrediente.md) | Alimente pe categorii, verdicte Ema/Adi, lista de fibre | 🟡 Ema completă, Adi gol |
| 2️⃣ Rețete | [`comun/2_retete.md`](./comun/2_retete.md) · [`comun/retete/`](./comun/retete/) | Index + fișe cu macro/porție și verdicte | ⚪ aștept prima rețetă |
| 3️⃣ Cumpărături | [`comun/3_cumparaturi.md`](./comun/3_cumparaturi.md) | Listă pe magazine, generată din meniuri | ⚪ blocat: lipsesc magazinele |

## Module Ema

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| 🧍 Profil & obiective | [`ema/1_profil.md`](./ema/1_profil.md) | Date, analize, restricții, obiectiv | 🟡 lipsesc talie/șold, job, somn, loc antrenament |
| 🥗 Nutriție | [`ema/2_nutritie.md`](./ema/2_nutritie.md) | Calorii, macro, fibre, principii | 🟢 2100 kcal · P150/G65/C230 · fibre 25–30 g |
| 🍳 Plan mese | [`ema/3_plan-mese.md`](./ema/3_plan-mese.md) | Meniu săptămânal + porții | ⚪ după rețete |
| 🏋️ Sală / antrenament | [`ema/4_sala.md`](./ema/4_sala.md) | Split, exerciții, progresie | ⚪ blocat: unde antrenează |
| ❤️ Sănătate & recuperare | [`ema/5_sanatate.md`](./ema/5_sanatate.md) | Somn, stres, mobilitate, monitorizare | ⚪ după profil |

## Module Adi (doar bucătărie — vezi [CLAUDE.md §0](./CLAUDE.md))

| Modul | Fișier | Ce conține | Status |
|-------|--------|-----------|--------|
| 🧍 Profil | [`adi/1_profil.md`](./adi/1_profil.md) | Date necesare pentru ținte | 🔴 gol |
| 🥗 Nutriție | [`adi/2_nutritie.md`](./adi/2_nutritie.md) | Calorii, macro, fibre | 🔴 blocat de profil |
| 🍳 Plan mese | [`adi/3_plan-mese.md`](./adi/3_plan-mese.md) | Meniu săptămânal + porții | ⚪ după rețete |

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

1. **Ingrediente + preferințe + ținte macro/fibre**, pentru amândoi. ⬅️ *suntem aici* — Ema e gata, **Adi e blocat: lipsesc datele lui**.
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
| 2026-09-10 | **Stabilit pipeline-ul culinar în 3 pași** (ingrediente+preferințe+macro/fibre → rețete → cumpărături). Creat `comun/` cu `0_pipeline.md`, `1_ingrediente.md` (mutat din `ema/7_alimente.md`, cu coloane de verdict Ema/Adi), `2_retete.md` + `retete/_sablon.md`, `3_cumparaturi.md` (mutat din `ema/6_cumparaturi.md`). **Adi reintrodus în scop, doar pe bucătărie** — creat `adi/1-3`. Fibrele promovate la macro de rang egal. Actualizate CLAUDE.md (§0, §2.1 nou, §3) și README. | toate |
