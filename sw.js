// Service worker: precarga todo para usar la app sin señal.
// La versión del caché viene de js/version.js (APP_VERSION). Para publicar una versión
// nueva, cambiá SOLO esa constante: el navegador detecta el cambio, instala este SW con
// un caché nuevo y, al activarse, borra los cachés viejos de esta app.
importScripts("js/version.js");

var PREFIJO = "pryecto_materiales-";
var CACHE = PREFIJO + self.APP_VERSION;

var ESTATICOS = [
  "./",
  "index.html",
  "css/app.css",
  "js/version.js",
  "js/srs.js",
  "js/store.js",
  "js/datos.js",
  "js/ui.js",
  "js/estudiar.js",
  "js/practicar.js",
  "js/examen.js",
  "js/simulacro.js",
  "js/app.js",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png"
];

function sinCacheHttp(url) {
  return new Request(url, { cache: "reload" });
}

// Baja un JSON, lo guarda en el caché y lo devuelve ya interpretado.
function guardarJson(cache, url) {
  return fetch(sinCacheHttp(url)).then(function (r) {
    if (!r.ok) throw new Error(url + ": " + r.status);
    return cache.put(url, r.clone()).then(function () { return r.json(); });
  });
}

function figuras(lista, destino) {
  (lista || []).forEach(function (x) { if (x.figura && x.figura.src) destino[x.figura.src] = true; });
}

function precargar() {
  return caches.open(CACHE).then(function (cache) {
    return cache.addAll(ESTATICOS.map(sinCacheHttp))
      .then(function () {
        return Promise.all([
          guardarJson(cache, "data/indice.json"),
          guardarJson(cache, "data/fuentes.json"),
          guardarJson(cache, "data/glosario.json")
        ]);
      })
      .then(function (r) {
        var temas = r[0].temas;
        return Promise.all(temas.map(function (t) {
          return Promise.all([guardarJson(cache, t.tarjetas), guardarJson(cache, t.preguntas)]);
        }));
      })
      .then(function (porTema) {
        var imgs = {};
        porTema.forEach(function (par) { figuras(par[0].tarjetas, imgs); figuras(par[1].preguntas, imgs); });
        return cache.addAll(Object.keys(imgs).map(sinCacheHttp));
      });
  });
}

self.addEventListener("install", function (e) {
  e.waitUntil(precargar());
});

// La página pide activar la versión nueva cuando el usuario toca «Actualizar».
self.addEventListener("message", function (e) {
  if (e.data === "activar") self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (claves) {
      return Promise.all(claves.map(function (k) {
        if (k.indexOf(PREFIJO) === 0 && k !== CACHE) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === "navigate") {
    e.respondWith(
      caches.open(CACHE).then(function (c) { return c.match("index.html"); })
        .then(function (r) { return r || fetch(req); })
        .catch(function () { return fetch(req); })
    );
    return;
  }
  e.respondWith(
    caches.open(CACHE).then(function (c) { return c.match(req, { ignoreSearch: true }); })
      .then(function (r) { return r || fetch(req); })
  );
});
