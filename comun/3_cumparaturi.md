# 🛒 Cumpărături — listă comună (Ema + Adi)

> **Pasul 3** din [pipeline](./0_pipeline.md). Se generează **automat** din meniurile săptămânale:
> [`ema/3_plan-mese.md`](../ema/3_plan-mese.md) + [`adi/3_plan-mese.md`](../adi/3_plan-mese.md).
> Nimic nu intră aici „de mână" — dacă un aliment apare în listă, el vine dintr-o rețetă programată.

## Cum se generează

1. Fiecare rețetă programată se explodează în ingrediente × porții.
2. Cantitățile identice se **agregă** între rețete și între cele două persoane.
3. Se convertesc în **unități de cumpărat** (kg, buc., pachet, conservă), rotunjite la ambalajul real.
4. Se scade ce e deja în casă (stoc / staples).
5. Se grupează pe **magazin**, apoi pe raion.
6. Se marchează perisabilele (🥬 cumpără proaspăt) vs. ce se ia în avans (📦).

## Magazine disponibile

> ⚠️ **Blocant.** Am nevoie de: ce magazine aveți la îndemână + ce se găsește bun/ieftin în fiecare.
> Până atunci, listele ies grupate doar pe categorii.

| Magazin | Ce luăm de aici | Observații |
|---------|-----------------|------------|
| ⟨…⟩ | ⟨…⟩ | |

## Listă „staples" (mereu în casă)
*(Se completează după ce avem primele rețete — ce se repetă în ≥3 rețete devine staple.)*

## Listă săptămânală curentă
*(Gol — se generează după ce există meniu la Pasul 2.)*

| ✓ | Produs | Cantitate | Magazin | Categorie | Perisabil |
|:-:|--------|----------:|---------|-----------|:---------:|
| | *(gol)* | | | | |
