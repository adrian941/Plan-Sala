# 🔄 Pipeline-ul de planificare culinară (Ema + Adi)

> **Acesta este procesul oficial de lucru pe partea de mâncare.** Stabilit de utilizator (2026-09-10).
> Bucătăria e comună (Ema și Adi gătesc împreună), dar **țintele nutriționale sunt individuale**.
> Regulile de fond și persona: [CLAUDE.md](../CLAUDE.md) · Indexul viu: [Gym-Rules.md](../Gym-Rules.md)

---

## Schema

```
   PASUL 1                    PASUL 2                     PASUL 3
┌────────────────┐        ┌─────────────────┐        ┌──────────────────┐
│ INGREDIENTE    │        │ REȚETE          │        │ CUMPĂRĂTURI      │
│ + preferințe   │  ───▶  │ (farfurii)      │  ───▶  │ listă pe magazine│
│ + ținte macro  │        │ + verdicte/pers.│        │ + cantități      │
│   & fibre      │        │ + meniu săptăm. │        │                  │
│  (per persoană)│        │  (per persoană) │        │   (comună)       │
└────────────────┘        └─────────────────┘        └──────────────────┘
 comun/1_ingrediente       comun/2_retete             comun/3_cumparaturi
 ema|adi/1_profil          comun/retete/*.md
 ema|adi/2_nutritie        ema|adi/3_plan-mese
```

Regula de aur: **nu sari peste pași.** Nimic nu ajunge în lista de cumpărături dacă nu provine dintr-o rețetă programată în meniu, iar nicio rețetă nu intră în meniu dacă folosește ingrediente respinse la Pasul 1.

---

## PASUL 1 — Ingrediente & nevoi nutriționale

**Fișiere:** [`1_ingrediente.md`](./1_ingrediente.md) · [`ema/1_profil.md`](../ema/1_profil.md) + [`ema/2_nutritie.md`](../ema/2_nutritie.md) · [`adi/1_profil.md`](../adi/1_profil.md) + [`adi/2_nutritie.md`](../adi/2_nutritie.md)

**Intrare:** date reale despre fiecare persoană (vârstă, sex, înălțime, greutate, activitate, obiectiv, medical) + preferințe alimentare și culinare.

**Ieșire:**
1. **Bazinul de ingrediente permise**, pe categorii, cu **verdict separat pentru Ema și pentru Adi**.
2. **Țintele zilnice per persoană**: kcal, proteine, grăsimi, carbohidrați, **fibre**.

**Legenda verdictelor** (folosită identic în toate fișierele):

| Simbol | Sens | Efect în pipeline |
|:------:|------|-------------------|
| ⭐ | favorit | prioritizat în meniu |
| ✅ | îi place | folosibil liber |
| 🟡 | neutru / o mănâncă | folosibil, dar nu repetat des |
| ❌ | nu-i place | **exclus** din meniul acelei persoane |
| ⛔ | nu poate (alergie/intoleranță/medical) | **exclus total, fără excepții** |
| ❔ | netestat | candidat de testat |

**Regula pentru gătitul comun:** o rețetă se gătește împreună doar dacă **niciunul** dintre ei nu are ❌ sau ⛔ pe ingredientele-cheie. Dacă unul are ❌ pe un ingredient *secundar*, se rezolvă prin **variantă „la farfurie"** (ex. brânza se adaugă doar în porția Emei) — se notează explicit în fișa rețetei.

---

## PASUL 2 — Farfurii / rețete

**Fișiere:** [`2_retete.md`](./2_retete.md) (index) · [`retete/`](./retete/) (o fișă per rețetă) · [`ema/3_plan-mese.md`](../ema/3_plan-mese.md) + [`adi/3_plan-mese.md`](../adi/3_plan-mese.md) (meniul săptămânal, per persoană)

**Cum funcționează, concret:**

> **Tu îmi dai rețete noi, cu detalii + cui îi place și cui nu. Eu le adaug în listele specializate.**

La fiecare rețetă nouă pe care mi-o dai, eu fac automat următoarele, fără să mai întreb:

1. Creez fișa în `comun/retete/<nume-reteta>.md` după [`retete/_sablon.md`](./retete/_sablon.md).
2. Calculez **macro + fibre per porție** (și pe 100 g unde ajută).
3. Notez **verdictul Ema** și **verdictul Adi** (din ce îmi spui tu).
4. O trec în indexul din [`2_retete.md`](./2_retete.md), cu tag-uri (masă, timp, tip proteină, meal-prep da/nu).
5. Actualizez [`1_ingrediente.md`](./1_ingrediente.md) dacă apar **ingrediente noi** sau dacă rețeta îmi dezvăluie o **preferință nouă** (ex. „Adi urăște vinetele" → ❌ la vinete, în toate rețetele care le conțin).
6. Semnalez dacă rețeta **nu se încadrează** în țintele cuiva (ex. prea multă grăsime pentru Ema) și propun ajustarea porției sau a ingredientelor.

**Ce detalii îmi sunt utile** când îmi dai o rețetă (dă-mi ce ai, completez eu restul):
ingrediente + cantități · mod de preparare · timp · nr. porții · cui îi place / cui nu · când se mănâncă (mic dejun/prânz/cină/gustare) · se pretează la meal prep?

**Ieșire:** meniu săptămânal per persoană — aceleași rețete de bază, **porții diferite** ca să nimerească țintele fiecăruia.

---

## PASUL 3 — Lista de cumpărături

**Fișier:** [`3_cumparaturi.md`](./3_cumparaturi.md)

**Intrare:** meniurile săptămânale ale ambilor (Pasul 2) × numărul de porții.

**Algoritm:**
1. Explodez fiecare rețetă programată în ingrediente × porții.
2. **Agreg** cantitățile identice între rețete și între cele două persoane (un singur rând „piept de pui — 1,4 kg", nu cinci).
3. Convertesc în **unități de cumpărat**, nu de gătit (kg, buc., pachet, conservă) — cu rotunjire în sus la ambalajul real.
4. Scad ce există deja în casă (stoc / staples).
5. Grupez **pe magazin**, apoi pe raion/categorie.
6. Marchez perisabilele vs. ce se poate cumpăra în avans.

**Blocant curent:** lipsesc magazinele disponibile + ce se găsește în fiecare. Fără ele, lista iese doar pe categorii, nu pe magazine.

---

## Reguli de consistență (le respect eu, automat)

- **O singură sursă per informație.** Ingredientele și preferințele trăiesc doar în `1_ingrediente.md`. Rețetele doar în `retete/`. Nu duplic.
- **Preferințele se propagă înapoi.** Orice „nu-mi place X" descoperit la Pasul 2 se scrie la Pasul 1 și re-filtrează automat tot ce urmează.
- **Fiecare modificare se notează** în jurnalul din [Gym-Rules.md](../Gym-Rules.md).
- **Fibrele sunt macro de rang egal** în acest proiect: apar în ținte, în fișele de rețetă și în verificarea meniului — nu doar ca notă de subsol.
