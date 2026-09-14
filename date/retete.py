# -*- coding: utf-8 -*-
import sys, io
from ingrediente_db import DB, NAME, ING
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def macro(items):
    t=[0.0]*5
    for k,g in items:
        v=DB[k]
        for i in range(5): t[i]+=v[i]*g/100
    return t
def r5(x): return int(round(x/5.0)*5)

SHORT = {
 "ou":"ouă","branza_vaci":"brânză de vaci","paine":"pâine integrală","banana":"banană","mar":"măr",
 "ulei":"ulei de măsline","skyr":"skyr","iaurt_grec":"iaurt grec","lapte":"lapte 1,5%","ovaz":"fulgi de ovăz",
 "fructe_padure":"fructe de pădure","chia":"chia","nuci":"nuci","in":"in măcinat","unt_arahide":"unt de arahide",
 "avocado":"avocado","rosii":"roșii","castravete":"castravete","migdale":"migdale","pui_piept":"piept de pui",
 "cartof_dulce":"cartof dulce","broccoli":"broccoli","vita":"vită slabă","ceapa":"ceapă","morcov":"morcov",
 "ardei":"ardei","ciuperci":"ciuperci","rosii_pasate":"roșii pasate","malai":"mălai","telemea":"telemea",
 "somon":"somon","quinoa":"quinoa","fasole_verde":"fasole verde","sardine":"sardine","naut":"năut",
 "salata":"salată verde","pui_tocat":"piept de pui tocat","dorada":"doradă","chefal":"chefal","porc_muschi":"mușchi de porc","ton":"ton (conservă, scurs)","linte":"linte","paste_int":"paste integrale",
 "dovlecel":"dovlecel","parmezan":"parmezan","porc_cotlet":"cotlet de porc","cartof":"cartofi","conopida":"conopidă",
 "unt":"unt","varza":"varză","spanac":"spanac","cocos_light":"lapte de cocos light","orez_alb":"orez basmati",
 "orez_brun":"orez brun","masline":"măsline","linte_rosie":"linte roșie","telina":"țelină",
 "seminte_dovleac":"semințe de dovleac","soia":"sos de soia","caju":"caju","pastrav":"păstrăv","ridichi":"ridichi",
 "usturoi":"usturoi","ceapa_verde":"ceapă verde","kefir":"kefir","albus":"albușuri",
 "hrisca":"hrișcă","vinete":"vinete","rucola":"rucola","sfecla":"sfeclă","mazare":"mazăre","varza_bruxelles":"varză de Bruxelles",
 "dovleac":"dovleac","sparanghel":"sparanghel","praz":"praz","kale":"kale","zmeura":"zmeură","afine":"afine",
 "seminte_floarea":"semințe de floarea-soarelui","tahini":"tahini","patrunjel":"pătrunjel","mustar":"muștar","lamaie":"suc de lămâie","pui_pulpa":"pulpă de pui",
}
PIECE = {"ou":(55,"ouă","ou"),"banana":(120,"banane","banană"),"mar":(180,"mere","măr")}
PLANT_CATS = {"Cereale & amidon","Leguminoase","Legume","Fructe","Grăsimi"}
CAT = {k:c for k,_,c,*_ in ING}
NOT_PLANT = {"ulei","unt","cocos_light"}
def qty(k,g):
    if k in PIECE:
        w,pl,sg=PIECE[k]; n=g/w
        n_s = f"{n:g}".replace(".5","½")
        return f"{n_s} {sg if n==1 else pl}"
    if k in ("lapte","cocos_light","soia","lamaie"): return f"{g:g} ml {SHORT[k]}"
    return f"{g:g} g {SHORT[k]}"

