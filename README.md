# Plan Sala & Nutriție

Planuri personalizate de antrenament, nutriție și sănătate. **Mâncarea și cumpărăturile se fac la comun**, în funcție de preferințele și nevoile fiecărei persoane.

## 📌 Start aici

- **[CLAUDE.md](./CLAUDE.md)** — constituția proiectului (rol, metodă, reguli de arhitectură). Fișier stabil.
- **[Gym-Rules.md](./Gym-Rules.md)** — planul VIU, se updatează iterativ și linkează modular.
- **[comun/0_pipeline.md](./comun/0_pipeline.md)** — procesul culinar în 3 pași.
- **[persoane/README.md](./persoane/README.md)** — cine e în plan și cum adaugi pe cineva.

## Pipeline culinar

```
1. Ingrediente + preferințe + ținte macro/fibre  →  2. Rețete  →  3. Listă de cumpărături
   catalog comun + filtre per persoană              fișe comune    agregată peste toți
```

## Arhitectură

Două domenii, separate strict:

| Folder | Conține | Regula |
|--------|---------|--------|
| `comun/` | alimente, rețete, generatorul de cumpărături | **neutru** — niciun nume de persoană |
| `persoane/` | profil, ținte, preferințe, meniu — un folder per om | **excepții** — se scrie doar ce iese din normal |

O persoană nouă = `cp -r persoane/_sablon persoane/<nume>`, **zero modificări în `comun/`**.

## Structură

```
CLAUDE.md        ← reguli stabile
Gym-Rules.md     ← index-master viu
comun/           ← catalog ingrediente, rețete, cumpărături, liste generate
persoane/        ← _sablon/ + un folder per persoană (ema/, …)
```
