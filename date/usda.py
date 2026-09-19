# -*- coding: utf-8 -*-
"""Legătura cu baza oficială USDA FoodData Central (SR Legacy) — de acolo vin valorile.

    python usda.py cauta "chicken breast raw"     caută un aliment și-i arată ID-ul
    python usda.py arata 171077                   toți nutrienții unui aliment
    python usda.py nutrienti                      reîmprospătează valorile complete (toate alimentele noastre)
    python usda.py adauga 168874 quinoa "Quinoa, crudă" "Cereale & amidon" [--scurt quinoa]
                                                  aliment nou în plan.db, cu valorile luate din USDA

Cum stau lucrurile cu valorile:
  · cele cinci de pe farfurie (kcal, P, G, C, fibre) stau în tabelul `ingredient` și sunt
    valorile *de plan* — de obicei USDA, dar uneori ajustate de om (lapte 1,5% = media dintre
    1% și 2%, doradă = sea bass). `nutrienti` NU le atinge niciodată;
  · valorile complete (minerale, vitamine, aminoacizi, acizi grași) stau în
    `ingredient_nutrient` și se rescriu liniștit de câte ori vrei.
  · `adauga` e singurul care scrie și cele cinci — la un aliment care încă nu există.

Baza USDA se dezarhivează o dată din usda/*.zip într-un usda/usda.db local (ignorat de git,
se reface oricând). Zip-ul oficial are 36 MB de valori — de-aia nu-l citim la fiecare rulare.
"""
import csv, glob, io, os, sqlite3, sys, zipfile

import db

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(HERE, "usda", "FoodData_Central_sr_legacy_food_csv_2018-04.zip")
SR = os.path.join(HERE, "usda", "sr")
USDA_DB = os.path.join(HERE, "usda", "usda.db")

# cele cinci valori de pe farfurie, cu ID-ul lor USDA
CELE_5 = {1008: "kcal", 1003: "proteine", 1004: "grasimi", 1005: "carbo", 1079: "fibre"}

# numele românești ale nutrienților care ne interesează cel mai des (restul rămân cum le zice USDA)
NUME_RO = {
    1008: "Calorii", 1003: "Proteine", 1004: "Grăsimi", 1005: "Carbohidrați", 1079: "Fibre",
    1063: "Zaharuri", 1093: "Sodiu", 1092: "Potasiu", 1087: "Calciu", 1089: "Fier",
    1090: "Magneziu", 1091: "Fosfor", 1095: "Zinc", 1098: "Cupru", 1101: "Mangan", 1103: "Seleniu",
    1106: "Vitamina A", 1109: "Vitamina E", 1114: "Vitamina D", 1185: "Vitamina K",
    1162: "Vitamina C", 1165: "Tiamină (B1)", 1166: "Riboflavină (B2)", 1167: "Niacină (B3)",
    1175: "Vitamina B6", 1177: "Folat", 1178: "Vitamina B12", 1180: "Colină",
    1253: "Colesterol", 1258: "Grăsimi saturate", 1292: "Grăsimi mononesaturate",
    1293: "Grăsimi polinesaturate", 1404: "Omega-3 (ALA)", 1272: "Omega-3 (DHA)", 1278: "Omega-3 (EPA)",
}


def grupa(nbr):
    """USDA își numerotează nutrienții pe familii; le dăm nume ca să se poată filtra."""
    try:
        n = int(float(nbr))
    except (TypeError, ValueError):
        return "altele"
    return ("macro" if n < 300 else "mineral" if n < 400 else "vitamina"
            if n < 500 else "aminoacizi" if n < 600 else "lipide" if n < 700 else "altele")


def _csv(nume):
    if not glob.glob(SR + "/*/food.csv"):
        print("dezarhivez baza USDA (o singură dată)…")
        zipfile.ZipFile(ZIP).extractall(SR)
    return csv.DictReader(io.open(glob.glob(SR + "/*/")[0] + nume, encoding="utf-8"))