# ---------- rețete ----------
# comp = listă de (etichetă, [(ing, gS, gM), ...]); etichetele: Proteină / Legume / Amidon / Sos / Fruct / Grăsimi
R = {}
def rec(id, nume, scurt, masa, timp, tine, comp, cum, var=""):
    S=[(k,gs) for _,items in comp for k,gs,gm in items if gs>0]
    M=[(k,gm) for _,items in comp for k,gs,gm in items if gm>0]
    R[id]=dict(id=id,nume=nume,scurt=scurt,masa=masa,timp=timp,tine=tine,comp=comp,S=S,M=M,cum=cum,var=var)

# ===== MIC DEJUN =====
rec("MD1","Omletă cu legume și brânză de vaci, pâine integrală + banană","Omletă cu legume","mic dejun 🥚","15′","nu",
 [("Proteină",[("ou",165,220),("branza_vaci",100,120)]),
  ("Legume",[("spanac",50,50),("rosii",60,60),("ciuperci",50,50),("ceapa_verde",20,20)]),
  ("Amidon",[("paine",50,50)]),("Grăsimi",[("ulei",5,5)]),("Fruct",[("banana",120,120)])],
 "Ciupercile și ceapa verde 3 min în ulei, spanacul și roșiile 1 min, ouăle bătute deasupra, amestecat până se leagă. Brânza de vaci alături. Banana la final.",
 "Legumele = ce e în casă (ardei, dovlecel, praz). Banana ↔ măr / 150 g fructe de pădure.")
rec("MD2","Ovăz peste noapte cu skyr, fructe de pădure, chia și nuci","Ovăz peste noapte","mic dejun","5′ (seara)","3 zile",
 [("Proteină",[("skyr",200,200)]),("Amidon",[("ovaz",60,70)]),("Fruct",[("fructe_padure",100,100)]),
  ("Grăsimi",[("chia",10,10),("nuci",10,15)]),("Sos",[("lapte",100,100)])],
 "Totul într-un borcan, amestecat, la frigider peste noapte. Nucile deasupra dimineața. Scorțișoară.",
 "Iarna: ovăz fiert în lapte, skyr adăugat la final.")
rec("MD3","Bol de iaurt grec cu banană, unt de arahide, ovăz și in","Bol de iaurt grec","mic dejun","5′","nu",
 [("Proteină",[("iaurt_grec",200,200)]),("Amidon",[("ovaz",40,50)]),("Fruct",[("banana",120,120),("afine",50,50)]),
  ("Grăsimi",[("unt_arahide",15,20),("in",10,10)])],
 "Iaurtul în bol, banana felii și afinele, ovăzul și inul deasupra, untul de arahide picurat. Scorțișoară.", "")
rec("MD4","Ouă ochiuri cu avocado pe pâine, roșii, castravete, brânză de vaci + măr","Ochiuri cu avocado","mic dejun 🥚","10′","nu",
 [("Proteină",[("ou",165,220),("branza_vaci",100,120)]),("Legume",[("rosii",100,100),("castravete",100,100),("rucola",20,20)]),
  ("Amidon",[("paine",50,50)]),("Grăsimi",[("avocado",50,50)]),("Fruct",[("mar",180,180)])],
 "Avocado zdrobit cu lămâie pe pâine, ouăle (ochiuri sau fierte moi) deasupra, rucola, roșiile, castravetele și brânza alături.", "")

# ===== GUSTĂRI =====
rec("G1","Skyr cu măr și migdale","Skyr cu măr","gustare","2′","—",
 [("Proteină",[("skyr",200,250)]),("Fruct",[("mar",180,180)]),("Grăsimi",[("migdale",15,20)])],
 "Se mănâncă împreună sau separat. Scorțișoară pe măr.", "")
rec("G2","Brânză de vaci cu pâine integrală și legume crude","Brânză de vaci cu pâine","gustare","5′","—",
 [("Proteină",[("branza_vaci",150,200)]),("Amidon",[("paine",40,50)]),("Legume",[("castravete",50,50),("ardei",50,50),("morcov",50,50)])],
 "Brânza pe pâine cu sare, piper, mărar sau boia; legumele crude, bețe, alături.",
 "Ridichi lângă castravete — doar la cine le vrea.")
