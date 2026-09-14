# 📊 date/ — baza de date și calculatorul planului

Aici stă **sursa** din care se generează fișierele de mâncare. Nu se editează manual `comun/1_ingrediente.md`, `comun/2_retete.md`, `ema/4_meniu.md`, `adi/4_meniu.md` — se modifică aici și se regenerează.

| Fișier | Ce e |
|---|---|
| `ingrediente_db.py` | **Baza de ingrediente**: valori per 100 g (kcal, P, G, C, fibre), sursa USDA cu ID. Un ingredient nou = un rând nou aici. |
| `retete.py` | Rețetele (componentele farfuriei cu cantități S / M), calendarul pe 14 zile, țintele calorice (copiate din `ema/2_nutritie.md` și `adi/2_nutritie.md`). Rulat singur, afișează macro-urile pe rețetă și pe zi. |
| `genereaza.py` | Scrie `comun/1_ingrediente.md`, `comun/2_retete.md`, `ema/4_meniu.md`, `adi/4_meniu.md` din cele două de mai sus. |
| `usda_cauta.py` | Caută un aliment în baza USDA locală: `python usda_cauta.py "chicken breast raw"`. |
| `usda/*.zip` | Baza oficială USDA FoodData Central, SR Legacy (aprilie 2018), descărcată de pe fdc.nal.usda.gov. Se dezarhivează automat la prima căutare în `usda/sr/` (ignorat de git). |

## Cum se lucrează

```
cd date
python usda_cauta.py "quinoa uncooked"     # 1. găsești ingredientul nou + ID-ul
# 2. îl adaugi în ingrediente_db.py
# 3. scrii / modifici rețeta în retete.py
python retete.py                           # 4. verifici că zilele ies la țintă
python genereaza.py                        # 5. regenerezi fișierele .md
```

**Regulă:** țintele din `retete.py` (`TARGET`) se țin identice cu `ema/2_nutritie.md` și `adi/2_nutritie.md`, care vin din profil. Când se schimbă profilul (greutate, activitate, obiectiv) → se recalculează nutriția → se actualizează `TARGET` → se regenerează.
