// Núcleo de la sección Progreso: dominio, subtemas débiles, racha, tiempo por día y
// exportar/importar. Módulo puro: recibe los datos y el estado guardado por parámetro.
// Funciona en el navegador (window.Progreso) y en Node (module.exports).
//
// Definiciones:
//   · Dominio: % de ítems (tarjetas + preguntas) cuya última calificación fue «la sabía»
//     o «bien». Lo nunca visto cuenta como no sabido.
//   · Aciertos: % de intentos respondidos «bien» en preguntas (registro.bien / registro.n).
//   · Racha: días seguidos con al menos 1 ítem calificado; si hoy todavía no hay
//     actividad, se cuenta hasta ayer.
(function (root) {
  "use strict";

  var SRS = root && root.SRS ? root.SRS : (typeof require !== "undefined" ? require("./srs.js") : null);
  var APP = "pryecto_materiales";
  var FORMATO = 1;
  var SABIDO = { sabia: true, bien: true };
  var HISTORIAL_MAX = 10;

  function pct(a, b) { return b ? Math.round(a / b * 100) : 0; }

  function nuevoGrupo(extra) {
    var g = { total: 0, vistos: 0, sabidos: 0, intentos: 0, bien: 0 };
    Object.keys(extra || {}).forEach(function (k) { g[k] = extra[k]; });
    return g;
  }

  function sumar(g, reg, esPregunta) {
    g.total++;
    if (!reg) return;
    g.vistos++;
    if (SABIDO[reg.r]) g.sabidos++;
    if (esPregunta) {
      g.intentos += reg.n || 0;
      g.bien += reg.bien || 0;
    }
  }

  function cerrar(g) {
    g.dominio = pct(g.sabidos, g.total);
    g.aciertos = g.intentos ? pct(g.bien, g.intentos) : null;
    return g;
  }

  // Devuelve {global, temas: [{tema, ..., subtemas: [...]}], subtemas: [...]}
  function dominio(tarjetas, preguntas, leerT, leerP) {
    var porSub = {}, porTema = {}, orden = [], global = nuevoGrupo();
    function agregar(it, reg, esPregunta) {
      if (!porSub[it.subtema]) {
        porSub[it.subtema] = nuevoGrupo({ tema: it.tema, subtema: it.subtema });
        orden.push(it.subtema);
      }
      if (!porTema[it.tema]) porTema[it.tema] = nuevoGrupo({ tema: it.tema });
      sumar(porSub[it.subtema], reg, esPregunta);
      sumar(porTema[it.tema], reg, esPregunta);
      sumar(global, reg, esPregunta);
    }
    tarjetas.forEach(function (t) { agregar(t, leerT(t.id), false); });
    preguntas.forEach(function (p) { agregar(p, leerP(p.id), true); });
    orden.sort();
    var subtemas = orden.map(function (k) { return cerrar(porSub[k]); });
    var temas = Object.keys(porTema).map(Number).sort().map(function (n) {
      var g = cerrar(porTema[n]);
      g.subtemas = subtemas.filter(function (s) { return s.tema === n; });
      return g;
    });
    return { global: cerrar(global), temas: temas, subtemas: subtemas };
  }

  // Subtemas con algo visto y menor dominio (empate: menos aciertos; sin aciertos va después).
  function debiles(subtemas, n) {
    return subtemas.filter(function (s) { return s.vistos > 0 && s.dominio < 100; })
      .slice()
      .sort(function (a, b) {
        if (a.dominio !== b.dominio) return a.dominio - b.dominio;
        var aa = a.aciertos == null ? 101 : a.aciertos, ba = b.aciertos == null ? 101 : b.aciertos;
        if (aa !== ba) return aa - ba;
        return a.subtema < b.subtema ? -1 : 1;
      })
      .slice(0, n == null ? 3 : n);
  }

  function sinVer(subtemas) {
    return subtemas.filter(function (s) { return s.vistos === 0; });
  }

  function activo(diario, dia) {
    return !!(diario && diario[dia] && diario[dia].items > 0);
  }

  function racha(diario, hoy) {
    var incluyeHoy = activo(diario, hoy);
    var d = incluyeHoy ? hoy : SRS.sumar(hoy, -1);
    var dias = 0;
    while (activo(diario, d)) { dias++; d = SRS.sumar(d, -1); }
    return { dias: dias, incluyeHoy: incluyeHoy };
  }

  // Últimos n días (el último es hoy): [{dia, min, items}]
  function porDia(diario, hoy, n) {
    var out = [];
    for (var i = (n || 7) - 1; i >= 0; i--) {
      var dia = SRS.sumar(hoy, -i);
      var d = (diario || {})[dia] || { seg: 0, items: 0 };
      out.push({ dia: dia, min: Math.round(d.seg / 60), items: d.items });
    }
    return out;
  }

  // ---------- Exportar / importar ----------
  function vacio() {
    return { tarjetas: {}, preguntas: {}, diario: {}, prefs: {}, simulacro: null, historial: [] };
  }

  function exportar(estado, version, ahora) {
    return {
      app: APP,
      formato: FORMATO,
      version: version,
      exportado: new Date(ahora).toISOString(),
      progreso: JSON.parse(JSON.stringify(estado))
    };
  }

  function esMapaDeRegistros(m) {
    if (!m || typeof m !== "object" || Array.isArray(m)) return false;
    return Object.keys(m).every(function (k) {
      var r = m[k];
      return r && typeof r === "object" && typeof r.r === "string" && typeof r.n === "number";
    });
  }

  // Revisa un objeto leído de un archivo. Devuelve {ok, error, progreso, resumen}.
  function validar(obj) {
    function mal(msg) { return { ok: false, error: msg }; }
    if (!obj || typeof obj !== "object") return mal("El archivo no es un JSON de progreso.");
    if (obj.app !== APP) return mal("El archivo no es un progreso de esta app.");
    if (obj.formato !== FORMATO) return mal("El archivo es de un formato que esta versión no conoce.");
    var p = obj.progreso;
    if (!p || typeof p !== "object") return mal("Al archivo le falta el progreso.");
    if (!esMapaDeRegistros(p.tarjetas || {}) || !esMapaDeRegistros(p.preguntas || {})) {
      return mal("Los registros de tarjetas o preguntas están dañados.");
    }
    if (p.diario && (typeof p.diario !== "object" || Array.isArray(p.diario))) return mal("El registro diario está dañado.");
    if (p.historial && !Array.isArray(p.historial)) return mal("El historial de simulacros está dañado.");
    var limpio = vacio();
    limpio.tarjetas = p.tarjetas || {};
    limpio.preguntas = p.preguntas || {};
    limpio.diario = p.diario || {};
    limpio.prefs = p.prefs && typeof p.prefs === "object" ? p.prefs : {};
    limpio.simulacro = p.simulacro || null;
    limpio.historial = p.historial || [];
    return {
      ok: true,
      progreso: limpio,
      resumen: {
        tarjetas: Object.keys(limpio.tarjetas).length,
        preguntas: Object.keys(limpio.preguntas).length,
        dias: Object.keys(limpio.diario).length,
        simulacros: limpio.historial.length,
        exportado: obj.exportado || null
      }
    };
  }

  function combinarRegistros(a, b) {
    var out = {};
    Object.keys(a || {}).forEach(function (id) { out[id] = a[id]; });
    Object.keys(b || {}).forEach(function (id) {
      if (!out[id] || (b[id].t || 0) > (out[id].t || 0)) out[id] = b[id];
    });
    return out;
  }

  // Combina el progreso actual con uno importado sin perder nada:
  // por ítem queda el registro más reciente; por día, el mayor tiempo y la mayor cantidad.
  function combinar(actual, nuevo) {
    var r = vacio();
    actual = actual || vacio();
    r.tarjetas = combinarRegistros(actual.tarjetas, nuevo.tarjetas);
    r.preguntas = combinarRegistros(actual.preguntas, nuevo.preguntas);
    [actual.diario || {}, nuevo.diario || {}].forEach(function (d) {
      Object.keys(d).forEach(function (dia) {
        var x = r.diario[dia] || { seg: 0, items: 0 };
        r.diario[dia] = { seg: Math.max(x.seg, d[dia].seg || 0), items: Math.max(x.items, d[dia].items || 0) };
      });
    });
    Object.keys(nuevo.prefs || {}).forEach(function (k) { r.prefs[k] = nuevo.prefs[k]; });
    Object.keys(actual.prefs || {}).forEach(function (k) { r.prefs[k] = actual.prefs[k]; });
    r.simulacro = actual.simulacro || nuevo.simulacro || null;
    var vistos = {};
    r.historial = (actual.historial || []).concat(nuevo.historial || []).filter(function (h) {
      var k = [h.fecha, h.duracion, h.nota, h.usado].join("|");
      if (vistos[k]) return false;
      vistos[k] = true;
      return true;
    }).sort(function (a, b) { return a.fecha < b.fecha ? 1 : a.fecha > b.fecha ? -1 : 0; })
      .slice(0, HISTORIAL_MAX);
    return r;
  }

  var Progreso = {
    APP: APP,
    FORMATO: FORMATO,
    dominio: dominio,
    debiles: debiles,
    sinVer: sinVer,
    racha: racha,
    porDia: porDia,
    exportar: exportar,
    validar: validar,
    combinar: combinar,
    vacio: vacio
  };

  if (typeof module !== "undefined" && module.exports) module.exports = Progreso;
  else root.Progreso = Progreso;
})(typeof self !== "undefined" ? self : this);