rec("G3","Shake post-sală: lapte, skyr, banană, unt de arahide","Shake post-sală","gustare 🏋️","3′","—",
 [("Proteină",[("skyr",150,200)]),("Sos",[("lapte",200,200)]),("Fruct",[("banana",120,120)]),("Grăsimi",[("unt_arahide",10,15)])],
 "Totul la blender; cacao sau scorțișoară opțional. Fără blender: skyr + banană tăiată + laptele băut alături.",
 "De ce: proteină rapidă + carbohidrați simpli după forță.")

# ===== FELURI PRINCIPALE — farfuria 40/40/20 =====
rec("P1","Pui la cuptor cu legume la tavă, cartof dulce și sos de tahini cu lămâie","Pui la cuptor cu legume la tavă","prânz/cină","45′ (10 activ)","3 zile",
 [("Proteină",[("pui_piept",150,190)]),
  ("Legume",[("broccoli",100,100),("morcov",60,60),("ceapa",50,50),("ardei",60,60)]),
  ("Amidon",[("cartof_dulce",200,220)]),
  ("Sos",[("tahini",12,12),("usturoi",3,3),("lamaie",10,10)]),("Grăsimi",[("ulei",7,9)])],
 "Cartoful dulce cuburi + morcovul cu ½ din ulei și boia afumată, 20 min la 200 °C. Se adaugă puiul (oregano, usturoi, lămâie), broccoli, ceapa și ardeiul cu restul de ulei, încă 20–25 min. Sos: tahini + lămâie + usturoi pisat + 2 linguri apă + sare, amestecat până e cremos.", "")
rec("P2","Tocăniță de vită cu ciuperci, mămăligă și salată de varză roșie cu mere","Tocăniță de vită cu mămăligă","prânz/cină","75′ (15 activ)","4 zile · congelator",
 [("Proteină",[("vita",160,200)]),
  ("Legume",[("ciuperci",80,80),("ceapa",50,50),("morcov",50,50),("ardei",40,40),("varza",100,100),("mar",40,40)]),
  ("Amidon",[("malai",65,70)]),
  ("Sos",[("rosii_pasate",100,100)]),("Grăsimi",[("ulei",10,12)])],
 "Vita rumenită în ½ ulei, ceapa + morcovul 5 min, ciupercile + ardeiul, roșiile pasate + apă cât să acopere, boia, cimbru, dafin. La foc mic 60 min (25 la oala sub presiune). Mămăliga proaspăt, 10 min. Salata: varză roșie tăiată fin frecată cu sare + oțet, mere julienne, restul de ulei.",
 "Fără telemea peste mămăligă — regula: nu amestecăm lactate cu carne.")
rec("P3","Doradă la cuptor cu fasole verde cu usturoi, salată de rucola, quinoa și sos de lămâie cu mărar 🐟","Doradă cu quinoa","cină","25′","1 zi (rece)",
 [("Proteină",[("dorada",200,240)]),
  ("Legume",[("fasole_verde",150,150),("rucola",40,40),("rosii",80,80),("usturoi",3,3)]),
  ("Amidon",[("quinoa",55,60)]),
  ("Sos",[("lamaie",10,10),("usturoi",2,2)]),("Grăsimi",[("ulei",12,12)])],
 "Dorada (întreagă, curățată, sau file) cu lămâie + usturoi + ½ din ulei, 18–20 min la 200 °C. Quinoa fiartă 15 min (1:2 apă). Fasolea verde 5 min în apă clocotită, apoi 1 min în tigaie cu usturoi și ulei. Rucola cu roșii cherry și un strop de lămâie. Sos: lămâie + ½ din ulei + mărar tocat + usturoi.",
 "Se face ×2, proaspăt. Cântărită ca file (la pește întreg, ~½ din greutate e carne). Merge la fel cu chefal, păstrăv sau — mai rar — somon (+150 kcal).")
