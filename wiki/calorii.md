# 🔢 Cum se calculează caloriile: BMR → TDEE → țintă

> Ghid de referință, valabil pentru oricine. Cifrele concrete ale fiecăruia stau în `1_profil.md` (calcul) și `2_nutritie.md` (ținte) din folderul lui.

Trei pași, în ordine:

1. **BMR** — cât arde corpul în repaus complet (dacă ai sta în pat toată ziua).
2. **TDEE** — BMR × factorul de activitate = cât consumi de fapt într-o zi obișnuită.
3. **Țintă** — TDEE ± deficit/surplus, în funcție de obiectiv.

---

## 1. BMR — formula Mifflin-St Jeor

Cea mai validată formulă pentru populația generală (Academy of Nutrition and Dietetics; Frankenfield 2005). Eroare tipică ±10%.

```
BMR = 10 × greutate (kg) + 6.25 × înălțime (cm) − 5 × vârstă (ani) + s
```

| Sex biologic | s |
|---|---:|
| Bărbat | **+5** |
| Femeie | **−161** |

**Exemple:**

- Bărbat, 108 kg, 192 cm, 32 ani: `10×108 + 6.25×192 − 5×32 + 5 = 1080 + 1200 − 160 + 5 = ` **2125 kcal**
- Femeie, 116 kg, 185 cm, 29 ani: `10×116 + 6.25×185 − 5×29 − 161 = 1160 + 1156 − 145 − 161 = ` **2010 kcal**

### De ce nu Harris-Benedict?
Harris-Benedict (1919, revizuită 1984) e formula „clasică", dar supraestimează cu ~5% la persoanele de azi. Mifflin-St Jeor (1990) a fost calibrată pe populație modernă și bate mai bine realitatea, mai ales la supraponderali.

### Rafinare: Katch-McArdle
Când știm **procentul de grăsime** (măsurat, nu ghicit), e mai precisă formula pe masă slabă:

```
BMR = 370 + 21.6 × masa slabă (kg)
masa slabă = greutate × (1 − % grăsime / 100)
```

Contează la persoane cu multă grăsime: Mifflin numără toate kilogramele, dar grăsimea arde puține calorii, deci poate supraestima BMR-ul. Se folosește după ce avem talia, șoldul sau o măsurătoare de bioimpedanță.

---

## 2. TDEE — factorul de activitate

```
TDEE = BMR × factor
```

| Factor | Nivel | Când se aplică |
|---:|---|---|
| **1.2** | sedentar | fără sport, job la birou |
| **1.375** | ușor | 1–3 antrenamente/săpt., job la birou |
| **1.55** | moderat | 4–5 antrenamente/săpt., sau 1–3 + job în picioare |
| **1.725** | intens | 6–7 antrenamente/săpt., sau antrenament zilnic + job activ |
| **1.9** | foarte intens | 2 antrenamente/zi sau muncă fizică grea + sport |

**Exemplu:** 2 antrenamente/săpt., ~1h, job la birou → **1.375**.
- Bărbat cu BMR 2125 → TDEE ≈ **2920 kcal**
- Femeie cu BMR 2010 → TDEE ≈ **2765 kcal**

### Reguli de bun-simț la alegerea factorului
- **La dubiu, alege factorul mai mic.** Factorii supraestimează la persoane cu greutate mare și la începători (sesiunile sunt încă scurte/ușoare, iar restul zilei e de obicei sedentar).
- „Antrenament" înseamnă ~1h de efort real. Mersul pe jos zilnic intră la factor doar dacă e mult (>10.000 pași).
- Factorul nu e bătut în cuie: se verifică cu cântarul (vezi §4).

---

## 3. Ținta calorică — deficit sau surplus

```
Țintă = TDEE − deficit    (slăbit)
Țintă = TDEE              (menținere)
Țintă = TDEE + surplus    (masă musculară)
```

| Obiectiv | Ajustare | Ritm așteptat |
|---|---|---|
| **Slăbit** | −500 … −700 kcal/zi | 0,5–0,7 kg/săpt. |
| **Menținere** | 0 | — |
| **Masă musculară** | +200 … +300 kcal/zi | 0,25–0,5 kg/lună (începători pot mai mult) |

1 kg de grăsime ≈ **7700 kcal**, deci un deficit de 550 kcal/zi ≈ 0,5 kg/săpt.

### Limite de siguranță
- **Nu sub BMR** pe termen lung — corpul reacționează cu oboseală, foame greu de controlat și pierdere de mușchi.
- Deficit peste ~1000 kcal/zi doar sub supraveghere medicală.
- La persoane cu multă grăsime, deficitul poate fi la limita de sus (~700) fără probleme; pe măsură ce greutatea scade, deficitul se micșorează.
- Proteina se dimensionează pe **greutatea-țintă / masa slabă**, nu pe greutatea actuală (altfel iese exagerat la persoane grele): ~1,6–2,2 g/kg greutate-țintă.

---

## 4. Recalibrarea după cântar

Toate formulele sunt estimări. Adevărul e trendul cântarului:

1. Cântărire zilnic dimineața, după toaletă, înainte de mâncare. Se compară **media pe săptămână**, nu ziua cu ziua (apa variază cu ±1–2 kg).
2. După **2–3 săptămâni**:
   - scade cu ritmul dorit → nu schimba nimic;
   - scade prea încet sau deloc → **−150 kcal**;
   - scade prea repede (>1 kg/săpt. după prima săptămână) → **+150 kcal**.
3. Prima săptămână de deficit pierzi mai mult (apă + glicogen) — nu e grăsime, nu te bucura și nu ajusta încă.
4. Recalculează BMR/TDEE la fiecare **5 kg** pierdute sau când se schimbă activitatea.
