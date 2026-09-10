# 🔄 Pipeline-ul de planificare culinară

> **Procesul oficial de lucru pe partea de mâncare.** Stabilit de utilizator (2026-09-10).
> Bucătăria e comună — se gătește și se cumpără împreună — dar **țintele și preferințele sunt individuale**.
> Regulile de fond și persona: [CLAUDE.md](../CLAUDE.md) · Indexul viu: [Gym-Rules.md](../Gym-Rules.md)

---

## Schema

```
       PASUL 1                      PASUL 2                    PASUL 3
┌──────────────────────┐     ┌────────────────────┐     ┌──────────────────┐
│ 1a CATALOG (comun)   │     │ 2a REȚETE (comune) │     │ 3 CUMPĂRĂTURI    │
│    ingrediente       │────▶│    fișe neutre     │────▶│   agregare peste │
│    neutre, fapte     │     │    macro/porție    │     │   toate meniurile│
├──────────────────────┤     ├────────────────────┤     │   → liste/       │
│ 1b PER PERSOANĂ      │     │ 2b PER PERSOANĂ    │     │      (comună)    │
│    profil → ținte    │────▶│    meniu + porții  │────▶│                  │
│    + preferințe      │     │    + verdicte      │     │                  │
└──────────────────────┘     └────────────────────┘     └──────────────────┘
 comun/1_ingrediente.md       comun/2_retete.md          comun/3_cumparaturi.md
 persoane/<x>/1_profil.md     comun/retete/*.md          comun/liste/*.md
 persoane/<x>/2_nutritie.md   persoane/<x>/4_meniu.md
 persoane/<x>/3_preferinte.md
```

**Regula de aur:** nu sari peste pași. Nimic nu ajunge în lista de cumpărături dacă nu vine dintr-o rețetă programată într-un meniu, și nicio rețetă nu intră în meniul cuiva dacă îi încalcă restricțiile.

---

## Principii de arhitectură

Structura respectă patru reguli. Dacă o modificare le încalcă, modificarea e greșită.

**1. Comunul e neutru.** Nimic din `comun/` nu conține nume de persoane: nici catalogul, nici fișele de rețetă, nici generatorul de cumpărături. Ele descriu *alimente și preparate*, nu *oameni*.

**2. Preferințele sunt excepții, nu enumerări.** Fiecare persoană declară doar ce iese din normal: ⭐ favorit, ❌ nu-i place, ⛔ nu poate. Tot restul catalogului e implicit acceptat. Consecință: nu trebuie bifat fiecare aliment pentru fiecare om.

**3. O persoană = un folder.** Adăugarea cuiva înseamnă `cp -r persoane/_sablon persoane/<nume>` și zero modificări în `comun/`. Dacă adăugarea unei persoane te obligă să editezi un fișier comun, arhitectura s-a stricat.

**4. Vederile derivate sunt marcate ca atare.** Indexul de rețete are coloane per persoană — dar e o *proiecție* regenerabilă, nu sursa de adevăr. Se editează la sursă (`persoane/<x>/3_preferinte.md`), se regenerează în index.

---

## PASUL 1 — Ingrediente & nevoi nutriționale

### 1a. Catalogul comun — [`1_ingrediente.md`](./1_ingrediente.md)
Fapte despre alimente: grupă, rol pe farfurie (P/L/A/G/F), conținut de fibre. Neutru, nu se schimbă când apare o persoană nouă.

### 1b. Partea individuală — `persoane/<nume>/`
| Fișier | Ce produce |
|--------|-----------|
| `1_profil.md` | date de corp, activitate, medical, obiectiv |
| `2_nutritie.md` | **ținte zilnice**: kcal, proteine, grăsimi, carbohidrați, **fibre** |
| `3_preferinte.md` | **filtrul**: ⭐ favorite, ❌ ce nu-i place, ⛔ restricții, reguli de frecvență, preferințe culinare |

**Legenda verdictelor** (aceeași peste tot):

| Simbol | Sens | Efect în pipeline |
|:------:|------|-------------------|
| ⭐ | favorit | prioritizat în meniu |
| ✅ | îi place | folosibil liber — **implicit pentru tot ce nu e listat** |
| 🟡 | tolerat | folosibil, dar nu repetat des |
| ❌ | nu-i place | **exclus** din meniul acelei persoane |
| ⛔ | nu poate (alergie/medical) | **exclus total, fără excepții** |
| ❔ | netestat | candidat de testat |

