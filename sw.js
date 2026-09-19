/* Service worker — ca site-ul să fie instalabil (PWA) și să meargă și fără internet.
   Stă în rădăcină pentru că un service worker poate controla doar folderul lui și
   ce e sub el; din _site/ n-ar putea controla index.html.

   Strategia: „întâi rețeaua, apoi copia locală”. Cât timp e net, vezi mereu ultima
   versiune (regula veche de prospețime rămâne); fără net, se servește ce s-a salvat
   ultima dată. Parametrul „?t=…” din index.html e ignorat la salvare, ca să nu se
   adune câte o copie la fiecare deschidere. */

const VERSIUNE = "plan-sala-v9";
const ESENTIALE = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./_site/style.css",
  "./_site/app.js",
  "./_site/data.js",
  "./_site/icons/icon-192.png",
  "./_site/icons/icon-512.png",
];

// cheia din cache: adresa fără „?t=…”, ca o pagină să aibă o singură copie
const cheie = (cerere) => {
  const u = new URL(cerere.url);
  u.search = "";
  return u.href;
};

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(VERSIUNE)
      // fiecare separat: dacă unul lipsește, restul tot se salvează
      .then((c) => Promise.all(ESENTIALE.map((u) => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((k) => Promise.all(k.filter((n) => n !== VERSIUNE).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (e) => {
  if (e.data === "skipWaiting") self.skipWaiting();
});

self.addEventListener("fetch", (e) => {
  const cerere = e.request;
  if (cerere.method !== "GET") return;

  const u = new URL(cerere.url);

  // fonturile Google: întâi copia locală (nu se schimbă), ca să meargă și offline
  if (u.hostname === "fonts.googleapis.com" || u.hostname === "fonts.gstatic.com") {
    e.respondWith(
      caches.match(cerere).then((copie) => copie || fetch(cerere).then((r) => {
        const clona = r.clone();
        caches.open(VERSIUNE).then((c) => c.put(cerere, clona));
        return r;
      }).catch(() => copie))
    );
    return;
  }

  if (u.origin !== location.origin) return;

  e.respondWith(
    fetch(cerere)
      .then((r) => {
        if (r && r.ok && r.type === "basic") {
          const clona = r.clone();
          caches.open(VERSIUNE).then((c) => c.put(cheie(cerere), clona));
        }
        return r;
      })
      .catch(() =>
        caches.match(cheie(cerere)).then((copie) =>
          copie || (cerere.mode === "navigate" ? caches.match("./index.html") : Response.error())
        )
      )
  );
});
