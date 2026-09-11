# 🔄 Cum lucrăm la mâncare — cei 3 pași

> Regula casei pe partea de mâncare. Se gătește și se cumpără **la comun**, dar fiecare are nevoile lui.
> Regulile de fond: [CLAUDE.md](../CLAUDE.md) · Ce e la zi: [Gym-Rules.md](../Gym-Rules.md)

---

## Pasul 1 — Ce mâncăm și de ce are nevoie fiecare

Două lucruri separate:

**Lista de alimente** — [`1_ingrediente.md`](./1_ingrediente.md). Ce se poate mânca, pe categorii, cu cât are fiecare fibre. E o listă despre *mâncare*, nu despre oameni: nu scrie nimeni în ea cui îi place ce.

**Ce vrea și ce-i trebuie fiecăruia** — în folderul lui:

| Fișier | Ce conține |
|--------|-----------|
| `1_profil.md` | vârstă, greutate, activitate, obiectiv, sănătate |
| `2_nutritie.md` | de câte calorii, proteine, grăsimi, carbohidrați și **fibre** are nevoie pe zi |
| `3_preferinte.md` | ce-i place, ce nu-i place, ce nu poate mânca |

**Preferințele se scriu scurt: doar ce iese din tipar.** Dacă un aliment nu apare în `3_preferinte.md`, se înțelege că e ok. Nu bifăm 200 de alimente pentru fiecare om.

| Semn | Sens | Ce înseamnă la gătit |
|:----:|------|----------------------|
| ⭐ | favorit | îl punem des |
| ❌ | nu-i place | nu apare în meniul lui |
| ⛔ | nu poate (alergie, medical) | **nu apare nicăieri, fără excepții** |
| 🟡 | îl mănâncă, dar nu des | cu măsură |
| ❔ | n-am testat | de încercat |

**Când unuia nu-i place ceva:** dacă e un ingredient de care rețeta nu depinde (brânza de deasupra, măslinele), nu renunțăm la rețetă — se pune doar în farfuria cui îl vrea. Se notează în rețetă.

---

## Pasul 2 — Rețetele

**Tu îmi dai rețete, cu ce detalii ai și cu „ăstuia îi place, ăluia nu". Eu le pun la locul lor.**

Ce fac de fiecare dată, fără să mai întreb:

1. Scriu rețeta în [`2_retete.md`](./2_retete.md) — ingrediente, preparare, timp, porții.
2. Calculez **calorii, proteine, grăsimi, carbohidrați și fibre pe porție**.
3. Marchez ingredientele de care se poate renunța (pentru „doar în farfuria lui").
4. Trec verdictele în `ema/3_preferinte.md` și `adi/3_preferinte.md`.
5. Adaug în lista de alimente ce ingrediente noi apar.
6. Îți spun dacă rețeta nu se încadrează în ce-i trebuie cuiva, și cu ce o ajustăm.

**Ce-mi ajută să știu:** ingrediente și cantități · cum se face · cât durează · câte porții ies · cui îi place și cui nu · la ce masă se mănâncă · ține la frigider câteva zile?

Apoi, **meniul săptămânal** se face separat pentru fiecare (`ema/4_meniu.md`, `adi/4_meniu.md`): de multe ori aceeași rețetă, dar **porții diferite**, fiindcă nevoile diferă.

---

## Pasul 3 — Cumpărăturile

[`3_cumparaturi.md`](./3_cumparaturi.md) — o singură listă, pentru amândoi.

Iau meniurile amândurora, adun ingredientele (o singură linie „piept de pui — 1,4 kg", nu cinci), le trec în cantități de cumpărat (kg, bucăți, pachete), scad ce e deja în casă și le grupez pe magazine.

**Îmi mai trebuie:** ce magazine aveți la îndemână și ce se găsește bun în fiecare. Până atunci lista iese grupată doar pe categorii.

---

## De ce e împărțit așa

**Ce ține de mâncare stă în `comun/`. Ce ține de un om stă în folderul lui.**

Lista de alimente și rețetele sunt aceleași indiferent cine mănâncă din ele — de asta nu au nume de oameni în ele. Ce se schimbă de la om la om (nevoi, gusturi, porții) stă la el. Așa, când completăm profilul lui Adi, nu trebuie rescrisă nicio rețetă.

**Ordinea contează:** nimic nu ajunge pe lista de cumpărături dacă nu vine dintr-o rețetă pusă în meniu, și nicio rețetă nu intră în meniul cuiva dacă are în ea ceva ce el nu poate mânca.

**Ce aflăm pe parcurs se scrie la sursă.** Dacă la o rețetă iese „Adi nu suportă vinetele", asta se scrie în preferințele lui — și de atunci înainte filtrează singură toate rețetele, nu doar pe aceea.