rec("P4","Salată de ton cu năut, legume crude și vinegretă de muștar 🐟","Salată de ton","prânz","10′ (fără gătit)","2 zile",
 [("Proteină",[("ton",110,140)]),
  ("Legume",[("castravete",70,70),("ardei",50,50),("rosii",80,80),("salata",50,50),("ceapa",20,20)]),
  ("Amidon",[("naut",150,180)]),
  ("Sos",[("mustar",8,8),("lamaie",10,10)]),("Grăsimi",[("ulei",10,10),("masline",15,15)]),("Amidon ",[("paine",40,40)])],
 "Totul amestecat; tonul scurs, rupt cu furculița deasupra, măslinele felii. Dressing: muștar + lămâie + ulei + mărar, bătute cu furculița. Pâinea alături.",
 "Ridichi — doar la cine le vrea. Săpt. 2: 60 g linte uscată fiartă în loc de năut. Tonul e pește slab — omega-3 vine de la doradă / păstrăv / chefal, la cinele de marți.")
rec("P5","Chili de linte cu pui tocat, avocado și salată de castraveți","Chili de linte cu pui","prânz/cină","45′ (10 activ)","4 zile · congelator",
 [("Proteină",[("pui_tocat",150,190)]),
  ("Legume",[("ceapa",50,50),("ardei",60,60),("morcov",50,50),("castravete",100,100)]),
  ("Amidon",[("linte",65,75)]),
  ("Sos",[("rosii_pasate",150,150),("lamaie",5,5)]),("Grăsimi",[("ulei",5,6),("avocado",50,50)])],
 "Carnea rumenită în ulei, ceapa + ardeiul + morcovul 5 min, lintea + roșiile + apă (2 degete peste), chimion, boia afumată, usturoi, oregano, chili. La foc mic 30–35 min. Alături: castravete felii cu lămâie, mărar și sare. Avocado cuburi peste chili la servire.",
 "Se face ×8 — jumătate la congelator. Piept de pui tocat acasă sau la măcelar; pui tocat comercial: +35 kcal, −8 g P.")
rec("P6","Paste integrale cu pui, sos de roșii cu dovlecel și salată de rucola cu roșii cherry","Paste cu pui și dovlecel","prânz/cină","30′","3 zile",
 [("Proteină",[("pui_piept",150,190)]),
  ("Legume",[("dovlecel",150,150),("ceapa",40,40),("rucola",40,40),("rosii",80,80)]),
  ("Amidon",[("paste_int",70,75)]),
  ("Sos",[("rosii_pasate",150,150)]),("Grăsimi",[("ulei",8,9),("masline",15,15)])],
 "Puiul fâșii rumenit, scos. Ceapa + dovlecelul 5 min, roșiile pasate, busuioc, oregano, usturoi, 10 min. Puiul înapoi. Pastele al dente, amestecate în sos; măsline felii deasupra. Rucola + roșii cherry cu lămâie alături.", "")
rec("P7","Cotlet de porc cu piure de conopidă și morcov, cartofi copți și salată de varză","Cotlet de porc cu piure de conopidă","prânz/cină","40′","3 zile (salata proaspăt)",
 [("Proteină",[("porc_cotlet",150,190)]),
  ("Legume",[("conopida",150,150),("morcov",80,80),("varza",120,120)]),
  ("Amidon",[("cartof",180,210)]),
  ("Sos",[("mustar",8,8)]),("Grăsimi",[("ulei",10,12)])],
 "Conopida + morcovul fierte 15 min, pasate cu ½ din ulei + puțină apă de la fiert + usturoi + nucșoară → piure cremos. Cartofii felii cu rozmarin la cuptor, 25 min la 200 °C. Cotletul bătut subțire, condimentat, 3–4 min pe parte în tigaie încinsă; muștar deasupra. Salata: varză frecată cu sare, oțet, chimen, ulei.",
 "Piureul merge și cu broccoli în loc de morcov.")
