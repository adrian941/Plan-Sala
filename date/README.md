# 📊 date/ — baza de date a aplicației

Aici stă **plan.db**, baza SQLite din care iese tot: fișierele `.md` și site-ul. E **sursa unică de adevăr**.

Nu se editează manual `comun/1_ingrediente.md`, `comun/2_retete.md`, `comun/4_calendar.md`, `ema/4_meniu.md`, `adi/4_meniu.md`, `ema/4b_meniu_zilnic.md`, `adi/4b_meniu_zilnic.md`, `_site/data.js` — toate se regenerează din bază.

| Fișier | Ce e |
|---|---|
| `plan.db` | **Baza.** Alimente (cu valorile nutriționale complete și perisabilitatea), rețete cu cantități S/M și **modul de preparare pas cu pas**, calendarul pe 14 zile, persoanele și țintele lor, magazinele. |
| `plan.sql` | **Dump-ul text al bazei**, scris automat la fiecare rulare. El e ce se vede în `git diff` (baza e binară): un ingredient nou sau o cantitate schimbată se citesc direct în PR. |
| `schema.sql` | Schema comentată — ce tabele există și de ce. Din ea se construiește baza de la zero. |
| `db.py` | Accesul la bază: `incarca()` întoarce planul întreg ca obiecte Python. Din linia de comandă: `dump`, `reconstruieste`, `verifica`. |
| `calcule.py` | Macro-uri, rotunjiri, cantități scrise frumos, totaluri pe zi, numărat plante. Nu atinge baza — primește planul. |
| `genereaza.py` | **Scrie tot:** cele 7 fișiere `.md`, `_site/data.js` și `plan.sql`. Textul explicativ (regulile, cum e gândit calendarul) stă în el, ca șablon; datele vin exclusiv din bază. |
| `raport.py` | Verifică fără să scrie nimic: ce iese pe fiecare rețetă, totalurile zilelor față de țintă, plantele pe săptămână. |
| `usda.py` | Legătura cu baza oficială USDA: caută alimente, aduce valorile complete, adaugă un aliment nou în `plan.db`. |
| `usda/*.zip` | Baza oficială **USDA FoodData Central, SR Legacy** (aprilie 2018), de pe fdc.nal.usda.gov. La prima folosire se face din ea un `usda/usda.db` local (ignorat de git, se reface oricând). |

## Cum se lucrează

### Un aliment nou

```
cd date
python usda.py cauta "quinoa uncooked"                                   # 1. găsești ID-ul oficial
python usda.py adauga 168874 quinoa "Quinoa, crudă" "Cereale & amidon" --scurt quinoa
                                                                         # 2. intră în plan.db cu
                                                                         #    valorile luate din USDA
python genereaza.py                                                      # 3. apare în lista de alimente și pe site
```

`adauga` scrie și cele cinci valori de pe farfurie (kcal, P, G, C, fibre) **și** toate celelalte pe care le are USDA (minerale, vitamine, aminoacizi, acizi grași) — ele stau în `ingredient_nutrient`. O parte din ele se și văd acum: **13 vitamine + 10 minerale** la pagina Alimente de pe site (butonul „Vitamine & minerale"), **8 vitamine** pe linia fiecărei rețete din caietul de print și **toate cele 13 vitamine pe banda fiecărei zile**, la paginile Detaliat din caiet — acolo doar ca **procent din DZR**, cu o liniuță încărcată până la el (o coloană are ~4 mm, cantitatea în µg/mg n-ar încăpea). Care anume se afișează se alege în `genereaza.py`, în listele `MICRO`, `VITAMINE` și `VITAMINE_ZI`; restul rămân în bază, materie primă pentru „acoperim necesarul de fier / B12?".

Procentul din **DZR** se socotește din `nutrient.dzr` — doza zilnică de referință, în aceeași unitate ca valorile. E VNR-ul de pe etichetele din UE (Reg. 1169/2011, anexa XIII), deci **același pentru Ema și Adi**; colina, care n-are VNR, are aportul adecvat EFSA (400 mg). Completat doar la cele 13 vitamine: `dzr` NULL înseamnă „nu arătăm procent". Vrei procente și la minerale → pui valorile în coloana aia, nu în cod.

### O rețetă nouă, o cantitate schimbată, altă zi în calendar

O rețetă nouă are nevoie, pe lângă ingrediente și cantități, de **`reteta.preparare`** (modul de preparare: un pas pe linie, fără numere — ele se pun la afișare) și de **`reteta.sfat`** (nota „de ce așa": tehnica de bucătar plus motivul nutrițional). Fără ele, rețeta apare goală pe pagina de rețete și în caietul de print.

Se modifică în `plan.db` (cu SQL, sau cu orice unealtă de SQLite — DB Browser for SQLite e cea mai comodă), apoi:

```
python raport.py        # ies zilele la țintă?
python genereaza.py     # regenerează cele 7 .md + _site/data.js + plan.sql
```

### Dacă baza s-a stricat sau a ieșit prost dintr-un merge

```
python db.py reconstruieste   # plan.db se reface din plan.sql
python db.py verifica         # schema e cea din schema.sql? tabelele sunt pline?
```

**Un amănunt de git:** după `reconstruieste`, fișierul binar `plan.db` poate arăta „modificat" chiar dacă datele sunt aceleași (SQLite își rearanjează paginile). **`plan.sql` e cel care spune adevărul** — dacă el nu s-a schimbat, nici datele nu s-au schimbat.

## Două reguli

1. **Valorile de plan nu se rescriu din USDA.** Cele cinci de pe farfurie stau în tabelul `ingredient` și unele sunt ajustate cu bună știință (lapte 1,5% = media dintre 1% și 2%; doradă = valori de la sea bass; mixul de fructe de pădure = media a trei). `python usda.py nutrienti` le lasă în pace — scrie doar alături, în `ingredient_nutrient`.
2. **Țintele din `persoana` se țin identice cu `ema/2_nutritie.md` și `adi/2_nutritie.md`**, care vin din profil. Când se schimbă profilul (greutate, activitate, obiectiv) → se recalculează nutriția → se actualizează țintele în bază → se regenerează.