**Regula pentru gătitul comun:** o rețetă se gătește împreună dacă **niciunul** dintre cei care o mănâncă nu are ❌/⛔ pe un ingredient **neopțional**. Dacă problema e pe un ingredient marcat *opțional* în fișă, se rezolvă prin **variantă „la farfurie"** (se adaugă doar în porțiile care îl vor) — descrisă în fișă prin ingredient, nu prin nume.

---

## PASUL 2 — Farfurii / rețete

### 2a. Rețetele comune — [`2_retete.md`](./2_retete.md) + [`retete/`](./retete/)

> **Tu îmi dai rețete noi, cu detalii + cui îi place și cui nu. Eu le adaug în listele specializate.**

La fiecare rețetă nouă fac automat, fără să mai întreb:

1. Creez fișa **neutră** în `retete/<nume-reteta>.md` după [`retete/_sablon.md`](./retete/_sablon.md).
2. Calculez **macro + fibre per porție** (și pe 100 g unde ajută).
3. Marchez ce ingrediente sunt **opționale** (cele care permit varianta „la farfurie").
4. Scriu verdictele în `persoane/<nume>/3_preferinte.md`, la fiecare persoană în parte.
5. Regenerez rândul din indexul [`2_retete.md`](./2_retete.md).
6. Actualizez catalogul [`1_ingrediente.md`](./1_ingrediente.md) dacă apar **ingrediente noi**.
7. Semnalez dacă rețeta **nu încape** în țintele cuiva și propun ajustarea porției sau a ingredientelor.

**Ce detalii îmi sunt utile** (dă-mi ce ai, completez eu restul):
ingrediente + cantități · mod de preparare · timp · nr. porții · cui îi place / cui nu · când se mănâncă · se pretează la meal prep?

### 2b. Meniul individual — `persoane/<nume>/4_meniu.md`
Aceleași rețete de bază, **porții diferite**, ca să nimerească țintele fiecăruia. Aici se aplică filtrul din `3_preferinte.md`.

---

## PASUL 3 — Lista de cumpărături

**Generator + magazine:** [`3_cumparaturi.md`](./3_cumparaturi.md) · **Listele efective:** [`liste/`](./liste/)

Explodează rețetele din toate meniurile în ingrediente × porții, **agregă peste toate persoanele**, convertește în unități de cumpărat, scade stocul, grupează pe magazin. Generatorul nu cunoaște nume — merge peste câte foldere există în `persoane/`.

**Blocant curent:** lipsesc magazinele + ce se găsește în fiecare. Fără ele, lista iese doar pe categorii.

---

## Cum adaug o persoană nouă

```bash
cp -r persoane/_sablon persoane/<nume>
```

1. Completez `1_profil.md` (vârstă, sex, înălțime, greutate, activitate, obiectiv, medical).
2. Calculez `2_nutritie.md` (Mifflin-St Jeor → TDEE → ținte + fibre).
3. Notez `3_preferinte.md` — **doar excepțiile**.
4. Adaug o coloană în indexul de rețete și rândul în [`persoane/README.md`](../persoane/README.md) + [`Gym-Rules.md`](../Gym-Rules.md).
5. Rețetele existente **nu se ating**; îi trec doar verdictele.

**Test de sănătate al arhitecturii:** dacă pașii de mai sus cer editarea unei fișe de rețetă sau a catalogului, ceva e greșit.

Verificare automată: `python3 scripts/verifica.py`

---

## Reguli de consistență (le respect eu, automat)

- **O singură sursă per informație.** Alimentele → catalog. Preferințele → folderul persoanei. Rețetele → `retete/`. Nu duplic.
- **Preferințele se propagă înapoi.** Orice „nu-mi place X" descoperit la Pasul 2 se scrie la Pasul 1 (în `3_preferinte.md`) și re-filtrează automat tot ce urmează.
- **Fiecare modificare se notează** în jurnalul din [Gym-Rules.md](../Gym-Rules.md).
- **Fibrele sunt macro de rang egal**: apar în ținte, în fișele de rețetă și în verificarea meniului — nu ca notă de subsol.
