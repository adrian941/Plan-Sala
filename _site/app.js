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
  const IMPLICIT = { view: "ema", macro: true, ing: false };
  const state = { page: "meniu", view: IMPLICIT.view, week: 0, allIng: IMPLICIT.ing, macro: IMPLICIT.macro, printLook: false };
  const PAGES = ["meniu", "retete", "alimente"];
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

  function ingredientRow(rows, ps, detail) {
    // rows: [{who, ing}] — aceeași poziție în listă la fiecare persoană
    const first = rows.find((r) => r.ing) || {};
    const name = first.ing ? first.ing.name : "";
    if (ps.length === 1) {
      const i = first.ing;
      if (detail) return `<li><span class="q">${esc(i.qty)}</span><span class="u">${i.unit}</span><span class="n">${esc(name)}</span><span class="c">${+i.p}</span><span class="c">${+i.g}</span><span class="c">${+i.c}</span><span class="c">${+i.f}</span><span class="k"><b>${i.k}</b></span></li>`;
      return `<li><span class="q">${esc(i.qty)}</span><span class="u">${i.unit}</span><span class="n">${esc(name)}</span><span class="k"><b>${i.k}</b></span><span class="m">${macroShort(i)}</span></li>`;
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
    return `<li class="meal t-${ORDER[ref.type] ?? 9}">
      <button class="mh" type="button" aria-expanded="false">
        <span class="nm" title="${esc(ref.type)}">${esc(ref.name)}</span>
        <span class="kc">${kc}</span>
        <span class="mt">${mt}</span>
      </button>
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
    return `<article class="day" id="day-${wi}-${d}" data-i="${d}">
      <header class="dh"><h2>${ref.name}${ref.tags ? ` <span class="tags">${esc(ref.tags)}</span>` : ""}</h2><div class="dt">${kc}</div></header>
      <div class="bars">${bars}</div>
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
    return data[who].map((_, wi) => [[0, 3], [4, 6]].map((range) =>
      page("v-one p-det", weekHtml(wi, [who], false, `${PEOPLE[who]} — Detaliat — `, range, true))).join("")).join("");
  }
  function printHtml() {
    const ingPages = () => data.ema.map((_, wi) =>
      page("v-comun p-ing", weekHtml(wi, ["ema", "adi"], false, "Ema + Adi — Ingrediente pentru cumpărături — "))).join("");
    const macroPage = (who) => page("v-one p-macro",
      `<h1 class="pt">${PEOPLE[who]} — mese și macronutrienți</h1>` + data[who].map((_, wi) => weekHtml(wi, [who], false)).join(""));
    // ordinea: ingredientele pentru cumpărături (amândoi), apoi fiecare persoană: mesele cu macro, apoi paginile detaliate
    const person = (who) => macroPage(who) + detailPages(who);
    return ingPages() + person("ema") + page("p-blank", "") + person("adi");   // pagină goală între Ema și Adi (pentru print față-verso)
  }

  const bodyClass = () => `pg-${state.page} v-${state.view}${state.allIng ? " all-ing" : ""}${state.macro ? "" : " no-macro"}${state.printLook ? " print-look" : ""}`;
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
  // (S = porția standard, M = porția mare) — atât, fără calorii pe ingredient.
  const GRUPE = ["Mic dejun", "Gustări", "Feluri principale"];
  function reteteHtml() {
    const R = window.RETETE || [];
    if (!R.length) return `<p class="loading">Nu găsesc rețetele. Rulează <code>python date/genereaza.py</code> ca să regenerezi <code>_site/data.js</code>.</p>`;
    const grupuri = GRUPE.filter((gr) => R.some((r) => r.grup === gr));
    return `<p class="hint"><span><b>S</b> = porție standard (Ema) · <b>M</b> = porție mare (Adi). Apasă o rețetă ca să vezi ingredientele.</span></p>` +
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
      <div class="rb"><ul class="ring">
        <li class="hd"><span class="n"></span><span class="s">S</span><span class="m">M</span></li>
        ${linii}
      </ul></div>
    </li>`;
  }

  // ---------- pagina „Alimente” ----------
  // Lista de alimente pe categorii (comun/1_ingrediente.md). Doar numele, cu kcal/100 g discret.
  function alimenteHtml() {
    const A = window.ALIMENTE || [];
    if (!A.length) return `<p class="loading">Nu găsesc lista de alimente. Rulează <code>python date/genereaza.py</code>.</p>`;
    const n = A.reduce((t, c) => t + c.items.filter((i) => i.plan).length, 0);
    const tot = A.reduce((t, c) => t + c.items.length, 0);
    return `<p class="hint"><button class="pill" id="doar-plan" type="button" aria-pressed="true">Doar din meniu</button>
        <span><b>${n}</b> din ${tot} alimente · kcal la 100 g</span></p>` +
      A.map((c) => `<section class="grup cat${c.items.some((i) => i.plan) ? "" : " vid"}">
        <h2 class="gt">${c.icon} ${esc(c.cat)} <small>${c.items.filter((i) => i.plan).length}/${c.items.length}</small></h2>
        <ul class="alist">${c.items.map((i) =>
          `<li class="${i.plan ? "in" : "out"}"><span class="n">${esc(i.nume)}</span><span class="k">${i.kcal}</span></li>`).join("")}</ul>
      </section>`).join("");
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
  const markOpts = () => opts().classList.toggle("activ", state.macro !== IMPLICIT.macro || state.allIng !== IMPLICIT.ing);

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
      const btn = e.target.closest(".rh"); if (!btn) return;
      const open = btn.closest(".rec").classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });
    $("#pane-alimente").addEventListener("click", (e) => {
      const b = e.target.closest("#doar-plan"); if (!b) return;
      const doar = b.getAttribute("aria-pressed") !== "true";
      b.setAttribute("aria-pressed", String(doar));
      $("#pane-alimente").classList.toggle("tot", !doar);
    });
    addEventListener("resize", mutaPastila);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(mutaPastila);
    window.addEventListener("hashchange", () => { readHash(); syncControls(); render(); applyPage(); });
  }
  function syncControls() {
    const who = document.querySelector(`input[name="who"][value="${state.view}"]`); if (who) who.checked = true;
    $("#toggle-ing").setAttribute("aria-pressed", String(state.allIng));
    $("#toggle-macro").setAttribute("aria-pressed", String(state.macro));
    const wk = document.querySelector(`input[name="week"][value="${state.week}"]`); if (wk) wk.checked = true;
    markOpts();
    mutaPastila();
  }

  // ---------- start ----------
  (function init() {
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
