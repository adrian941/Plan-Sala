-- ============================================================================
--  plan.db — baza de date a aplicației. SURSA UNICĂ DE ADEVĂR.
--  Tot ce se vede în fișierele .md și pe site iese de aici, prin genereaza.py.
--  Nimic nu se scrie de mână în fișierele generate.
--
--  Reconstruire de la zero:   python date/db.py reconstruieste   (din plan.sql)
--  Dump text (pentru git):    se scrie automat la fiecare modificare → plan.sql
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
--  meta — versiunea schemei și alte chei mărunte
-- ---------------------------------------------------------------------------
CREATE TABLE meta (
  cheie   TEXT PRIMARY KEY,
  valoare TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
--  categorie — grupele de alimente, în ordinea în care apar în liste
--  `rol` = rolul pe farfuria 40/40/20: P proteină · L legume · A amidon ·
--  G grăsime (nu ocupă felie) · F fruct · — condiment
-- ---------------------------------------------------------------------------
CREATE TABLE categorie (
  id      INTEGER PRIMARY KEY,   -- și ordinea de afișare
  nume    TEXT NOT NULL UNIQUE,  -- "Carne & pește"
  icon    TEXT NOT NULL,         -- 🥩
  rol     TEXT NOT NULL          -- P / L / A / G / F / P + A / —
);

-- ---------------------------------------------------------------------------
--  ingredient — lista de alimente. Valorile sunt PER 100 g de aliment
--  crud / uscat (conservele: scurse). Ele sunt cele din care se calculează
--  absolut tot: rețete, meniuri, totaluri pe zi.
--
--  De ce stau cele cinci valori aici și nu în `ingredient_nutrient`:
--  sunt valorile *de plan*, verificate de om. De obicei vin din USDA, dar
--  unele sunt ajustate cu bună știință (lapte 1,5% = media dintre 1% și 2%,
--  doradă = valori de la sea bass, mix de fructe de pădure = media a trei).
--  Importul din USDA nu le atinge niciodată — el scrie doar în
--  `ingredient_nutrient`, alături.
-- ---------------------------------------------------------------------------
CREATE TABLE ingredient (
  cheie         TEXT PRIMARY KEY,                     -- "pui_piept"
  nume          TEXT NOT NULL,                        -- "Piept de pui, fără piele, crud"
  nume_scurt    TEXT,                                 -- "piept de pui" (cum apare în meniu); NULL = se taie din `nume` la prima virgulă
  categorie_id  INTEGER NOT NULL REFERENCES categorie(id),
  pozitie       INTEGER NOT NULL,                     -- ordinea în categoria lui

  kcal          REAL NOT NULL,
  proteine      REAL NOT NULL,
  grasimi       REAL NOT NULL,
  carbo         REAL NOT NULL,
  fibre         REAL NOT NULL,

  sursa         TEXT NOT NULL,                        -- "USDA 171077" / "etichetă"
  fdc_id        INTEGER,                              -- ID-ul USDA, dacă există (căutabil pe fdc.nal.usda.gov)
  nota          TEXT NOT NULL DEFAULT '',

  -- cum se scrie cantitatea în meniu
  unitate       TEXT NOT NULL DEFAULT 'g' CHECK (unitate IN ('g','ml')),
  gram_bucata   REAL,                                 -- 55 la ou → "3 ouă" în loc de "165 g"
  bucata_sg     TEXT,                                 -- "ou"
  bucata_pl     TEXT,                                 -- "ouă"

  -- se pune la socoteala „plante diferite pe săptămână" (țintă American Gut Project ≥30)?
  -- uleiul și untul ies, deși vin din plante / nu sunt legume pe farfurie
  e_planta      INTEGER NOT NULL DEFAULT 0 CHECK (e_planta IN (0,1)),

  -- perisabilitate — DE COMPLETAT. Rămâne goală până decidem unde se afișează;
  -- de aici va ieși „ce se cumpără proaspăt" vs. „ce se ia din timp" pe lista de cumpărături.
  zile_frigider INTEGER,                              -- câte zile ține în frigider, crud
  se_congeleaza INTEGER CHECK (se_congeleaza IN (0,1)),
  e_staple      INTEGER CHECK (e_staple IN (0,1)),    -- se ține mereu în casă (cămară)
  nota_pastrare TEXT
);
CREATE INDEX ix_ingredient_cat ON ingredient(categorie_id, pozitie);

-- ---------------------------------------------------------------------------
--  nutrient + ingredient_nutrient — valorile nutriționale complete,
--  importate din baza oficială USDA (SR Legacy) de `usda_import.py`.
--  Per 100 g, ca peste tot. Nimic de aici nu e încă afișat: e materia primă
--  pentru „acoperim necesarul de fier / calciu / B12?".
-- ---------------------------------------------------------------------------
CREATE TABLE nutrient (
  id       INTEGER PRIMARY KEY,   -- nutrient_id de la USDA (1008 = Energy, 1003 = Protein…)
  nume     TEXT NOT NULL,         -- cum îi zice USDA
  nume_ro  TEXT,                  -- cum îi zicem noi, unde are rost
  unitate  TEXT NOT NULL,         -- KCAL / G / MG / UG / IU
  grupa    TEXT                   -- macro / mineral / vitamina / lipide / aminoacizi / altele
);

CREATE TABLE ingredient_nutrient (
  ingredient_cheie TEXT NOT NULL REFERENCES ingredient(cheie) ON DELETE CASCADE,
  nutrient_id      INTEGER NOT NULL REFERENCES nutrient(id),
  valoare          REAL NOT NULL,   -- per 100 g
  PRIMARY KEY (ingredient_cheie, nutrient_id)
) WITHOUT ROWID;

-- ---------------------------------------------------------------------------
--  reteta — o rețetă, cu ce iese pe porție calculat din ingrediente.
--  Cantitățile stau în reteta_ingredient, pe două mărimi de porție (S și M).
-- ---------------------------------------------------------------------------
CREATE TABLE reteta (
  id          TEXT PRIMARY KEY,   -- "MD1", "P12"
  pozitie     INTEGER NOT NULL,   -- ordinea în liste
  grup        TEXT NOT NULL,      -- "Mic dejun" / "Gustări" / "Feluri principale"
  nume        TEXT NOT NULL,      -- numele întreg, cum apare în meniu
  scurt       TEXT NOT NULL,      -- numele scurt, pentru calendar și cardurile de pe site
  masa        TEXT NOT NULL,      -- "prânz/cină", "mic dejun 🥚", "gustare 🏋️"
  timp        TEXT NOT NULL,      -- "45′ (10 activ)"
  tine        TEXT NOT NULL,      -- cât ține la frigider: "3 zile", "nu", "—"
  cum         TEXT NOT NULL,      -- cum se face
  varianta    TEXT NOT NULL DEFAULT '',  -- „merge și cu…"

  -- pentru calendarul de gătit
  proaspat    INTEGER NOT NULL DEFAULT 0 CHECK (proaspat IN (0,1)),  -- se face ×2, în ziua aia (peștele)
  congelator  INTEGER NOT NULL DEFAULT 0 CHECK (congelator IN (0,1)),-- se face ×8, jumătate la congelator
  semn        TEXT NOT NULL DEFAULT '',   -- 🐟 lângă numele din calendar
  carne_rosie TEXT,               -- "vită" / "porc" — pentru verificarea „max 2 feluri/săpt."
  peste       TEXT,               -- "doradă" / "păstrăv" — pentru verificarea „pește 2×/săpt."
  nota_gatit  TEXT                -- se lipește în coloana „ce se gătește seara"
);

-- elementele farfuriei, în ordine: Proteină · Legume · Amidon · Sos · Fruct · Grăsimi
CREATE TABLE reteta_element (
  id        INTEGER PRIMARY KEY,
  reteta_id TEXT NOT NULL REFERENCES reteta(id) ON DELETE CASCADE,
  pozitie   INTEGER NOT NULL,
  eticheta  TEXT NOT NULL,        -- se păstrează exact, spațiile incluse (o rețetă are două elemente „Amidon")
  UNIQUE (reteta_id, pozitie)
);

CREATE TABLE reteta_ingredient (
  id               INTEGER PRIMARY KEY,
  element_id       INTEGER NOT NULL REFERENCES reteta_element(id) ON DELETE CASCADE,
  pozitie          INTEGER NOT NULL,
  ingredient_cheie TEXT NOT NULL REFERENCES ingredient(cheie),
  g_s              REAL NOT NULL DEFAULT 0,   -- grame (sau ml) la porția S; 0 = nu intră
  g_m              REAL NOT NULL DEFAULT 0,   -- idem, porția M
  UNIQUE (element_id, pozitie)
);

-- ---------------------------------------------------------------------------
--  persoana — cine mănâncă, ce mărime de porție are și care-i sunt țintele.
--  Țintele sunt aceleași cu cele din `<persoana>/2_nutritie.md`, care vin din profil.
-- ---------------------------------------------------------------------------
CREATE TABLE persoana (
  cheie        TEXT PRIMARY KEY,   -- "ema" / "adi"
  pozitie      INTEGER NOT NULL,
  nume         TEXT NOT NULL,      -- "Ema"
  pronume      TEXT NOT NULL,      -- "ea" / "el"
  portie       TEXT NOT NULL CHECK (portie IN ('S','M')),
  portie_nume  TEXT NOT NULL,      -- "standard" / "mare"
  kcal         INTEGER NOT NULL,
  proteine     INTEGER NOT NULL,
  grasimi      INTEGER NOT NULL,
  carbo        INTEGER NOT NULL,
  fibre_tinta  TEXT NOT NULL,      -- "25–30"
  apa          TEXT NOT NULL       -- litri pe zi: "2,5"
);

-- ---------------------------------------------------------------------------
--  zi + zi_masa — calendarul pe 14 zile: ce rețetă, în ce zi, la ce masă.
-- ---------------------------------------------------------------------------
CREATE TABLE zi (
  id             INTEGER PRIMARY KEY,  -- 0…13, în ordine
  saptamana      INTEGER NOT NULL,     -- 1 sau 2
  pozitie        INTEGER NOT NULL,     -- 0…6 în săptămână
  nume           TEXT NOT NULL,        -- "Luni"
  nume_scurt     TEXT NOT NULL,        -- "Lu"
  semne          TEXT NOT NULL DEFAULT '',  -- 🥚 zi cu ouă · 🏋️ zi de sală
  nota_gatit     TEXT,                 -- „+ borcane de ovăz peste noapte pt. marți"
  gatit_override TEXT,                 -- înlocuiește tot ce s-ar fi gătit în seara aia
  UNIQUE (saptamana, pozitie)
);

CREATE TABLE zi_masa (
  id        INTEGER PRIMARY KEY,
  zi_id     INTEGER NOT NULL REFERENCES zi(id) ON DELETE CASCADE,
  pozitie   INTEGER NOT NULL,      -- 0 mic dejun · 1 prânz · 2 gustare · 3 cină
  tip       TEXT NOT NULL,         -- "Mic dejun" / "Prânz" / "Gustare" / "Cină"
  icon      TEXT NOT NULL,         -- 🌅 🍲 🍎 🌙
  reteta_id TEXT NOT NULL REFERENCES reteta(id),
  UNIQUE (zi_id, pozitie)
);

-- ---------------------------------------------------------------------------
--  magazin + cumparaturi — pasul 3. DE COMPLETAT: tabelele există, dar sunt
--  goale până știm ce magazine aveți la îndemână și ce se găsește bun în fiecare.
--  Lista se va calcula din rețetele puse în calendar × porțiile fiecăruia.
-- ---------------------------------------------------------------------------
CREATE TABLE magazin (
  id       INTEGER PRIMARY KEY,
  nume     TEXT NOT NULL UNIQUE,
  pozitie  INTEGER NOT NULL,
  nota     TEXT
);

-- de unde luăm fiecare aliment, cu ce ambalaj se vinde (ca să rotunjim lista la ambalajul real)
CREATE TABLE ingredient_magazin (
  ingredient_cheie TEXT NOT NULL REFERENCES ingredient(cheie) ON DELETE CASCADE,
  magazin_id       INTEGER NOT NULL REFERENCES magazin(id) ON DELETE CASCADE,
  preferat         INTEGER NOT NULL DEFAULT 0 CHECK (preferat IN (0,1)),
  ambalaj_g        REAL,          -- cât are un pachet / o conservă
  ambalaj_nume     TEXT,          -- "conservă 400 g", "pachet 500 g"
  nota             TEXT,
  PRIMARY KEY (ingredient_cheie, magazin_id)
);

-- ce e deja în casă, ca să nu cumpărăm de două ori
CREATE TABLE stoc (
  ingredient_cheie TEXT PRIMARY KEY REFERENCES ingredient(cheie) ON DELETE CASCADE,
  cantitate_g      REAL NOT NULL DEFAULT 0,
  actualizat       TEXT
);