rec("P8","Curry de pui cu conopidă, spanac și năut, orez basmati","Curry de pui cu năut","prânz/cină","35′","3 zile",
 [("Proteină",[("pui_piept",150,190)]),
  ("Legume",[("conopida",120,120),("spanac",80,80),("ceapa",50,50),("rosii",60,60)]),
  ("Amidon",[("orez_alb",55,60),("naut",80,80)]),
  ("Sos",[("cocos_light",50,60)]),("Grăsimi",[("ulei",5,6)])],
 "Ceapa + ghimbir + usturoi în ulei, curry + turmeric + chimion 1 min, puiul 5 min, roșiile + laptele de cocos + conopida + năutul, 15 min. Spanacul la final, 2 min. Orezul fiert separat. Coriandru deasupra.", "")
rec("P10","Chiftele de pui la cuptor cu salată grecească, orez brun și sos de tahini","Chiftele de pui cu orez brun","prânz/cină","45′","3 zile (salata proaspăt)",
 [("Proteină",[("pui_piept",150,190),("ovaz",15,15)]),
  ("Legume",[("rosii",100,100),("castravete",100,100),("ceapa",30,30),("ardei",50,50)]),
  ("Amidon",[("orez_brun",55,60)]),
  ("Sos",[("tahini",12,12),("lamaie",10,10),("usturoi",3,3)]),("Grăsimi",[("masline",20,20),("ulei",8,9)])],
 "Pieptul tocat (acasă sau la măcelar) cu ovăz, ceapă rasă, usturoi, pătrunjel → chiftele, 20–25 min la 200 °C. Orezul brun 30 min. Salata: roșii, castravete, ceapă roșie, ardei, măsline, oregano, ulei. Sos: tahini + lămâie + usturoi + apă.",
 "Măslinele se pun în farfurie, nu în salata comună.")
rec("P11","Mușchi de porc la grătar cu piure de broccoli și dovlecel, hrișcă și sos de roșii cu busuioc","Mușchi de porc cu piure de broccoli","prânz/cină","30′","3 zile",
 [("Proteină",[("porc_muschi",160,200)]),
  ("Legume",[("broccoli",150,150),("dovlecel",120,120),("ceapa",30,30)]),
  ("Amidon",[("hrisca",55,60)]),
  ("Sos",[("rosii_pasate",100,100)]),("Grăsimi",[("ulei",8,10),("seminte_dovleac",10,10)])],
 "Broccoli + dovlecelul fierte 8 min la abur, pasate cu ½ din ulei, usturoi, lămâie, sare → piure verde. Hrișca fiartă 15 min. Mușchiul de porc medalioane de 2 cm, condimentat (boia, cimbru, usturoi), 3–4 min pe parte pe grătar/tigaie încinsă. Sos: roșii pasate încălzite cu ceapă și busuioc, 5 min. Semințe de dovleac peste piure.",
 "Merge și cu cotlet de porc sau piept de pui. Piureul merge și din conopidă + mazăre.")
rec("P12","Stir-fry de vită cu broccoli, ardei, ciuperci și varză, orez basmati, sos soia-ghimbir, caju","Stir-fry de vită","prânz/cină","25′","2 zile",
 [("Proteină",[("vita",150,190)]),
  ("Legume",[("broccoli",100,100),("ardei",70,70),("ciuperci",50,50),("varza",60,60),("ceapa_verde",20,20)]),
  ("Amidon",[("orez_alb",55,60)]),
  ("Sos",[("soia",15,15),("usturoi",3,3)]),("Grăsimi",[("ulei",8,8),("caju",15,20)])],
 "Tigaie foarte încinsă; vita fâșii 2 min, scoasă. Broccoli + ardeiul întâi, apoi ciupercile + varza, 5–6 min. Vita înapoi, soia + usturoi + ghimbir, 1 min. Ceapă verde și caju deasupra.", "")