def construieste(forteaza=False):
    """usda/*.zip → usda/usda.db. Se face o singură dată; pe urmă e instantaneu."""
    if os.path.exists(USDA_DB) and not forteaza:
        return USDA_DB
    if os.path.exists(USDA_DB):
        os.remove(USDA_DB)
    print("construiesc usda/usda.db din baza oficială (durează ~un minut)…")
    c = sqlite3.connect(USDA_DB)
    c.executescript("""
        CREATE TABLE aliment (fdc_id INTEGER PRIMARY KEY, descriere TEXT NOT NULL);
        CREATE TABLE nutrient (id INTEGER PRIMARY KEY, nume TEXT, unitate TEXT, nbr TEXT, rang REAL);
        CREATE TABLE valoare (fdc_id INTEGER, nutrient_id INTEGER, cantitate REAL,
                              PRIMARY KEY (fdc_id, nutrient_id)) WITHOUT ROWID;""")
    c.executemany("INSERT INTO aliment VALUES (?,?)",
                  ((int(r["fdc_id"]), r["description"]) for r in _csv("food.csv")))
    c.executemany("INSERT INTO nutrient VALUES (?,?,?,?,?)",
                  ((int(r["id"]), r["name"], r["unit_name"], r["nutrient_nbr"],
                    float(r["rank"]) if r["rank"] else None) for r in _csv("nutrient.csv")))
    c.executemany("INSERT OR IGNORE INTO valoare VALUES (?,?,?)",
                  ((int(r["fdc_id"]), int(r["nutrient_id"]), float(r["amount"]))
                   for r in _csv("food_nutrient.csv") if r["amount"]))
    c.commit()
    n = c.execute("SELECT count(*) FROM valoare").fetchone()[0]
    c.close()
    print(f"gata: {n} valori")
    return USDA_DB


def usda():
    c = sqlite3.connect(construieste())
    c.row_factory = sqlite3.Row
    return c


def valori(u, fdc_id):
    """[(nutrient_id, nume, unitate, nbr, cantitate), …] — tot ce știe USDA despre alimentul ăsta."""
    return u.execute("""SELECT n.id, n.nume, n.unitate, n.nbr, v.cantitate
                        FROM valoare v JOIN nutrient n ON n.id = v.nutrient_id
                        WHERE v.fdc_id = ? ORDER BY n.rang IS NULL, n.rang, n.id""", (fdc_id,)).fetchall()


# ---------------------------------------------------------------- comenzi
def cmd_cauta(q, n=10):
    u = usda()
    like = "%" + "%".join(q.split()) + "%"
    randuri = u.execute("SELECT fdc_id, descriere FROM aliment WHERE lower(descriere) LIKE lower(?) LIMIT ?",
                        (like, n)).fetchall()
    if not randuri:
        # cuvintele pot fi în altă ordine în descriere
        randuri = [r for r in u.execute("SELECT fdc_id, descriere FROM aliment")
                   if all(w in r["descriere"].lower() for w in q.lower().split())][:n]
    for r in randuri:
        v = {x["id"]: x["cantitate"] for x in valori(u, r["fdc_id"])}
        cinci = "  ".join(f"{nume} {v.get(i, '—')}" for i, nume in CELE_5.items())
        print(f"  {r['fdc_id']} | {r['descriere']}\n      {cinci}")


def cmd_arata(fdc_id):
    u = usda()
    a = u.execute("SELECT descriere FROM aliment WHERE fdc_id = ?", (fdc_id,)).fetchone()
    if not a:
        sys.exit(f"USDA n-are alimentul {fdc_id}")
    print(f"{fdc_id} · {a['descriere']}  (per 100 g)")
    for v in valori(u, fdc_id):
        print(f"  {v['id']:>5} {v['nume'][:52]:<52} {v['cantitate']:>10.3f} {v['unitate'].lower()}  [{grupa(v['nbr'])}]")


def _scrie_nutrienti(c, u, cheie, fdc_id):
    n = 0
    for v in valori(u, fdc_id):
        c.execute("INSERT OR REPLACE INTO nutrient(id,nume,nume_ro,unitate,grupa) VALUES (?,?,?,?,?)",
                  (v["id"], v["nume"], NUME_RO.get(v["id"]), v["unitate"], grupa(v["nbr"])))
        c.execute("INSERT OR REPLACE INTO ingredient_nutrient VALUES (?,?,?)",
                  (cheie, v["id"], v["cantitate"]))
        n += 1
    return n


