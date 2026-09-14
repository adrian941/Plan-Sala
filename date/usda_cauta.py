# -*- coding: utf-8 -*-
# Caută un aliment în baza USDA SR Legacy (locală) și afișează kcal / P / G / C / fibre per 100 g + fdc_id.
# Folosire:  python usda_cauta.py "chicken breast raw" "lentils raw"
# Prima rulare dezarhivează usda/FoodData_Central_sr_legacy_food_csv_2018-04.zip în usda/sr/ (ignorat de git).
import csv, sys, os, glob, zipfile, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(HERE, "usda", "FoodData_Central_sr_legacy_food_csv_2018-04.zip")
SR = os.path.join(HERE, "usda", "sr")
if not glob.glob(SR + "/*/food.csv"):
    zipfile.ZipFile(ZIP).extractall(SR)
d = glob.glob(SR + "/*/")[0]
foods = {r["fdc_id"]: r["description"] for r in csv.DictReader(open(d + "food.csv", encoding="utf-8"))}
NUT = {"1008": "kcal", "1003": "P", "1004": "G", "1005": "C", "1079": "F"}
vals = {}
for r in csv.DictReader(open(d + "food_nutrient.csv", encoding="utf-8")):
    if r["nutrient_id"] in NUT:
        vals.setdefault(r["fdc_id"], {})[NUT[r["nutrient_id"]]] = float(r["amount"])
def show(fid):
    v = vals.get(str(fid), {})
    return f"{fid} | {foods[str(fid)]} | kcal {v.get('kcal')} P {v.get('P')} G {v.get('G')} C {v.get('C')} F {v.get('F')}"
def search(q, n=10):
    words = q.lower().split()
    for f in [f for f, desc in foods.items() if all(w in desc.lower() for w in words)][:n]:
        print("  ", show(f))
if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("##", q); search(q)
