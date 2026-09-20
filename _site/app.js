/* Meniul, rețetele și alimentele vin din _site/data.js, scris de date/genereaza.py direct din
   date/plan.db (baza de date a aplicației, sursa unică de adevăr). Site-ul n-are date proprii
   și nu mai citește fișierele .md: el desenează exact structura primită. */
(function () {
  "use strict";

  const SHORT = { Luni: "Lu", Marți: "Ma", Miercuri: "Mi", Joi: "Jo", Vineri: "Vi", Sâmbătă: "Sâ", Duminică: "Du" };
  const PEOPLE = { ema: "Ema", adi: "Adi" };

  // ---------- încărcare ----------
  // window.MENIU[cine] = [{ n, days:[{ name, tags, total, meals:[{ icon, type, name, total, ing }] }] }]
  // Totul e gata calculat în Python; aici doar așezăm mesele în ordinea de pe card.
  function incarca(who) {
    const sapt = (window.MENIU && window.MENIU[who]) || [];
    sapt.forEach((w) => w.days.forEach((d) => d.meals.sort((a, b) => (ORDER[a.type] ?? 9) - (ORDER[b.type] ?? 9))));
    return sapt;
  }

  // ---------- stare ----------
  // Cum arată la prima deschidere (până când cineva atinge butoanele): meniul Emei,
  // cu Macro pornit și Ingredientele oprite. Pe urmă contează ce a ales el, salvat în browser.
  const IMPLICIT = { view: "ema", macro: true, ing: false, micro: false };
  const state = { page: "meniu", view: IMPLICIT.view, week: 0, allIng: IMPLICIT.ing, macro: IMPLICIT.macro, micro: IMPLICIT.micro, printLook: false };
  const PAGES = ["meniu", "retete", "alimente"];
  // „caietul îngust", doar cu rețete: index.html?caiet=retete
  // Aceleași cartonașe ca în caietul mare de print, dar foaia e cât o TREIME de A4 culcat
  // (99 × 210 mm, adică exact lățimea unei coloane de rețete). Pe telefon iese cât ecranul,
  // deci se citește derulând, fără zoom. Vezi blocul „caiet-retete" din style.css.
  const CAIET = /[?&]caiet=retete(?:&|$)/.test(location.search);
  // ordinea meselor pe card: mic dejun, prânz, cină, apoi (cu spațiu) gustarea
  const ORDER = { "Mic dejun": 0, "Prânz": 1, "Cină": 2, "Gustare": 3 };
  const g = (x) => `${+x}g`;
  const macroLong = (t) => `Pr:<b>${g(t.p)}</b>, Gr:<b>${g(t.g)}</b>, Ca:<b>${g(t.c)}</b>, Fi:<b>${g(t.f)}</b>`;
  const macroShort = (t) => `P:${g(t.p)}, G:${g(t.g)}, C:${g(t.c)}, F:${g(t.f)}`;
  const data = {};
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // al cui meniu se deschide: hash-ul din link > ultima alegere salvată în browser > Ema
  const store = {
    get(k) { try { return localStorage.getItem("meniu." + k); } catch (_) { return null; } },
    set(k, v) { try { localStorage.setItem("meniu." + k, v); } catch (_) { /* browser fără storage */ } }
  };
  function readHash() {
    const saved = store.get("view");
    // „null” = n-a fost atins niciodată butonul → rămâne valoarea implicită
    const salvat = (k, implicit) => { const v = store.get(k); return v === null ? implicit : v === "1"; };
    state.macro = salvat("macro", IMPLICIT.macro);
    state.allIng = salvat("ing", IMPLICIT.ing);
    state.micro = salvat("micro", IMPLICIT.micro);
    if (saved && PEOPLE[saved] || saved === "comun") state.view = saved;
    // #ema/2 = persoana + săptămâna; opțional /i (ingrediente) /m (macro) /p (doar cardurile, ambele săptămâni — pentru printat/poză)
    const m = /^#(ema|adi|comun)(?:\/([12]))?((?:\/[imp])*)/.exec(location.hash);
    if (m) {
      state.page = "meniu";
      state.view = m[1]; if (m[2]) state.week = +m[2] - 1;
      if (m[3]) { state.allIng = m[3].includes("i"); state.macro = m[3].includes("m"); state.printLook = m[3].includes("p"); }
      return;
    }
    // #retete / #alimente — celelalte două pagini
    const pg = /^#(retete|alimente)/.exec(location.hash);
    state.page = pg ? pg[1] : "meniu";
  }
  function writeHash() {
    if (state.printLook) return;
    history.replaceState(null, "", state.page === "meniu" ? `#${state.view}/${state.week + 1}` : `#${state.page}`);
  }

  // ---------- randare ----------
  const persons = () => (state.view === "comun" ? ["ema", "adi"] : [state.view]);

  function bar(t, who) {
    const kp = t.p * 4, kg = t.g * 9, kc = t.c * 4, s = kp + kg + kc || 1;
    return `<div class="brow p-${who}">
      <div class="bar" title="${PEOPLE[who]}: proteine / grăsimi / carbohidrați">
        <i style="width:${(kp / s * 100).toFixed(1)}%"></i><i style="width:${(kg / s * 100).toFixed(1)}%"></i><i style="width:${(kc / s * 100).toFixed(1)}%"></i>
      </div>
      <div class="mac"><span>P <b>${t.p}</b></span><span>G <b>${t.g}</b></span><span>C <b>${t.c}</b></span><span>F <b>${t.f}</b></span></div>
    </div>`;
  }

  // ---------- micronutrienții (butonul „Micronutrienți", implicit oprit) ----------
  // Valorile vin gata socotite din data.js, în ordinea din window.MICRO; aici doar le
  // împerechem cu eticheta scurtă și unitatea. Se arată pe trei nivele: ingredient, masă
  // și zi — iar procentul din DZR apare DOAR pe zi, fiindcă DZR-ul e o doză zilnică;
  // pus la o masă sau la un ingredient ar spune ceva ce nu înseamnă nimic.
  const microCap = () => window.MICRO || [];
  function microLinie(vals, cls) {
    const M = microCap();
    if (!M.length) return "";
    if (!vals) return `<span class="mic ${cls} gol">fără valori în USDA</span>`;
    return `<span class="mic ${cls}">` + vals.map((v, i) =>
      `<span><i>${esc(M[i].s)}</i>${esc(v)}<u>${esc(M[i].u)}</u></span>`).join("") + "</span>";
  }

  function ingredientRow(rows, ps, detail) {
    // rows: [{who, ing}] — aceeași poziție în listă la fiecare persoană
    const first = rows.find((r) => r.ing) || {};
    const name = first.ing ? first.ing.name : "";
    if (ps.length === 1) {
      const i = first.ing;
      // kcal la fiecare ingredient: verde, dar NEîngroșat — bold rămâne doar la Total (masă/zi)
      if (detail) return `<li><span class="q">${esc(i.qty)}</span><span class="u">${i.unit}</span><span class="n">${esc(name)}</span><span class="c">${+i.p}</span><span class="c">${+i.g}</span><span class="c">${+i.c}</span><span class="c">${+i.f}</span><span class="k">${i.k}</span></li>`;
      return `<li><span class="q">${esc(i.qty)}</span><span class="u">${i.unit}</span><span class="n">${esc(name)}</span><span class="k"><b>${i.k}</b></span><span class="m">${macroShort(i)}</span>${microLinie(i.m, "ing")}</li>`;
    }
    const q = rows.map((r) => `<span class="q p-${r.who}">${r.ing ? esc(r.ing.qty) : "—"}</span><span class="u p-${r.who}">${r.ing ? r.ing.unit : ""}</span>`).join("");
    const k = rows.map((r) => `<b class="p-${r.who}">${r.ing ? r.ing.k : "—"}</b>`).join(" / ");
    const tip = rows.map((r) => r.ing ? `${PEOPLE[r.who]}: ${macroShort(r.ing)}` : "").filter(Boolean).join(" | ");
    return `<li title="${esc(tip)}">${q}<span class="n">${esc(name)}</span><span class="k">${k}</span></li>`;
  }

  function mealHtml(idx, ps, days, detail) {
    const ref = days[ps[0]].meals[idx];
    if (!ref) return "";
    const kc = ps.map((w) => { const m = days[w].meals[idx]; return `<b class="p-${w}">${m ? m.total.k : "—"}</b>`; }).join("");
    const mt = ps.map((w) => { const m = days[w].meals[idx]; if (!m) return ""; const t = m.total;
      return `<span class="p-${w}">${macroLong(t)}</span>`; }).join("");
    const n = Math.max(...ps.map((w) => (days[w].meals[idx] || { ing: [] }).ing.length));
    let rows = "";
    for (let i = 0; i < n; i++) {
      const cells = ps.map((w) => {
        const m = days[w].meals[idx];
        let ing = m && m.ing[i];
        // dacă ordinea diferă între persoane, caută după nume
        if (ing && m !== ref && ref.ing[i] && ing.name !== ref.ing[i].name) ing = m.ing.find((x) => x.name === ref.ing[i].name) || ing;
        return { who: w, ing };
      });
      rows += ingredientRow(cells, ps, detail);
    }
    // în modul detaliat, un rând de cap de tabel pentru coloanele de macro
    if (detail) {
      const t = ref.total;
      rows = `<li class="hd"><span></span><span></span><span class="n"></span><span class="c">P</span><span class="c">G</span><span class="c">C</span><span class="c">F</span><span class="k">kcal</span></li>` + rows
        + `<li class="tot"><span class="e"></span><span class="n">Total</span><span class="c">${t.p}</span><span class="c">${t.g}</span><span class="c">${t.c}</span><span class="c">${t.f}</span><span class="k"><b>${t.k}</b></span></li>`;
    }
    // totalul de micronutrienți al mesei: un rând sub macro-uri, în afara butonului
    // (rămâne la vedere și când masa e închisă, exact ca linia de macro)
    const micm = ps.map((w) => { const m = days[w].meals[idx];
      return m ? `<div class="micm p-${w}">${ps.length > 1 ? `<em>${PEOPLE[w]}</em>` : ""}${microLinie(m.m, "masa")}</div>` : ""; }).join("");
    return `<li class="meal t-${ORDER[ref.type] ?? 9}">
      <button class="mh" type="button" aria-expanded="false">
        <span class="nm" title="${esc(ref.type)}">${esc(ref.name)}</span>
        <span class="kc">${kc}</span>
        <span class="mt">${mt}</span>
      </button>
      ${micm}
      <div class="ing"><ul class="${ps.length > 1 ? "two" : detail ? "det" : ""}">${rows}</ul></div>
    </li>`;
  }

  function dayHtml(d, wi, ps, detail) {
    const days = {}; ps.forEach((w) => { days[w] = data[w][wi].days[d]; });
    const ref = days[ps[0]];
    const kc = ps.map((w) => `<span class="kc p-${w}"><b>${days[w].total.k}</b> <small>kcal</small></span>`).join("");
    const bars = ps.map((w) => bar(days[w].total, w)).join("");
    const n = Math.max(...ps.map((w) => days[w].meals.length));
    let meals = "";
    for (let i = 0; i < n; i++) meals += mealHtml(i, ps, days, detail);
    // În modul detaliat (paginile de print), pe banda verde a zilei stă totalul ei: două rânduri
    // — capul de coloane (P / G / C / F / kcal) și, dedesubt, cifrele — așezate exact peste
    // coloanele de macro ale ingredientelor. Alinierea o ține CSS-ul: banda folosește aceleași
    // lățimi fixe de coloană ca `ul.det` (vezi --det-n / --det-k din style.css).
    const dtot = detail ? (() => { const t = ref.total;
      return `<span class="c r1">P</span><span class="c r1">G</span><span class="c r1">C</span><span class="c r1">F</span><span class="k r1">kcal</span>`
        + `<span class="c r2">${t.p}</span><span class="c r2">${t.g}</span><span class="c r2">${t.c}</span><span class="c r2">${t.f}</span><span class="k r2"><b>${t.k}</b></span>`;
    })() : "";
    // Al treilea rând al benzii, pe toată lățimea cardului: vitaminele zilei, toate 13 pe
    // un rând. O vitamină = numele · cât la sută din DZR a strâns ziua · DZR-ul, ca să se
    // citească „cât din cât" · o liniuță încărcată până la acel procent.
    // Două cifre, nu trei: cantitatea strânsă ar fi chiar pct × DZR, deci n-o mai scriem.
    // Liniuța e plină la 100% și rămâne plină peste — cifra spune cât e de fapt.
    // Numele și cifrele stau pe ACEEAȘI linie, cu liniuța dedesubt — așa banda ține într-un
    // rând mai puțin de fiecare grup. Vitaminele și mineralele sunt despărțite vizibil: sunt
    // două feluri de lucruri, iar fără despărțire lista de 23 se citește ca o înșiruire.
    const vitz = detail && ref.vit ? `<div class="vitz">
      ${ref.vit.map((v, i) => (i === 0
          ? `<span class="vzl">Vitamine${ref.vitPartial ? "*" : ""} — azi / DZR</span>`
          : (v.vit !== ref.vit[i - 1].vit ? `<span class="vzl vzl2">Minerale</span>` : ""))
        + `<span class="vz${v.pct === null ? " fara" : (v.pct >= 100 ? " full" : "")}">
        <span class="vzd"><em>${esc(v.n)}</em><b>${esc(v.v)}</b>${v.dzr === null ? "" : "/" + esc(v.dzr)}<i>${esc(v.u)}</i></span>
        ${v.pct === null ? "" : `<span class="vzb" style="--f: ${Math.min(v.pct, 100)}%"></span>`}
      </span>`).join("")}
    </div>` : "";
    // micronutrienții zilei: singurul loc unde are rost procentul din DZR, fiindcă DZR-ul
    // e o doză ZILNICĂ. Verde = ziua acoperă, ocru = nu; sodiul n-are procent (e plafon).
    const micz = ps.map((w) => {
      const zi = days[w], M = microCap();
      if (!M.length || !zi.m) return "";
      const cel = zi.m.map((v, i) => {
        const p = zi.mpct[i];
        return `<span class="mz${p === null ? "" : (p >= 100 ? " ok" : " sub")}">`
          + `<b>${esc(M[i].n)}</b><i>${esc(v)}${esc(M[i].u)}</i>`
          + `<u>${p === null ? "—" : p + "%"}</u></span>`;
      }).join("");
      return `<div class="micz p-${w}"><h3>Micronutrienți${ps.length > 1 ? ` — ${PEOPLE[w]}` : ""}
        <small>cât a strâns ziua · % din DZR</small></h3><div class="mzg">${cel}</div></div>`;
    }).join("");
    return `<article class="day" id="day-${wi}-${d}" data-i="${d}">
      <header class="dh"><h2>${ref.name}${ref.tags ? ` <span class="tags">${esc(ref.tags)}</span>` : ""}</h2><div class="dt">${kc}</div>${dtot}${vitz}</header>
      <div class="bars">${bars}</div>
      ${micz}
      <ol class="meals">${meals}</ol>
    </article>`;
  }

  function weekHtml(wi, ps, hidden, prefix = "", range, detail) {
    const w = data[ps[0]][wi];
    const idx = w.days.map((_, i) => i).filter((i) => !range || (i >= range[0] && i <= range[1]));
    const sufix = range ? ` — ${SHORT[w.days[range[0]].name]}–${SHORT[w.days[range[1]].name]}` : "";
    return `<section class="wk" data-w="${wi}"${hidden ? " hidden" : ""}><h2 class="wt">${prefix}Săptămâna ${wi + 1}${sufix}</h2>${idx.map((i) => dayHtml(i, wi, ps, detail)).join("")}</section>`;
  }
  // Ctrl+P tipărește mereu același caiet, indiferent de ce e bifat pe ecran:
  // Ema + Adi cu ingrediente (o săptămână pe pagină) · fiecare persoană cu macro · paginile detaliate.
  // REGULA STRUCTURII: o secțiune `.ps` = exact o foaie tipărită, iar conținutul ei stă într-un
  // singur `.pg`. Așa, când imprimanta ne dă hârtia în picioare (telefoanele Android nu respectă
  // `@page size: landscape`), CSS-ul poate să rotească `.pg` cu 90° și tot iese A4 întors.
  const page = (cls, inner) => `<section class="ps ${cls}"><div class="pg">${inner}</div></section>`;
  function detailPages(who) {
    return data[who].map((_, wi) => [[0, 3], [4, 6]].map((range) => {
      const zile = data[who][wi].days.slice(range[0], range[1] + 1);
      // steluța de la „Vitamine" vine de la zilele cu alimente fără valori în USDA — aceleași
      // trei ca la rețete, deci aceeași notă (vezi NOTA_USDA)
      const stea = zile.some((z) => z.vitPartial);
      return page("v-one p-det", weekHtml(wi, [who], false, `${PEOPLE[who]} — Detaliat — `, range, true)
        + (stea ? `<p class="rnota">${NOTA_USDA}</p>` : ""));
    }).join("")).join("");
  }
  // Paginile de rețete din caiet: numai numele, ingredientele cu cantitatea pentru amândoi
  // (Ema + Adi, adică porția S + porția M — cât pui efectiv în oală) și modul de preparare.
  // Nimic altceva, în afară de o singură linie cu kcal, macro-uri și, secundar, vitaminele.
  //
  // Împărțirea pe pagini: foaia are 3 coloane, iar fiecare rețetă își ia exact înălțimea ei
  // și stă ÎNTREAGĂ într-o singură coloană — niciodată ruptă între două. Pe o pagină intră
  // câte încap: se umple coloana de sus în jos, iar când următoarea rețetă nu mai intră
  // întreagă se trece la coloana următoare; după a treia, foaie nouă. De aceea paginile au
  // numere diferite de rețete — dar nu mai rămâne jumătate de căsuță goală sub cele scurte,
  // cum se întâmpla înainte, cu grila fixă de 6 căsuțe egale.
  //
  // Ca să știm ce încape, trebuie să știm cât e de înalt fiecare card, iar asta se află doar
  // desenându-l. De aceea `masoaraCarduri` le desenează o dată într-o cutie scoasă din ecran
  // (`.rmas` din style.css), le citește înălțimea și le șterge.
  // câte coloane are foaia de rețete: o ia din CSS (`--ret-col`), fiindcă tot de acolo vine
  // și lățimea coloanei din cutia de măsurat — 3 în caietul mare, 1 în cel îngust
  const retCol = () => +getComputedStyle(document.documentElement).getPropertyValue("--ret-col") || 3;

  // câți px are o valoare scrisă în CSS (mm, pt…), ca să putem socoti în aceeași unitate
  function pxDinCss(valoare) {
    const d = document.createElement("div");
    d.style.cssText = "position:absolute;visibility:hidden;height:" + valoare;
    document.body.appendChild(d);
    const px = d.getBoundingClientRect().height;
    d.remove();
    return px;
  }

  // Desenează cardurile în cutia de măsurat și întoarce înălțimile (px) + cât loc are o coloană.
  function masoaraCarduri(carduri) {
    const css = getComputedStyle(document.documentElement);
    const v = (nume) => css.getPropertyValue(nume).trim();
    const box = document.createElement("div");
    box.className = "rmas";
    box.setAttribute("aria-hidden", "true");
    // titlul și nota se măsoară și ele: mănâncă din înălțimea disponibilă pentru coloane
    box.innerHTML = `<h1 class="pt">${TITLU_RETETE}</h1><p class="rnota">${NOTA_USDA}</p>
      <div class="rcol">${carduri.join("")}</div>`;
    document.body.appendChild(box);
    const titlu = box.querySelector(".pt"), nota = box.querySelector(".rnota");
    const cuMargini = (el) => el.getBoundingClientRect().height + parseFloat(getComputedStyle(el).marginBottom || 0)
                                                              + parseFloat(getComputedStyle(el).marginTop || 0);
    const inaltimi = [...box.querySelector(".rcol").children].map((el) => el.getBoundingClientRect().height);
    // nota se pune doar pe paginile cu rețete fără valori USDA, dar îi păstrăm locul pe toate:
    // mai bine un pic de aer în plus decât o pagină care se revarsă
    const disponibil = pxDinCss(`calc(${v("--panza-inalt-tel")} / ${v("--fit")})`) - cuMargini(titlu) - cuMargini(nota);
    box.remove();
    return { inaltimi, disponibil, gap: pxDinCss(v("--ret-gap")) };
  }

  // Umple coloană cu coloană, în ordinea rețetelor. Întoarce [[coloană, …], …] cu indici.
  function impacheteaza(inaltimi, disponibil, gap, nCol) {
    const pagini = [];
    let pag = [], col = [], inalt = 0;
    const inchideColoana = () => {
      pag.push(col); col = []; inalt = 0;
      if (pag.length === nCol) { pagini.push(pag); pag = []; }
    };
    inaltimi.forEach((h, i) => {
      const cuRost = h + (col.length ? gap : 0);
      // nu mai încape întreagă → coloană nouă (dar o rețetă singură rămâne unde e, chiar dacă
      // e mai înaltă decât foaia — altfel am învârti la nesfârșit; azi cea mai înaltă are ~99mm)
      if (col.length && inalt + cuRost > disponibil) inchideColoana();
      inalt += h + (col.length ? gap : 0);
      col.push(i);
    });
    if (col.length) pag.push(col);
    if (pag.length) pagini.push(pag);
    return pagini;
  }

  // în foaia îngustă titlul lung s-ar rupe pe trei rânduri la fiecare pagină
  const TITLU_RETETE = CAIET ? "Rețete — cantități pentru amândoi (Ema + Adi)"
                             : "Rețete — cantitățile pentru amândoi (Ema + Adi), la un loc";
  // aceeași notă peste tot unde se adună vitamine: și la rețete, și pe banda zilei
  const NOTA_USDA = "* laptele, laptele de cocos și mixul de fructe de pădure n-au valori în USDA, deci lipsesc din suma de vitamine.";
  function recipeCard(r) {
    const ing = r.comp.reduce((t, c) => t.concat(c.items), [])
      .filter((i) => i.sm)
      .map((i) => `<li><span class="q">${esc(i.sm)}</span><span class="n">${esc(i.nume)}</span></li>`).join("");
    const t = r.total;
    // spațiu între ele, nu doar margine: altfel linia n-are unde să se rupă și iese din căsuță
    const vit = (r.vit || []).map((v) => `<span>${esc(v.n)}&nbsp;<b>${esc(v.v)}</b>${esc(v.u)}</span>`).join(" ");
    const pasi = (r.pasi || []).map((x) => `<li>${esc(x)}</li>`).join("");
    return `<article class="rp">
      <h2>${esc(r.nume)}${r.vitPartial ? " *" : ""}</h2>
      <p class="rl"><b>${t.k}</b> kcal · P&nbsp;<b>${t.p}</b>g · G&nbsp;<b>${t.g}</b>g · C&nbsp;<b>${t.c}</b>g · Fibre&nbsp;<b>${t.f}</b>g<span class="vt">${vit}</span></p>
      <div class="rc"><ul class="ri">${ing}</ul><ol class="rs">${pasi}</ol></div>
    </article>`;
  }
  function recipePages() {
    const R = window.RETETE || [];
    if (!R.length) return "";
    const carduri = R.map(recipeCard);
    const { inaltimi, disponibil, gap } = masoaraCarduri(carduri);
    return impacheteaza(inaltimi, disponibil, gap, retCol()).map((pag) => {
      const stea = pag.some((col) => col.some((i) => R[i].vitPartial));
      const coloane = pag.map((col) => `<div class="rcol">${col.map((i) => carduri[i]).join("")}</div>`).join("");
      return page("p-ret", `<h1 class="pt">${TITLU_RETETE}</h1>
        <div class="rcols">${coloane}</div>
        ${stea ? `<p class="rnota">${NOTA_USDA}</p>` : ""}`);
    }).join("");
  }
  function printHtml() {
    const ingPages = () => data.ema.map((_, wi) =>
      page("v-comun p-ing", weekHtml(wi, ["ema", "adi"], false, "Ema + Adi — Ingrediente pentru cumpărături — "))).join("");
    const macroPage = (who) => page("v-one p-macro",
      `<h1 class="pt">${PEOPLE[who]} — mese și macronutrienți</h1>` + data[who].map((_, wi) => weekHtml(wi, [who], false)).join(""));
    // ordinea: ingredientele pentru cumpărături (amândoi), apoi fiecare persoană: mesele cu macro, apoi paginile detaliate
    const person = (who) => macroPage(who) + detailPages(who);
    // pagină goală între Ema și Adi (pentru print față-verso); la sfârșit, rețetele
    return ingPages() + person("ema") + page("p-blank", "") + person("adi") + recipePages();
  }

  const bodyClass = () => `pg-${state.page} v-${state.view}${state.allIng ? " all-ing" : ""}${state.macro ? "" : " no-macro"}${state.micro ? " cu-micro" : ""}${state.printLook ? " print-look" : ""}`;
  function render() {
    document.body.className = bodyClass();
    if (!data.ema || !data.ema.length || !data.adi.length) return;   // meniul n-a putut fi citit — mesajul e deja pe ecran
    const weeks = data[persons()[0]];
    const w = weeks[state.week];
    if (!w) { $("#days").innerHTML = `<p class="loading">Nu găsesc săptămâna ${state.week + 1} în fișier.</p>`; return; }
    // toate săptămânile sunt în pagină: pe ecran se vede doar cea aleasă (/p în link le arată pe toate)
    $("#days").innerHTML = weeks.map((_, wi) => weekHtml(wi, persons(), wi !== state.week)).join("");
    $("#print").innerHTML = printHtml();
    $("#chips").innerHTML = w.days.map((d, i) =>
      `<button type="button" data-i="${i}"${i === 0 ? ' class="on"' : ""}>${SHORT[d.name] || d.name}<small>${d.total.k}</small></button>`).join("");
    currentWeekEl().scrollTo({ left: 0 });
    watchDays();
    writeHash();
  }

  // ---------- pagina „Rețete” ----------
  // Lista tuturor rețetelor, una sub alta. La apăsare se deschid ingredientele cu cantitatea
  // (S = porția standard, M = porția mare) și, dedesubt, modul de preparare pas cu pas.
  // Rețeta deschisă se închide fie din capul ei, fie din butonul „Minimizează” de la sfârșit.
  const GRUPE = ["Mic dejun", "Gustări", "Feluri principale"];
  function reteteHtml() {
    const R = window.RETETE || [];
    if (!R.length) return `<p class="loading">Nu găsesc rețetele. Rulează <code>python date/genereaza.py</code> ca să regenerezi <code>_site/data.js</code>.</p>`;
    const grupuri = GRUPE.filter((gr) => R.some((r) => r.grup === gr));
    return `<p class="hint"><span><b>S</b> = porție standard (Ema) · <b>M</b> = porție mare (Adi). Apasă o rețetă ca să vezi ingredientele și modul de preparare.</span></p>` +
      grupuri.map((gr) => `<section class="grup">
        <h2 class="gt">${esc(gr)} <small>${R.filter((r) => r.grup === gr).length}</small></h2>
        <ul class="rlist">${R.filter((r) => r.grup === gr).map(retetaHtml).join("")}</ul>
      </section>`).join("");
  }
  function retetaHtml(r) {
    const linii = r.comp.map((c) => `<li class="el"><span class="n">${esc(c.eticheta)}</span><span class="s"></span><span class="m"></span></li>` +
      c.items.map((i) => `<li><span class="n">${esc(i.nume)}</span><span class="s">${esc(i.s) || "—"}</span><span class="m">${esc(i.m) || "—"}</span></li>`).join("")).join("");
    const zile = (r.zile || []).join(" · ");
    return `<li class="rec" id="r-${esc(r.id)}">
      <button class="rh" type="button" aria-expanded="false">
        <span class="rn">${esc(r.nume)}</span>
        <span class="rk">${r.kcal.s} <small>/</small> ${r.kcal.m}<small> kcal</small></span>
        <span class="rm">${esc(r.timp)}${zile ? ` · ${esc(zile)}` : ""}</span>
      </button>
      <div class="rb">
        ${macroRow(r)}
        <ul class="ring">
          <li class="hd"><span class="n"></span><span class="s">S</span><span class="m">M</span></li>
          ${linii}
        </ul>
        ${prepHtml(r)}
        <div class="rfoot"><button class="mini" type="button">Minimizează rețeta</button></div>
      </div>
    </li>`;
  }
  // rândul cu macronutrienți, la rețeta deschisă: câte P/G/C/Fibre la porția S și la porția M
  function macroRow(r) {
    if (!r.macro) return "";
    const parte = (cls, litera, m) => `<span class="${cls}">${litera} <b>P</b>&nbsp;${g(m.p)} · <b>G</b>&nbsp;${g(m.g)} · <b>C</b>&nbsp;${g(m.c)} · <b>Fibre</b>&nbsp;${g(m.f)}</span>`;
    return `<p class="rmac">${parte("s", "S", r.macro.s)}${parte("m", "M", r.macro.m)}</p>`;
  }
  // modul de preparare, sub ingrediente: pașii numerotați, apoi nota de bucătar / nutriționist
  function prepHtml(r) {
    const pasi = r.pasi || [];
    if (!pasi.length && !r.sfat && !r.varianta) return "";
    return `<div class="prep">
      ${pasi.length ? `<h3>Mod de preparare</h3><ol class="pasi">${pasi.map((x) => `<li>${esc(x)}</li>`).join("")}</ol>` : ""}
      ${r.sfat ? `<p class="sfat"><b>De ce așa:</b> ${esc(r.sfat)}</p>` : ""}
      ${r.varianta ? `<p class="varn"><b>Variante:</b> ${esc(r.varianta)}</p>` : ""}
    </div>`;
  }

  // ---------- pagina „Alimente” ----------
  // Lista de alimente pe categorii (comun/1_ingrediente.md). Doar numele, cu kcal/100 g discret.
  // Restul valorilor — macronutrienții sub kcal, plus vitaminele și mineralele din USDA — stau
  // ascunse sub fiecare aliment: se deschid la apăsare, sau toate odată, din butonul „Valori
  // nutriționale”.
  function alimenteHtml() {
    const A = window.ALIMENTE || [];
    if (!A.length) return `<p class="loading">Nu găsesc lista de alimente. Rulează <code>python date/genereaza.py</code>.</p>`;
    const n = A.reduce((t, c) => t + c.items.filter((i) => i.plan).length, 0);
    const tot = A.reduce((t, c) => t + c.items.length, 0);
    return `<p class="hint"><button class="pill" id="doar-plan" type="button" aria-pressed="true">Doar din meniu</button>
        <button class="pill" id="toti-micro" type="button" aria-pressed="false">Valori nutriționale</button>
        <span><b>${n}</b> din ${tot} alimente · valorile sunt la 100 g</span></p>` +
      A.map((c) => `<section class="grup cat${c.items.some((i) => i.plan) ? "" : " vid"}">
        <h2 class="gt">${c.icon} ${esc(c.cat)} <small>${c.items.filter((i) => i.plan).length}/${c.items.length}</small></h2>
        <ul class="alist">${c.items.map(alimentHtml).join("")}</ul>
      </section>`).join("");
  }
  function alimentHtml(i) {
    return `<li class="${i.plan ? "in" : "out"}">
      <button class="ah" type="button" aria-expanded="false">
        <span class="n">${esc(i.nume)}</span><span class="k">${i.kcal}<small> kcal</small><span class="km">${macroShort(i)}</span></span>
      </button>
      <div class="mic">${microHtml(i)}</div>
    </li>`;
  }
  // window.MICRO = capul de tabel (nume, unitate, vitamină / mineral);
  // i.micro = valorile alimentului, în exact aceeași ordine (null = n-are corespondent în USDA)
  function microHtml(i) {
    const M = window.MICRO || [];
    if (!i.micro || !M.length) return `<p class="mnota">Fără valori în USDA — la alimentul ăsta mergem pe eticheta producătorului, care dă doar calorii și macro-uri.</p>`;
    const cell = (m, k) => `<div class="mrow"><span class="mn ${m.g}">${esc(m.n)}</span><span class="mv">${esc(i.micro[k])}<small>${esc(m.u)}</small></span></div>`;
    return `<div class="mgrid">${M.map(cell).join("")}</div><p class="mnota">la 100 g, din USDA FoodData Central</p>`;
  }

  // ---------- comutarea între pagini ----------
  function applyPage() {
    document.body.classList.remove("pg-meniu", "pg-retete", "pg-alimente");
    document.body.classList.add("pg-" + state.page);
    $("#pane-retete").hidden = state.page !== "retete";
    $("#pane-alimente").hidden = state.page !== "alimente";
    $("#days").hidden = state.page !== "meniu";
    document.querySelectorAll("#pages button").forEach((b) => {
      const on = b.dataset.page === state.page;
      b.classList.toggle("on", on);
      if (on) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
    if (state.page === "retete" && !$("#pane-retete").innerHTML) $("#pane-retete").innerHTML = reteteHtml();
    if (state.page === "alimente" && !$("#pane-alimente").innerHTML) $("#pane-alimente").innerHTML = alimenteHtml();
    mutaPastila();
    scrollTo(0, 0);
    writeHash();
  }

  // ---------- navigare pe telefon ----------
  let io = null;
  const currentWeekEl = () => document.querySelector(`.wk[data-w="${state.week}"]`);
  function watchDays() {
    if (io) io.disconnect();
    const root = currentWeekEl();
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const i = e.target.dataset.i;
        document.querySelectorAll("#chips button").forEach((b) => b.classList.toggle("on", b.dataset.i === i));
      });
    }, { root, threshold: 0.6 });
    root.querySelectorAll(".day").forEach((el) => io.observe(el));
  }

  // ---------- evenimente ----------
  // Pastila colorată de sub „Ema / Amândoi / Adi”: etichetele nu au lățimi egale (altfel
  // „Amândoi” nu încape pe telefoanele înguste), deci îi măsurăm de fiecare dată lățimea și
  // poziția etichetei bifate. Se recalculează și la rotirea ecranului și după ce se încarcă
  // fontul, pentru că atunci se schimbă lățimile.
  let pastilaGata = false;
  function mutaPastila() {
    const seg = $(".who"), th = seg && seg.querySelector(".thumb");
    if (!th || seg.offsetParent === null) return;          // capsula e ascunsă (altă pagină)
    const primul = seg.querySelector("label");
    const bifat = seg.querySelector("input:checked");
    const ales = bifat ? bifat.closest("label") : primul;
    if (!ales || !primul) return;
    if (!pastilaGata) {   // prima așezare e instantanee, nu alunecă de la lățimea din CSS
      pastilaGata = true;
      th.style.transition = "none";
      requestAnimationFrame(() => { th.style.transition = ""; });
    }
    th.style.width = ales.offsetWidth + "px";
    th.style.transform = `translateX(${ales.offsetLeft - primul.offsetLeft}px)`;
  }

  // panoul de opțiuni (Macro / Ingrediente / PDF): pe telefon se deschide din butonul cu
  // linii, pe ecran mare e mereu desfăcut în rând (butonul e ascuns din CSS).
  const opts = () => $("#opts");
  function closeOpts() {
    opts().classList.remove("open");
    $("#opts-btn").setAttribute("aria-expanded", "false");
  }
  // bulina de pe buton: se aprinde doar când afișarea e schimbată față de cea implicită
  // (Macro pornit, Ingrediente oprite) — altfel ar fi aprinsă mereu și n-ar mai spune nimic
  const markOpts = () => opts().classList.toggle("activ",
    state.macro !== IMPLICIT.macro || state.allIng !== IMPLICIT.ing || state.micro !== IMPLICIT.micro);

  function bind() {
    $("#opts-btn").addEventListener("click", (e) => {
      e.stopPropagation();
      const open = opts().classList.toggle("open");
      e.currentTarget.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", (e) => { if (!opts().contains(e.target)) closeOpts(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeOpts(); });

    document.querySelectorAll('input[name="who"]').forEach((r) => r.addEventListener("change", () => { state.view = r.value; store.set("view", r.value); mutaPastila(); render(); }));
    document.querySelectorAll('input[name="week"]').forEach((r) => r.addEventListener("change", () => { state.week = +r.value; render(); }));
    $("#toggle-ing").addEventListener("click", (e) => {
      state.allIng = !state.allIng;
      e.currentTarget.setAttribute("aria-pressed", String(state.allIng));
      document.body.classList.toggle("all-ing", state.allIng);
      store.set("ing", state.allIng ? "1" : "0");
      markOpts();
      // butonul global comandă tot: uită ce era deschis/închis pe fiecare masă în parte
      document.querySelectorAll(".meal.open").forEach((li) => { li.classList.remove("open"); li.querySelector(".mh").setAttribute("aria-expanded", "false"); });
    });
    $("#toggle-macro").addEventListener("click", (e) => {
      state.macro = !state.macro;
      e.currentTarget.setAttribute("aria-pressed", String(state.macro));
      document.body.classList.toggle("no-macro", !state.macro);
      store.set("macro", state.macro ? "1" : "0");
      markOpts();
    });
    $("#toggle-micro").addEventListener("click", (e) => {
      state.micro = !state.micro;
      e.currentTarget.setAttribute("aria-pressed", String(state.micro));
      document.body.classList.toggle("cu-micro", state.micro);
      store.set("micro", state.micro ? "1" : "0");
      markOpts();
    });
    $("#chips").addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      const el = document.getElementById(`day-${state.week}-${b.dataset.i}`);
      if (el) el.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", inline: "start", block: "nearest" });
    });
    $("#days").addEventListener("click", (e) => {
      const btn = e.target.closest(".mh"); if (!btn) return;
      const li = btn.closest(".meal");
      const open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });
    // butonul PDF = Ctrl+P: browserul face PDF-ul din blocul #print, mereu din datele curente
    $("#pdf").addEventListener("click", () => { closeOpts(); window.print(); });
    $("#pages").addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      state.page = b.dataset.page; closeOpts(); applyPage();
    });
    $("#pane-retete").addEventListener("click", (e) => {
      // „Minimizează rețeta": o închide și readuce capul ei în ecran, ca să nu sară pagina
      const mini = e.target.closest(".mini");
      if (mini) {
        const rec = mini.closest(".rec");
        rec.classList.remove("open");
        rec.querySelector(".rh").setAttribute("aria-expanded", "false");
        rec.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "nearest" });
        return;
      }
      const btn = e.target.closest(".rh"); if (!btn) return;
      const rec = btn.closest(".rec");
      const open = !rec.classList.contains("open");
      // o singură rețetă maximizată deodată: pe celelalte deschise le micșorează
      document.querySelectorAll("#pane-retete .rec.open").forEach((el) => {
        if (el === rec) return;
        el.classList.remove("open");
        el.querySelector(".rh").setAttribute("aria-expanded", "false");
      });
      rec.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
      // la maximizare, urcă titlul cât mai sus (sau cât încape, dacă pagina e prea scurtă)
      if (open) rec.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    });
    $("#pane-alimente").addEventListener("click", (e) => {
      const pane = $("#pane-alimente");
      const b = e.target.closest("#doar-plan");
      if (b) {
        const doar = b.getAttribute("aria-pressed") !== "true";
        b.setAttribute("aria-pressed", String(doar));
        pane.classList.toggle("tot", !doar);
        return;
      }
      // „Valori nutriționale": deschide restul valorilor (macro + micro) la toate alimentele deodată
      const mb = e.target.closest("#toti-micro");
      if (mb) {
        const on = mb.getAttribute("aria-pressed") !== "true";
        mb.setAttribute("aria-pressed", String(on));
        pane.classList.toggle("micro", on);
        pane.querySelectorAll(".alist li.open").forEach((li) => {
          li.classList.remove("open");
          li.querySelector(".ah").setAttribute("aria-expanded", "false");
        });
        return;
      }
      // un singur aliment, deschis din rândul lui
      const ah = e.target.closest(".ah"); if (!ah) return;
      const open = ah.closest("li").classList.toggle("open");
      ah.setAttribute("aria-expanded", String(open));
    });
    addEventListener("resize", mutaPastila);
    // fontul schimbă înălțimea cardurilor, deci și împărțirea rețetelor pe pagini:
    // după ce se încarcă, remăsurăm și refacem caietul de print
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => {
      mutaPastila();
      if (data.ema && data.ema.length && data.adi && data.adi.length) $("#print").innerHTML = printHtml();
    });
    window.addEventListener("hashchange", () => { readHash(); syncControls(); render(); applyPage(); });
  }
  function syncControls() {
    const who = document.querySelector(`input[name="who"][value="${state.view}"]`); if (who) who.checked = true;
    $("#toggle-ing").setAttribute("aria-pressed", String(state.allIng));
    $("#toggle-macro").setAttribute("aria-pressed", String(state.macro));
    $("#toggle-micro").setAttribute("aria-pressed", String(state.micro));
    const wk = document.querySelector(`input[name="week"][value="${state.week}"]`); if (wk) wk.checked = true;
    markOpts();
    mutaPastila();
  }

  // ---------- start ----------
  // Caietul îngust: pagina n-are nevoie de meniu, de butoane și de nimic din restul site-ului —
  // doar de cartonașele de rețete, unul sub altul, la lățimea foii.
  function caietRetete() {
    document.documentElement.classList.add("caiet-retete");
    // `@page` e regulă de document: nu se poate scrie pe o clasă. O punem de aici, după
    // style.css, ca să bată `@page`-urile de acolo (A4 landscape și cel de la telefon).
    const st = document.createElement("style");
    st.textContent = "@media print{@page{size:99mm 210mm;margin:4mm}}";
    document.head.appendChild(st);
    const deseneaza = () => { $("#print").innerHTML = recipePages(); };
    deseneaza();
    // fontul schimbă înălțimea cardurilor, deci și împărțirea pe foi — remăsurăm după ce vine
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(deseneaza);
  }

  (function init() {
    if (CAIET) { caietRetete(); return; }
    readHash();
    syncControls();
    document.body.className = bodyClass();
    data.ema = incarca("ema"); data.adi = incarca("adi");
    if (!data.ema.length || !data.adi.length) {
      $("#days").innerHTML = `<p class="loading">Nu am putut citi meniurile. Rulează <code>python date/genereaza.py</code> ca să regenerezi <code>_site/data.js</code>.</p>`;
      bind(); applyPage();   // Rețete și Alimente merg oricum — ele nu depind de meniuri
      return;
    }
    bind();
    render();
    applyPage();
  })();
})();
