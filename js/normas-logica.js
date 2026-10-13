// Lógica pura del entrenamiento «Normas» (sin DOM ni almacenamiento): ítems, lectura de la
// respuesta escrita, opciones de «¿qué determina?», registro con confusiones y dominio.
// Funciona en el navegador (window.NormasLogica) y en Node (module.exports) para las pruebas.
//
// Cada norma da dos ítems de repaso (cada uno con su registro de repetición espaciada, SRS):
//   «n-C127-e»  escribir: se lee qué determina y se escribe el número de la norma (como en el examen)
//   «n-C127-i»  inversa:  se ve la norma y se elige qué determina entre opciones de normas parecidas
// Registro = registro de SRS + {bien, conf, dias}:
//   conf[otraId] = veces que se confundió con esa norma (otraId «otra» si escribió un número que no está)
//   dias         = (solo en «e») días distintos en que la escribió bien; con 2 o más está «dominada»
(function (root) {
  "use strict";

  var LETRAS = ["C", "D"];
  var DIAS_DOMINIO = 2;
  var OPCIONES_INVERSA = 4;

  function claveE(id) { return "n-" + id + "-e"; }
  function claveI(id) { return "n-" + id + "-i"; }

  // Ítems en el orden de estudio. Cada familia es un bloque de «escribir» (E) y otro de «inversa» (I).
  // Los nuevos del día salen agrupados por familia, y la «inversa» de una familia se atrasa un bloque:
  // E1, E2, I1, E3, I2, … así nunca se pregunta al revés lo que se acaba de ver escribiendo.
  function items(normas, familias) {
    function bloque(f, tipo) {
      return normas.filter(function (n) { return n.familia === f.id; }).map(function (n) {
        return { id: tipo === "e" ? claveE(n.id) : claveI(n.id), norma: n.id, tipo: tipo, verificar: !!n.verificar };
      });
    }
    var out = [];
    familias.forEach(function (f, k) {
      out = out.concat(bloque(f, "e"));
      if (k > 0) out = out.concat(bloque(familias[k - 1], "i"));
    });
    if (familias.length) out = out.concat(bloque(familias[familias.length - 1], "i"));
    return out;
  }

  // «128», «c128», «ASTM C 128», «d-75» → «C128», «C128», «C128», «D75». letra: la elegida en pantalla.
  function parsear(letra, texto) {
    var t = String(texto == null ? "" : texto).toUpperCase();
    var m = t.match(/([CD])\s*[-.]?\s*(\d{1,5})/);
    if (m) return m[1] + m[2];
    var d = t.match(/(\d{1,5})/);
    if (!d) return null;
    return (LETRAS.indexOf(letra) >= 0 ? letra : "C") + d[1];
  }

  // resp: id escrito (o null). Devuelve {ok, conf} con conf = id de la norma con la que se confundió.
  function evaluarEscribir(norma, resp, porId) {
    if (resp === norma.id) return { ok: true, conf: null };
    if (resp && porId[resp]) return { ok: false, conf: resp };
    return { ok: false, conf: resp ? "otra" : null };
  }

  function barajar(lista, azar) {
    var a = lista.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(azar() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  // Opciones de «¿qué determina?»: la correcta y las normas con las que más se confunde, luego las
  // de su familia y al final cualquier otra. Devuelve [{norma, texto}] ya en orden aleatorio.
  function opcionesInversa(norma, normas, porId, azar) {
    azar = azar || Math.random;
    var vistos = {}; vistos[norma.id] = true;
    var textos = {}; textos[norma.mide] = true;
    var elegidas = [];
    function tomar(lista) {
      barajar(lista, azar).forEach(function (n) {
        if (!n || vistos[n.id] || textos[n.mide] || elegidas.length >= OPCIONES_INVERSA - 1) return;
        vistos[n.id] = true; textos[n.mide] = true; elegidas.push(n);
      });
    }
    tomar((norma.confunde_con || []).map(function (id) { return porId[id]; }));
    tomar(normas.filter(function (n) { return n.familia === norma.familia; }));
    tomar(normas);
    var todas = [norma].concat(elegidas).map(function (n) { return { norma: n.id, texto: n.mide }; });
    return barajar(todas, azar);
  }

  // Registro nuevo después de responder. o: {id, hoy, examen, verificar, ahora, conf}.
  // tipo: «e» o «i». No modifica prev.
  function registrar(prev, tipo, ok, o) {
    var reg = root.SRS.aplicar(prev, ok ? "bien" : "mal", {
      id: o.id, hoy: o.hoy, examen: o.examen, verificar: !!o.verificar, ahora: o.ahora
    });
    reg.bien = (prev && prev.bien || 0) + (ok ? 1 : 0);
    var conf = {};
    Object.keys(prev && prev.conf || {}).forEach(function (k) { conf[k] = prev.conf[k]; });
    if (!ok && o.conf) conf[o.conf] = (conf[o.conf] || 0) + 1;
    if (Object.keys(conf).length) reg.conf = conf; else delete reg.conf;
    if (tipo === "e") {
      var dias = (prev && prev.dias || []).slice();
      if (ok && dias.indexOf(o.hoy) < 0) dias.push(o.hoy);
      reg.dias = dias;
    }
    return reg;
  }

  // «Dominada»: la última vez que la escribió salió bien y la escribió bien en 2 días distintos.
  function dominada(regE) {
    return !!regE && regE.r === "bien" && (regE.dias || []).length >= DIAS_DOMINIO;
  }

  // nueva | dominada | riesgo (última falló o sigue en la caja 0 o 1) | camino
  function estadoNorma(regE, regI) {
    if (!regE && !regI) return "nueva";
    if (dominada(regE)) return "dominada";
    var malo = [regE, regI].some(function (r) { return r && (r.r === "mal" || r.caja <= 1); });
    return malo ? "riesgo" : "camino";
  }

  // Parejas confundidas, de la más a la menos fallada: [{a, b, n}] con a < b. «otra» no es pareja.
  function parejas(normas, leer) {
    var mapa = {};
    normas.forEach(function (n) {
      [claveE(n.id), claveI(n.id)].forEach(function (clave) {
        var r = leer(clave);
        Object.keys(r && r.conf || {}).forEach(function (otra) {
          if (otra === "otra") return;
          var par = [n.id, otra].sort();
          var k = par.join("|");
          mapa[k] = mapa[k] || { a: par[0], b: par[1], n: 0 };
          mapa[k].n += r.conf[otra];
        });
      });
    });
    return Object.keys(mapa).map(function (k) { return mapa[k]; })
      .sort(function (x, y) { return y.n - x.n || (x.a + x.b < y.a + y.b ? -1 : 1); });
  }

  // Ítems de estas normas: primero los «escribir» y luego los «inversa», en el orden dado.
  function itemsDe(todos, ids) {
    var orden = {};
    ids.forEach(function (id, i) { orden[id] = i; });
    var sel = todos.filter(function (it) { return orden[it.norma] !== undefined; });
    return sel.sort(function (x, y) {
      if (x.tipo !== y.tipo) return x.tipo === "e" ? -1 : 1;
      return orden[x.norma] - orden[y.norma];
    });
  }

  var NormasLogica = {
    LETRAS: LETRAS,
    DIAS_DOMINIO: DIAS_DOMINIO,
    claveE: claveE,
    claveI: claveI,
    items: items,
    parsear: parsear,
    evaluarEscribir: evaluarEscribir,
    opcionesInversa: opcionesInversa,
    registrar: registrar,
    dominada: dominada,
    estadoNorma: estadoNorma,
    parejas: parejas,
    itemsDe: itemsDe
  };

  if (typeof module !== "undefined" && module.exports) {
    root.SRS = root.SRS || require("./srs.js");
    module.exports = NormasLogica;
  } else root.NormasLogica = NormasLogica;
})(typeof self !== "undefined" ? self : this);