def cmd_nutrienti():
    """Valorile complete pentru toate alimentele noastre care au fdc_id."""
    u, c = usda(), db.conecteaza()
    total = fara = 0
    for r in c.execute("SELECT cheie, nume, fdc_id FROM ingredient ORDER BY cheie"):
        if not r["fdc_id"]:
            fara += 1
            continue
        n = _scrie_nutrienti(c, u, r["cheie"], r["fdc_id"])
        if n == 0:
            print(f"  ⚠️  {r['cheie']}: USDA {r['fdc_id']} n-are valori")
        total += n
    c.commit(); c.close()
    print(f"{total} valori scrise. {fara} alimente fără fdc_id (etichetă / medie) — rămân doar cu cele cinci.")
    db.scrie_dump()
    print("plan.sql actualizat. Rulează acum: python genereaza.py")


def cmd_adauga(fdc_id, cheie, nume, categorie, scurt=None, nota=""):
    """Aliment nou în plan.db, cu cele cinci valori luate direct din USDA."""
    u, c = usda(), db.conecteaza()
    if c.execute("SELECT 1 FROM ingredient WHERE cheie = ?", (cheie,)).fetchone():
        sys.exit(f"Cheia „{cheie}” există deja în plan.db — modific-o, n-o adăuga din nou.")
    cat = c.execute("SELECT id FROM categorie WHERE nume = ?", (categorie,)).fetchone()
    if not cat:
        aval = [r["nume"] for r in c.execute("SELECT nume FROM categorie ORDER BY id")]
        sys.exit(f"Categoria „{categorie}” nu există. Alege dintre: {', '.join(aval)}")
    v = {x["id"]: x["cantitate"] for x in valori(u, fdc_id)}
    lipsa = [n for i, n in CELE_5.items() if i not in v]
    if lipsa:
        print(f"  ⚠️  USDA {fdc_id} n-are {', '.join(lipsa)} — pun 0, verifică pe urmă în plan.sql")
    poz = (c.execute("SELECT max(pozitie) FROM ingredient WHERE categorie_id = ?", (cat["id"],)).fetchone()[0] or 0) + 1
    c.execute("""INSERT INTO ingredient(cheie,nume,nume_scurt,categorie_id,pozitie,kcal,proteine,grasimi,carbo,fibre,
                 sursa,fdc_id,nota) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
              (cheie, nume, scurt, cat["id"], poz,
               round(v.get(1008, 0)), *[round(v.get(i, 0), 1) for i in (1003, 1004, 1005, 1079)],
               f"USDA {fdc_id}", fdc_id, nota))
    n = _scrie_nutrienti(c, u, cheie, fdc_id)
    c.commit(); c.close()
    print(f"adăugat „{nume}” ({cheie}) în {categorie}, cu {n} valori nutriționale.")
    db.scrie_dump()
    print("Acum: pune-l într-o rețetă și rulează python genereaza.py")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "cauta":
        for q in a[1:]:
            print("##", q); cmd_cauta(q)
    elif a[0] == "arata":
        cmd_arata(int(a[1]))
    elif a[0] == "nutrienti":
        cmd_nutrienti()
    elif a[0] == "adauga":
        rest, scurt = list(a[1:]), None
        if "--scurt" in rest:
            i = rest.index("--scurt")
            scurt = rest[i + 1] if i + 1 < len(rest) else None
            del rest[i:i + 2]
        poz = rest[:4]
        if len(poz) < 4:
            sys.exit('Folosire: python usda.py adauga <fdc_id> <cheie> "<nume>" "<categorie>" [--scurt <nume scurt>]')
        cmd_adauga(int(poz[0]), poz[1], poz[2], poz[3], scurt)
    elif a[0] == "construieste":
        construieste(forteaza=True)
    else:
        sys.exit(__doc__)
