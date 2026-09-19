# -*- coding: utf-8 -*-
"""Accesul la plan.db — baza de date a aplicației, sursa unică de adevăr.

Tot ce citește sau scrie baza trece pe aici. `incarca()` întoarce planul întreg
ca obiecte Python simple; de acolo îl iau `calcule.py` și `genereaza.py`.

Din linia de comandă:
    python db.py dump             → rescrie plan.sql (dump-ul text ținut în git)
    python db.py reconstruieste   → reface plan.db din plan.sql
    python db.py verifica         → schema din plan.db == schema.sql? tabelele sunt pline?
"""
import io, os, sqlite3, sys
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
DB, SQL, SCHEMA = (os.path.join(HERE, n) for n in ("plan.db", "plan.sql", "schema.sql"))


# ============================ modelul ============================
# Obiecte simple, exact cât îi trebuie generatorului. Cantitățile sunt
# mereu per 100 g pentru ingrediente și în grame (sau ml) pentru rețete.

@dataclass
class Ingredient:
    cheie: str; nume: str; nume_scurt: str | None; categorie: str; pozitie: int
    kcal: float; proteine: float; grasimi: float; carbo: float; fibre: float
    sursa: str; fdc_id: int | None; nota: str
    unitate: str; gram_bucata: float | None; bucata_sg: str | None; bucata_pl: str | None
    e_planta: int

    @property
    def valori(self):
        """Cele cinci, în ordinea folosită peste tot: kcal, P, G, C, fibre."""
        return (self.kcal, self.proteine, self.grasimi, self.carbo, self.fibre)

    @property
    def scurt(self):
        """Numele cum apare în meniu: cel scurt dacă are, altfel până la prima virgulă."""
        return self.nume_scurt if self.nume_scurt else self.nume.split(",")[0]


@dataclass
class Categorie:
    id: int; nume: str; icon: str; rol: str
    ingrediente: list = field(default_factory=list)


@dataclass
class Reteta:
    id: str; pozitie: int; grup: str; nume: str; scurt: str; masa: str; timp: str
    tine: str; cum: str; varianta: str
    proaspat: int; congelator: int; semn: str
    carne_rosie: str | None; peste: str | None; nota_gatit: str | None
    # comp = [(eticheta, [(cheie, g_s, g_m), …]), …] — elementele farfuriei, în ordine
    comp: list = field(default_factory=list)

    def ingrediente(self, portie):
        """[(cheie, grame), …] pentru porția S sau M — doar ce intră efectiv."""
        i = 1 if portie == "S" else 2
        return [(it[0], it[i]) for _lbl, items in self.comp for it in items if it[i] > 0]


@dataclass
class Persoana:
    cheie: str; nume: str; pronume: str; portie: str; portie_nume: str
    kcal: int; proteine: int; grasimi: int; carbo: int; fibre_tinta: str; apa: str

    @property
    def tinta(self):
        return (self.kcal, self.proteine, self.grasimi, self.carbo)


@dataclass
class Zi:
    id: int; saptamana: int; pozitie: int; nume: str; nume_scurt: str; semne: str
    nota_gatit: str | None; gatit_override: str | None
    # mese = [(tip, icon, reteta_id), …] în ordinea: mic dejun, prânz, gustare, cină
    mese: list = field(default_factory=list)

    @property
    def retete(self):
        return [r for _t, _i, r in self.mese]


@dataclass
class Plan:
    categorii: list          # [Categorie], în ordinea de afișare
    ingrediente: dict        # cheie → Ingredient (în ordinea din liste)
    retete: dict             # id → Reteta (în ordinea din liste)
    persoane: list           # [Persoana]
    zile: list               # [Zi], 14, în ordine

    def persoana(self, cheie):
        return next(p for p in self.persoane if p.cheie == cheie)


# ============================ citirea ============================

def conecteaza(cale=DB):
    if not os.path.exists(cale):
        sys.exit(f"Nu găsesc {cale}. Rulează: python db.py reconstruieste")
    c = sqlite3.connect(cale)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    return c