rec("P13","Păstrăv la cuptor cu legume ratatouille, cartofi și sos de lămâie cu usturoi 🐟","Păstrăv cu ratatouille","cină","35′","1 zi (rece)",
 [("Proteină",[("pastrav",180,220)]),
  ("Legume",[("vinete",80,80),("dovlecel",80,80),("ardei",60,60),("ceapa",40,40),("rosii",60,60)]),
  ("Amidon",[("cartof",250,280)]),
  ("Sos",[("lamaie",10,10),("usturoi",3,3)]),("Grăsimi",[("ulei",10,12)])],
 "Cartofii felii cu ½ ulei + rozmarin, 20 min la 200 °C. Legumele cuburi cu restul de ulei + cimbru, în aceeași tavă, + păstrăvul cu lămâie și usturoi deasupra, încă 15–18 min. Sos: lămâie + ulei + usturoi + mărar (se toarnă peste pește la servire).",
 "Se face ×2, proaspăt. Merge la fel cu chefal sau doradă. Ridichi — doar la cine le vrea.")

# ---------- calendar ----------
PLAN = [
 ("Luni","🥚","MD1","P5","G1","P1"),("Marți","🏋️","MD2","P1","G3","P3"),("Miercuri","🥚","MD4","P4","G2","P2"),
 ("Joi","🏋️","MD3","P2","G3","P6"),("Vineri","🥚","MD1","P6","G1","P7"),("Sâmbătă","","MD2","P7","G2","P8"),
 ("Duminică","🥚","MD4","P8","G1","P10"),
 ("Luni","","MD3","P10","G2","P11"),("Marți","🥚🏋️","MD1","P11","G3","P13"),("Miercuri","","MD2","P4","G1","P12"),
 ("Joi","🥚🏋️","MD4","P12","G3","P5"),("Vineri","","MD3","P5","G2","P1"),("Sâmbătă","🥚","MD1","P1","G1","P6"),
 ("Duminică","","MD2","P6","G2","P10"),
]
TARGET = {"S":(2200,150,65,255),"M":(2400,180,75,250)}

def totals(size):
    out=[]
    for d in PLAN:
        s=[0.0]*5
        for m in d[2:]:
            t=macro(R[m][size])
            for i in range(5): s[i]+=t[i]
        out.append(s)
    return out
def plants(week):
    ks=set()
    for d in PLAN[week*7:week*7+7]:
        for m in d[2:]:
            for k,_ in R[m]["S"]:
                if CAT[k] in PLANT_CATS and k not in NOT_PLANT: ks.add(k)
    return ks

if __name__=="__main__":
    for id,r in R.items():
        s,m=macro(r["S"]),macro(r["M"])
        print(f"{id:4s} {r['scurt']:34s} S {r5(s[0]):4d} P{s[1]:3.0f} G{s[2]:3.0f} C{s[3]:3.0f} F{s[4]:3.0f}  M {r5(m[0]):4d} P{m[1]:3.0f} G{m[2]:3.0f} C{m[3]:3.0f} F{m[4]:3.0f}")
    for size,who in (("S","Ema"),("M","Adi")):
        print(who)
        T=totals(size); avg=[sum(x[i] for x in T)/14 for i in range(5)]
        for d,t in zip(PLAN,T): print(f"  {d[0]:9s} {t[0]:5.0f} P{t[1]:4.0f} G{t[2]:3.0f} C{t[3]:4.0f} F{t[4]:3.0f}")
        print(f"  MEDIE     {avg[0]:5.0f} P{avg[1]:4.0f} G{avg[2]:3.0f} C{avg[3]:4.0f} F{avg[4]:3.0f}   tinta {TARGET[size]}")
    for w in (0,1):
        p=plants(w); print(f"Plante săpt. {w+1}: {len(p)}", sorted(p))
