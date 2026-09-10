# 🛒 Cumpărături

> **Pasul 3** din [pipeline](./0_pipeline.md). Aici stau **generatorul** și **configurația de magazine**.
> Listele efective, săptămână de săptămână, sunt în [`liste/`](./liste/) — sunt rezultate, nu configurație.

## Generatorul

**Intrare:** meniurile săptămânale ale **tuturor persoanelor active** (`persoane/*/4_meniu.md`) × porții.

1. Fiecare rețetă programată se explodează în ingrediente × porții.
2. Cantitățile identice se **agregă peste toate persoanele și toate rețetele** (un singur rând „piept de pui — 1,4 kg").
3. Se convertesc în **unități de cumpărat** (kg, buc., pachet, conservă), rotunjite la ambalajul real.
4. Se scade ce e deja în casă (stoc / staples).
5. Se grupează pe **magazin**, apoi pe raion.
6. Se marchează perisabilele (🥬 proaspăt) vs. ce se ia în avans (📦).

> Algoritmul nu cunoaște nume de persoane — merge peste câte foldere există în `persoane/`.
> Adăugarea cuiva nu cere nicio modificare aici.

## Magazine disponibile

> ⚠️ **Blocant.** Am nevoie de: ce magazine aveți la îndemână + ce se găsește bun/ieftin în fiecare.
> Până atunci, listele ies grupate doar pe categorii.

| Magazin | Ce luăm de aici | Observații |
|---------|-----------------|------------|
| ⟨…⟩ | ⟨…⟩ | |

## Listă „staples" (mereu în casă)

*(Se completează după primele rețete — ce apare în ≥3 rețete devine staple.)*

| Produs | Cantitate de siguranță | Magazin |
|--------|------------------------|---------|
| ⟨…⟩ | | |

## Liste săptămânale

| Săptămână | Fișier |
|-----------|--------|
| *(niciuna încă)* | |