def incarca(cale=DB):
    """Citește tot planul din bază. Ordinea rândurilor e cea din bază — de ea
    depind fișierele generate, deci fiecare SELECT are ORDER BY explicit."""
    c = conecteaza(cale)

    categorii = [Categorie(r["id"], r["nume"], r["icon"], r["rol"])
                 for r in c.execute("SELECT * FROM categorie ORDER BY id")]
    dupa_id = {k.id: k for k in categorii}

    ingrediente = {}
    for r in c.execute("SELECT * FROM ingredient ORDER BY categorie_id, pozitie"):
        cat = dupa_id[r["categorie_id"]]
        ing = Ingredient(r["cheie"], r["nume"], r["nume_scurt"], cat.nume, r["pozitie"],
                         r["kcal"], r["proteine"], r["grasimi"], r["carbo"], r["fibre"],
                         r["sursa"], r["fdc_id"], r["nota"], r["unitate"],
                         r["gram_bucata"], r["bucata_sg"], r["bucata_pl"], r["e_planta"])
        ingrediente[ing.cheie] = ing
        cat.ingrediente.append(ing)

    retete = {}
    for r in c.execute("SELECT * FROM reteta ORDER BY pozitie"):
        retete[r["id"]] = Reteta(r["id"], r["pozitie"], r["grup"], r["nume"], r["scurt"],
                                 r["masa"], r["timp"], r["tine"], r["cum"], r["varianta"],
                                 r["proaspat"], r["congelator"], r["semn"],
                                 r["carne_rosie"], r["peste"], r["nota_gatit"])
    # ORDER BY reteta_id, pozitie: în interiorul unei rețete elementele vin în ordinea lor,
    # deci se adaugă la `comp` exact cum trebuie (între rețete ordinea n-are importanță).
    elemente = {}
    for r in c.execute("SELECT * FROM reteta_element ORDER BY reteta_id, pozitie"):
        items = []
        elemente[r["id"]] = items
        retete[r["reteta_id"]].comp.append((r["eticheta"], items))
    for r in c.execute("SELECT * FROM reteta_ingredient ORDER BY element_id, pozitie"):
        elemente[r["element_id"]].append((r["ingredient_cheie"], r["g_s"], r["g_m"]))

    persoane = [Persoana(r["cheie"], r["nume"], r["pronume"], r["portie"], r["portie_nume"],
                         r["kcal"], r["proteine"], r["grasimi"], r["carbo"],
                         r["fibre_tinta"], r["apa"])
                for r in c.execute("SELECT * FROM persoana ORDER BY pozitie")]

    zile = {}
    for r in c.execute("SELECT * FROM zi ORDER BY id"):
        zile[r["id"]] = Zi(r["id"], r["saptamana"], r["pozitie"], r["nume"], r["nume_scurt"],
                           r["semne"], r["nota_gatit"], r["gatit_override"])
    for r in c.execute("SELECT * FROM zi_masa ORDER BY zi_id, pozitie"):
        zile[r["zi_id"]].mese.append((r["tip"], r["icon"], r["reteta_id"]))

    c.close()
    return Plan(categorii, ingrediente, retete, persoane, list(zile.values()))


# ============================ dump / reconstruire ============================

def scrie_dump(cale=DB, iesire=SQL):
    """plan.db → plan.sql. Dump-ul e ce se vede în git: o linie INSERT pe rând,
    așa încât un ingredient nou sau o cantitate schimbată se citesc direct în diff."""
    c = sqlite3.connect(cale)
    with io.open(iesire, "w", encoding="utf-8", newline="\n") as f:
        f.write("-- Dump text al plan.db — GENERAT de `python db.py dump`, nu se editează.\n"
                "-- El e ce se vede în git (baza e binară). Reconstruire: python db.py reconstruieste\n")
        for linie in c.iterdump():
            f.write(linie + "\n")
    c.close()
    return iesire


def reconstruieste(sursa=SQL, iesire=DB):
    """plan.sql → plan.db. De folosit dacă baza s-a stricat sau după un merge în git."""
    if os.path.exists(iesire):
        os.remove(iesire)
    c = sqlite3.connect(iesire)
    c.executescript(io.open(sursa, encoding="utf-8").read())
    c.commit(); c.close()
    return iesire


def _schema(c):
    return sorted(r[0] for r in c.execute(
        "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%'"))


def verifica(cale=DB):
    """Baza are exact schema din schema.sql și nu e goală?"""
    c = conecteaza(cale)
    gol = sqlite3.connect(":memory:")
    gol.executescript(io.open(SCHEMA, encoding="utf-8").read())
    probleme = []
    if _schema(c) != _schema(gol):
        probleme.append("schema din plan.db diferă de schema.sql")
    for t, minim in (("categorie", 1), ("ingredient", 1), ("reteta", 1),
                     ("reteta_ingredient", 1), ("persoana", 2), ("zi", 14), ("zi_masa", 56)):
        n = c.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        if n < minim:
            probleme.append(f"tabelul {t} are {n} rânduri (așteptat ≥{minim})")
    orfane = c.execute("""SELECT count(*) FROM reteta_ingredient ri
                          LEFT JOIN ingredient i ON i.cheie = ri.ingredient_cheie
                          WHERE i.cheie IS NULL""").fetchone()[0]
    if orfane:
        probleme.append(f"{orfane} ingrediente folosite în rețete nu există în lista de alimente")
    c.close(); gol.close()
    return probleme


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verifica"
    if cmd == "dump":
        print("scris", scrie_dump())
    elif cmd == "reconstruieste":
        print("scris", reconstruieste())
    elif cmd == "verifica":
        p = verifica()
        print("\n".join("⚠️  " + x for x in p) if p else "✅ baza e în regulă")
        sys.exit(1 if p else 0)
    else:
        sys.exit(__doc__)
