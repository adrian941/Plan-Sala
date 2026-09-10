# 👥 Persoane

Fiecare persoană din plan are **un folder propriu**, cu aceeași structură. Tot ce e individual stă aici; tot ce e comun (catalog de ingrediente, rețete, cumpărături) stă în [`comun/`](../comun/).

## Persoane active

| Persoană | Folder | Scop | Status |
|----------|--------|------|--------|
| **Ema** | [`ema/`](./ema/) | plan complet (mâncare + sală + sănătate) | 🟡 în lucru |
| **Adi** | *(neconfigurat)* | doar mâncare — gătesc și cumpără la comun cu Ema | ⚪ se configurează ulterior |

## Cum adaugi o persoană nouă

```bash
cp -r persoane/_sablon persoane/<nume>
```

Apoi:
1. Completezi `1_profil.md` → de aici ies țintele.
2. Se calculează `2_nutritie.md` (kcal, macro, fibre).
3. Se notează `3_preferinte.md` — **doar excepțiile** față de catalog.
4. Se adaugă rândul în tabelul „Persoane active" de mai sus și în [`Gym-Rules.md`](../Gym-Rules.md).
5. Fișierele `5_sala.md` / `6_sanatate.md` se păstrează **doar dacă persoana e în scop și pe partea de antrenament**; altfel se șterg.

După ce ai terminat, rulează `python3 scripts/verifica.py` — confirmă că structura e completă și că nimic personal nu s-a scurs în fișierele comune.

**Nu trebuie modificat niciun fișier din `comun/`.** Dacă adăugarea unei persoane te obligă să editezi catalogul, rețetele sau pipeline-ul, arhitectura e greșită — vezi [`comun/0_pipeline.md`](../comun/0_pipeline.md#principii-de-arhitectură).

## Structura unui folder de persoană

| Fișier | Conține | Obligatoriu |
|--------|---------|:-----------:|
| `1_profil.md` | corp, activitate, medical, obiectiv | ✅ |
| `2_nutritie.md` | ținte: kcal, proteine, grăsimi, carbo, fibre | ✅ |
| `3_preferinte.md` | ce place / nu place / nu poate + verdicte pe rețete | ✅ |
| `4_meniu.md` | meniul săptămânal + porțiile proprii | ✅ |
| `5_sala.md` | programul de antrenament | opțional |
| `6_sanatate.md` | somn, stres, mobilitate, monitorizare | opțional |
