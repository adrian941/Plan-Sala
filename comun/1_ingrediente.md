# 🥦 Lista de alimente — sursa unică de adevăr pentru valori nutriționale

> **Pasul 1** din [cum lucrăm](./0_pipeline.md). **Toate calculele din rețete și meniuri pleacă din tabelul de mai jos** — nicio valoare nu se ia din altă parte.
>
> Aici nu scriem cui îi place ce. Gusturile fiecăruia stau la el: [`ema/3_preferinte.md`](../ema/3_preferinte.md), [`adi/3_preferinte.md`](../adi/3_preferinte.md).

## Regula

1. **Sursa:** [USDA FoodData Central](https://fdc.nal.usda.gov/) — baza de date oficială a Departamentului Agriculturii SUA (setul *SR Legacy*), referința standard folosită de aplicațiile de nutriție. Fiecare rând are ID-ul alimentului (căutabil pe site). Unde USDA nu are produsul (ex. lapte 1,5%, lapte de cocos light), se ia **eticheta producătorului** și se notează.

2. **Valorile sunt per 100 g de aliment crud / uscat** (carnea, peștele, orezul, pastele, lintea se cântăresc înainte de gătit). Excepții marcate: conservele (scurse), pâinea.

3. **Ingredient nou = rând nou aici, înainte să intre într-o rețetă.** Când apare o rețetă cu un ingredient care nu e în tabel, se caută în USDA și se adaugă.

4. Produsele românești de lactate (brânză de vaci, telemea, skyr) variază între producători — valoarea USDA e referința, dar dacă eticheta ta diferă mult, o folosim pe aceea.


**Rolul pe farfurie** (regula 40/40/20): `P` = proteină (40%) · `L` = legume / carbohidrați fibroși (40%) · `A` = amidon (20%) · `G` = grăsime (nu ocupă felie) · `F` = fruct


---


## 🥩 Carne & pește

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Piept de pui, fără piele, crud | P | 120 | 22.5 | 2.6 | 0 | 0 | [USDA 171077](https://fdc.nal.usda.gov/food-details/171077/nutrients) |  |
| Pulpă de pui dezosată, fără piele, crudă | P | 121 | 19.7 | 4.1 | 0 | 0 | [USDA 173627](https://fdc.nal.usda.gov/food-details/173627/nutrients) |  |
| Piept de pui tocat (acasă / la măcelar), crud | P | 120 | 22.5 | 2.6 | 0 | 0 | [USDA 171077](https://fdc.nal.usda.gov/food-details/171077/nutrients) | = piept de pui |
| Pui tocat comercial (cu pulpă), crud | P | 143 | 17.4 | 8.1 | 0 | 0 | [USDA 171116](https://fdc.nal.usda.gov/food-details/171116/nutrients) |  |
| Vită slabă (pulpă / mușchi, fără grăsime), crudă | P | 121 | 23.4 | 3 | 0 | 0 | [USDA 171762](https://fdc.nal.usda.gov/food-details/171762/nutrients) |  |
| Vită tocată 95% slabă, crudă | P | 137 | 21.4 | 5 | 0 | 0 | [USDA 171790](https://fdc.nal.usda.gov/food-details/171790/nutrients) |  |
| Cotlet de porc fără os, fără grăsime, crud | P | 127 | 22.4 | 3.4 | 0 | 0 | [USDA 168251](https://fdc.nal.usda.gov/food-details/168251/nutrients) |  |
| Mușchi de porc (tenderloin), crud | P | 109 | 21 | 2.2 | 0 | 0 | [USDA 168249](https://fdc.nal.usda.gov/food-details/168249/nutrients) |  |
| Ceafă de porc, fără grăsimea vizibilă, crudă | P | 132 | 18.7 | 5.7 | 0 | 0 | [USDA 168260](https://fdc.nal.usda.gov/food-details/168260/nutrients) | rar; cu grăsime e ~250 kcal |
| Somon de crescătorie, crud | P | 208 | 20.4 | 13.4 | 0 | 0 | [USDA 175167](https://fdc.nal.usda.gov/food-details/175167/nutrients) | pește gras ⭐ — mai rar |
| Doradă, crudă | P | 97 | 18.4 | 2 | 0 | 0 | [USDA 175142](https://fdc.nal.usda.gov/food-details/175142/nutrients) | USDA n-are doradă; valorile sunt de la sea bass (specie apropiată, ±10%) |
| Chefal, crud | P | 117 | 19.4 | 3.8 | 0 | 0 | [USDA 175123](https://fdc.nal.usda.gov/food-details/175123/nutrients) |  |
| Ton proaspăt, crud | P | 109 | 24.4 | 0.5 | 0 | 0 | [USDA 175159](https://fdc.nal.usda.gov/food-details/175159/nutrients) |  |
| Păstrăv curcubeu de crescătorie, crud | P | 141 | 19.9 | 6.2 | 0 | 0 | [USDA 173717](https://fdc.nal.usda.gov/food-details/173717/nutrients) | pește gras ⭐ |
| Ton conservă în apă, scurs | P | 116 | 25.5 | 0.8 | 0 | 0 | [USDA 171986](https://fdc.nal.usda.gov/food-details/171986/nutrients) |  |


## 🥚 Ouă

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Ou întreg, crud | P | 143 | 12.6 | 9.5 | 0.7 | 0 | [USDA 171287](https://fdc.nal.usda.gov/food-details/171287/nutrients) | 1 ou M ≈ 55 g → 79 kcal, 6,9 g P |
| Albuș, crud | P | 52 | 10.9 | 0.2 | 0.7 | 0 | [USDA 172183](https://fdc.nal.usda.gov/food-details/172183/nutrients) |  |


## 🥛 Lactate

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Skyr / iaurt grec 0% | P | 59 | 10.2 | 0.4 | 3.6 | 0 | [USDA 170894](https://fdc.nal.usda.gov/food-details/170894/nutrients) | USDA: Greek yogurt nonfat; skyr-ul din comerț e practic identic |
| Iaurt grec 2% | P | 73 | 10 | 1.9 | 3.9 | 0 | [USDA 170903](https://fdc.nal.usda.gov/food-details/170903/nutrients) |  |
| Iaurt simplu 1,5–2% | P | 63 | 5.3 | 1.6 | 7 | 0 | [USDA 170886](https://fdc.nal.usda.gov/food-details/170886/nutrients) |  |
| Brânză de vaci 2% (cottage) | P | 81 | 10.5 | 2.3 | 4.8 | 0 | [USDA 172182](https://fdc.nal.usda.gov/food-details/172182/nutrients) | brânza de vaci RO presată are de obicei mai multă proteină (13–16 g) — verifică eticheta |
| Brânză de vaci 4% | P | 98 | 11.1 | 4.3 | 3.4 | 0 | [USDA 172179](https://fdc.nal.usda.gov/food-details/172179/nutrients) |  |
| Kefir 1–2% | P | 43 | 3.8 | 1 | 4.8 | 0 | [USDA 170904](https://fdc.nal.usda.gov/food-details/170904/nutrients) |  |
| Lapte 1,5% | P | 46 | 3.3 | 1.5 | 4.8 | 0 | etichetă | USDA are doar 1% (42 kcal) și 2% (50 kcal); 1,5% = media |
| Lapte integral 3,5% | P | 61 | 3.2 | 3.3 | 4.8 | 0 | [USDA 172217](https://fdc.nal.usda.gov/food-details/172217/nutrients) |  |
| Telemea / feta | P | 265 | 14.2 | 21.5 | 3.9 | 0 | [USDA 173420](https://fdc.nal.usda.gov/food-details/173420/nutrients) |  |
| Mozzarella light (part skim) | P | 254 | 24.3 | 15.9 | 2.8 | 0 | [USDA 170847](https://fdc.nal.usda.gov/food-details/170847/nutrients) |  |
| Ricotta (part skim) | P | 138 | 11.4 | 7.9 | 5.1 | 0 | [USDA 171248](https://fdc.nal.usda.gov/food-details/171248/nutrients) |  |
| Parmezan ras | P | 420 | 28.4 | 27.8 | 13.9 | 0 | [USDA 171247](https://fdc.nal.usda.gov/food-details/171247/nutrients) |  |
| Cașcaval (tip cheddar) | P | 403 | 22.9 | 33.3 | 3.4 | 0 | [USDA 173414](https://fdc.nal.usda.gov/food-details/173414/nutrients) |  |


## 🥑 Grăsimi

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Unt | G | 717 | 0.9 | 81.1 | 0.1 | 0 | [USDA 173410](https://fdc.nal.usda.gov/food-details/173410/nutrients) |  |
| Ulei de măsline | G | 884 | 0 | 100 | 0 | 0 | [USDA 171413](https://fdc.nal.usda.gov/food-details/171413/nutrients) | 1 lingură ≈ 10 g |
| Avocado | G | 160 | 2 | 14.7 | 8.5 | 6.7 | [USDA 171705](https://fdc.nal.usda.gov/food-details/171705/nutrients) |  |
| Măsline | G | 116 | 0.8 | 10.9 | 6 | 1.6 | [USDA 169094](https://fdc.nal.usda.gov/food-details/169094/nutrients) |  |
| Nuci | G | 654 | 15.2 | 65.2 | 13.7 | 6.7 | [USDA 170187](https://fdc.nal.usda.gov/food-details/170187/nutrients) |  |
| Migdale | G | 579 | 21.2 | 49.9 | 21.6 | 12.5 | [USDA 170567](https://fdc.nal.usda.gov/food-details/170567/nutrients) |  |
| Caju | G | 553 | 18.2 | 43.9 | 30.2 | 3.3 | [USDA 170162](https://fdc.nal.usda.gov/food-details/170162/nutrients) |  |
| Alune de pădure | G | 628 | 15 | 60.8 | 16.7 | 9.7 | [USDA 170581](https://fdc.nal.usda.gov/food-details/170581/nutrients) |  |
| Semințe de chia | G | 486 | 16.5 | 30.7 | 42.1 | 34.4 | [USDA 170554](https://fdc.nal.usda.gov/food-details/170554/nutrients) |  |
| Semințe de in | G | 534 | 18.3 | 42.2 | 28.9 | 27.3 | [USDA 169414](https://fdc.nal.usda.gov/food-details/169414/nutrients) | măcinate, altfel nu se absorb |
| Semințe de dovleac | G | 559 | 30.2 | 49.1 | 10.7 | 6 | [USDA 170556](https://fdc.nal.usda.gov/food-details/170556/nutrients) |  |
| Tahini (pastă de susan) | G | 595 | 17 | 53.8 | 21.2 | 9.3 | [USDA 170189](https://fdc.nal.usda.gov/food-details/170189/nutrients) | bază pentru sosuri fără lactate |
| Unt de arahide natural | G | 598 | 22.2 | 51.4 | 22.3 | 5 | [USDA 172470](https://fdc.nal.usda.gov/food-details/172470/nutrients) |  |
| Lapte de cocos light (conservă) | G | 70 | 0.5 | 6.5 | 2 | 0 | etichetă | USDA are doar varianta normală (197 kcal); light = ~⅓ |


## 🍚 Cereale & amidon

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Fulgi de ovăz | A | 379 | 13.2 | 6.5 | 67.7 | 10.1 | [USDA 173904](https://fdc.nal.usda.gov/food-details/173904/nutrients) |  |
| Orez alb / basmati, crud | A | 365 | 7.1 | 0.7 | 80 | 1.3 | [USDA 169756](https://fdc.nal.usda.gov/food-details/169756/nutrients) |  |
| Orez brun, crud | A | 367 | 7.5 | 3.2 | 76.3 | 3.6 | [USDA 169703](https://fdc.nal.usda.gov/food-details/169703/nutrients) |  |
| Paste integrale, uscate | A | 352 | 13.9 | 2.9 | 73.4 | 9.2 | [USDA 169738](https://fdc.nal.usda.gov/food-details/169738/nutrients) |  |
| Quinoa, crudă | A | 368 | 14.1 | 6.1 | 64.2 | 7 | [USDA 168874](https://fdc.nal.usda.gov/food-details/168874/nutrients) |  |
| Hrișcă, crudă | A | 346 | 11.7 | 2.7 | 75 | 10.3 | [USDA 170685](https://fdc.nal.usda.gov/food-details/170685/nutrients) |  |
| Mălai (integral) | A | 362 | 8.1 | 3.6 | 76.9 | 7.3 | [USDA 169697](https://fdc.nal.usda.gov/food-details/169697/nutrients) |  |
| Cartof, crud, cu coajă | A | 77 | 2.1 | 0.1 | 17.5 | 2.1 | [USDA 170026](https://fdc.nal.usda.gov/food-details/170026/nutrients) |  |
| Cartof dulce, crud | A | 86 | 1.6 | 0.1 | 20.1 | 3 | [USDA 168482](https://fdc.nal.usda.gov/food-details/168482/nutrients) |  |
| Pâine integrală | A | 252 | 12.5 | 3.5 | 42.7 | 6 | [USDA 172688](https://fdc.nal.usda.gov/food-details/172688/nutrients) | 1 felie ≈ 40–50 g |


## 🫘 Leguminoase

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Linte verde/brună, uscată | P + A | 352 | 24.6 | 1.1 | 63.4 | 10.7 | [USDA 172420](https://fdc.nal.usda.gov/food-details/172420/nutrients) |  |
| Linte roșie, uscată | P + A | 358 | 23.9 | 2.2 | 63.1 | 10.8 | [USDA 174284](https://fdc.nal.usda.gov/food-details/174284/nutrients) |  |
| Năut conservă, scurs | P + A | 139 | 7.1 | 2.8 | 22.5 | 6.4 | [USDA 173800](https://fdc.nal.usda.gov/food-details/173800/nutrients) |  |
| Năut uscat | P + A | 378 | 20.5 | 6 | 63 | 12.2 | [USDA 173756](https://fdc.nal.usda.gov/food-details/173756/nutrients) |  |
| Fasole roșie conservă, scursă | P + A | 124 | 8 | 1.1 | 21.5 | 5.5 | [USDA 174285](https://fdc.nal.usda.gov/food-details/174285/nutrients) |  |
| Fasole neagră conservă | P + A | 91 | 6 | 0.3 | 16.6 | 6.9 | [USDA 175188](https://fdc.nal.usda.gov/food-details/175188/nutrients) |  |
| Mazăre verde, congelată | P + A | 77 | 5.2 | 0.4 | 13.6 | 4.5 | [USDA 170016](https://fdc.nal.usda.gov/food-details/170016/nutrients) |  |
| Edamame, congelat | P + A | 109 | 11.2 | 4.7 | 7.6 | 4.8 | [USDA 168410](https://fdc.nal.usda.gov/food-details/168410/nutrients) |  |


## 🥦 Legume

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Broccoli | L | 34 | 2.8 | 0.4 | 6.6 | 2.6 | [USDA 170379](https://fdc.nal.usda.gov/food-details/170379/nutrients) |  |
| Conopidă | L | 25 | 1.9 | 0.3 | 5 | 2 | [USDA 169986](https://fdc.nal.usda.gov/food-details/169986/nutrients) |  |
| Varză albă | L | 25 | 1.3 | 0.1 | 5.8 | 2.5 | [USDA 169975](https://fdc.nal.usda.gov/food-details/169975/nutrients) |  |
| Varză de Bruxelles | L | 43 | 3.4 | 0.3 | 9 | 3.8 | [USDA 170383](https://fdc.nal.usda.gov/food-details/170383/nutrients) |  |
| Kale | L | 35 | 2.9 | 1.5 | 4.4 | 4.1 | [USDA 168421](https://fdc.nal.usda.gov/food-details/168421/nutrients) |  |
| Spanac | L | 23 | 2.9 | 0.4 | 3.6 | 2.2 | [USDA 168462](https://fdc.nal.usda.gov/food-details/168462/nutrients) |  |
| Salată verde | L | 15 | 1.4 | 0.2 | 2.9 | 1.3 | [USDA 169249](https://fdc.nal.usda.gov/food-details/169249/nutrients) |  |
| Rucola | L | 25 | 2.6 | 0.7 | 3.7 | 1.6 | [USDA 169387](https://fdc.nal.usda.gov/food-details/169387/nutrients) |  |
| Roșii | L | 18 | 0.9 | 0.2 | 3.9 | 1.2 | [USDA 170457](https://fdc.nal.usda.gov/food-details/170457/nutrients) |  |
| Roșii pasate (passata / piure) | L | 38 | 1.7 | 0.2 | 9 | 1.9 | [USDA 170460](https://fdc.nal.usda.gov/food-details/170460/nutrients) |  |
| Ardei gras roșu | L | 26 | 1 | 0.3 | 6 | 2.1 | [USDA 170108](https://fdc.nal.usda.gov/food-details/170108/nutrients) |  |
| Castravete | L | 15 | 0.7 | 0.1 | 3.6 | 0.5 | [USDA 168409](https://fdc.nal.usda.gov/food-details/168409/nutrients) |  |
| Dovlecel | L | 17 | 1.2 | 0.3 | 3.1 | 1 | [USDA 169291](https://fdc.nal.usda.gov/food-details/169291/nutrients) |  |
| Vinete | L | 25 | 1 | 0.2 | 5.9 | 3 | [USDA 169228](https://fdc.nal.usda.gov/food-details/169228/nutrients) |  |
| Morcov | L | 41 | 0.9 | 0.2 | 9.6 | 2.8 | [USDA 170393](https://fdc.nal.usda.gov/food-details/170393/nutrients) |  |
| Sfeclă roșie | L | 43 | 1.6 | 0.2 | 9.6 | 2.8 | [USDA 169145](https://fdc.nal.usda.gov/food-details/169145/nutrients) |  |
| Țelină (tulpini) | L | 14 | 0.7 | 0.2 | 3 | 1.6 | [USDA 169988](https://fdc.nal.usda.gov/food-details/169988/nutrients) |  |
| Ridichi | L | 16 | 0.7 | 0.1 | 3.4 | 1.6 | [USDA 169276](https://fdc.nal.usda.gov/food-details/169276/nutrients) |  |
| Dovleac | L | 26 | 1 | 0.1 | 6.5 | 0.5 | [USDA 168448](https://fdc.nal.usda.gov/food-details/168448/nutrients) |  |
| Fasole verde | L | 31 | 1.8 | 0.2 | 7 | 2.7 | [USDA 169961](https://fdc.nal.usda.gov/food-details/169961/nutrients) |  |
| Sparanghel | L | 20 | 2.2 | 0.1 | 3.9 | 2.1 | [USDA 168389](https://fdc.nal.usda.gov/food-details/168389/nutrients) |  |
| Ceapă | L | 40 | 1.1 | 0.1 | 9.3 | 1.7 | [USDA 170000](https://fdc.nal.usda.gov/food-details/170000/nutrients) |  |
| Ceapă verde | L | 32 | 1.8 | 0.2 | 7.3 | 2.6 | [USDA 170005](https://fdc.nal.usda.gov/food-details/170005/nutrients) |  |
| Praz | L | 61 | 1.5 | 0.3 | 14.2 | 1.8 | [USDA 169246](https://fdc.nal.usda.gov/food-details/169246/nutrients) |  |
| Usturoi | L | 149 | 6.4 | 0.5 | 33.1 | 2.1 | [USDA 169230](https://fdc.nal.usda.gov/food-details/169230/nutrients) | 1 cățel ≈ 3 g |
| Ciuperci champignon | L | 22 | 3.1 | 0.3 | 3.3 | 1 | [USDA 169251](https://fdc.nal.usda.gov/food-details/169251/nutrients) |  |


## 🍓 Fructe

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Afine | F | 57 | 0.7 | 0.3 | 14.5 | 2.4 | [USDA 171711](https://fdc.nal.usda.gov/food-details/171711/nutrients) |  |
| Zmeură | F | 52 | 1.2 | 0.7 | 11.9 | 6.5 | [USDA 167755](https://fdc.nal.usda.gov/food-details/167755/nutrients) |  |
| Căpșuni | F | 32 | 0.7 | 0.3 | 7.7 | 2 | [USDA 167762](https://fdc.nal.usda.gov/food-details/167762/nutrients) |  |
| Mure | F | 43 | 1.4 | 0.5 | 9.6 | 5.3 | [USDA 173946](https://fdc.nal.usda.gov/food-details/173946/nutrients) |  |
| Mix fructe de pădure (congelat) | F | 47 | 0.9 | 0.4 | 11.4 | 3.6 | USDA (medie 171711/167755/167762) | media afine + zmeură + căpșuni |
| Banană | F | 89 | 1.1 | 0.3 | 22.8 | 2.6 | [USDA 173944](https://fdc.nal.usda.gov/food-details/173944/nutrients) | 1 buc. medie ≈ 120 g |
| Măr, cu coajă | F | 52 | 0.3 | 0.2 | 13.8 | 2.4 | [USDA 171688](https://fdc.nal.usda.gov/food-details/171688/nutrients) | 1 buc. medie ≈ 180 g |
| Pară, cu coajă | F | 57 | 0.4 | 0.1 | 15.2 | 3.1 | [USDA 169118](https://fdc.nal.usda.gov/food-details/169118/nutrients) |  |
| Kiwi | F | 61 | 1.1 | 0.5 | 14.7 | 3 | [USDA 168153](https://fdc.nal.usda.gov/food-details/168153/nutrients) |  |
| Portocală | F | 47 | 0.9 | 0.1 | 11.8 | 2.4 | [USDA 169097](https://fdc.nal.usda.gov/food-details/169097/nutrients) |  |
| Struguri | F | 69 | 0.7 | 0.2 | 18.1 | 0.9 | [USDA 174683](https://fdc.nal.usda.gov/food-details/174683/nutrients) |  |


## 🧂 Condimente

| Aliment | Rol | kcal | Proteine | Grăsimi | Carbo | Fibre | Sursă | Notă |
|---|:-:|--:|--:|--:|--:|--:|---|---|
| Sos de soia | — | 53 | 8.1 | 0.6 | 4.9 | 0.8 | [USDA 174277](https://fdc.nal.usda.gov/food-details/174277/nutrients) |  |
| Muștar | — | 60 | 3.7 | 3.3 | 5.8 | 4 | [USDA 172234](https://fdc.nal.usda.gov/food-details/172234/nutrients) |  |
| Suc de lămâie | — | 22 | 0.4 | 0.2 | 6.9 | 0.3 | [USDA 167747](https://fdc.nal.usda.gov/food-details/167747/nutrients) |  |


---

## Porții uzuale (pentru cântărit din ochi)

| Aliment | Porție | ≈ g |
|---|---|--:|
| Ou M | 1 buc. | 55 |
| Banană | 1 buc. medie | 120 |
| Măr | 1 buc. medie | 180 |
| Pâine integrală | 1 felie | 40–50 |
| Ulei de măsline | 1 lingură | 10 |
| Unt de arahide | 1 lingură | 15 |
| Semințe chia / in | 1 lingură | 10 |
| Nuci / migdale | 1 mână mică | 15–20 |
| Usturoi | 1 cățel | 3 |
| Orez / quinoa / hrișcă crud | 1 porție 20% | 55–65 |
| Carne / pește crud | 1 porție 40% | 150–220 |


## 🌾 De unde vin fibrele — pe scurt

Leguminoase (linte, năut: 10–12 g/100 g uscat), semințe (chia 34, in 27), ovăz (10), paste integrale (9), fructe de pădure (zmeură 6,5), avocado (6,7), legume (2–4 g/100 g). Practic: leguminoase + o lingură de semințe + fructe de pădure + legume la fiecare masă → 30–40 g/zi fără efort.
