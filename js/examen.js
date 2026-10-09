// Núcleo del Simulacro: armar el examen, deduplicar, puntuar y medir el tiempo.
// Módulo puro: el reloj («ahora», en ms) y la semilla del azar entran por parámetro.
// Funciona en el navegador (window.Examen) y en Node (module.exports) para las pruebas.
//
// Estructura (como el I examen de I-2025: 6 + 5 + 12 preguntas en 25 min, 40 puntos):
//   selección única 1 punto · falso/verdadero con justificación 2 puntos · respuesta corta 2 puntos
// Puntaje:
//   · F/V verdadero: 2 puntos si lo marca V.
//   · F/V falso: 1 punto por marcar F + 1 por la justificación (autoevaluada).
//   · Respuesta corta: 2 × puntos clave cubiertos / total, redondeado a 0,5 (autoevaluada).
(function (root) {
  "use strict";

  var ESTRUCTURA = {
    25: { seleccion_unica: 6, verdadero_falso: 5, respuesta_corta: 12 },
    40: { seleccion_unica: 10, verdadero_falso: 8, respuesta_corta: 18 },
    60: { seleccion_unica: 14, verdadero_falso: 12, respuesta_corta: 26 }
  };
  var PUNTOS = { seleccion_unica: 1, verdadero_falso: 2, respuesta_corta: 2 };
  var SECCIONES = ["seleccion_unica", "verdadero_falso", "respuesta_corta"];

  // ---------- Deduplicación ----------
  function normalizar(texto) {
    return String(texto || "")
      .toLowerCase()
      .normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/\(\s*\d+\s*puntos?\s*\)/g, " ")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  // Mismo enunciado y misma figura = misma pregunta. (Las 5 de «Normativa» del I-2026
  // comparten texto pero cada una tiene su foto: son preguntas distintas.)
  function claveDedup(p) {
    return normalizar(p.enunciado) + "|" + (p.figura && p.figura.src ? p.figura.src : "");
  }

  // «I-2026» → 20261; «II-2022» → 20222; sin fecha → 0
  function periodoNum(p) {
    var m = /^(I{1,2})-(\d{4})/.exec(p.examen && p.examen.periodo || "");
    return m ? +m[2] * 10 + m[1].length : 0;
  }

  function prioridad(p) {
    return (p.clave === "oficial" ? 1e6 : 0) + (p.origen === "examen" ? 1e5 : 0) + periodoNum(p);
  }

  // Deja una sola pregunta por clave: la de clave oficial y examen más reciente.
  // Conserva el orden de aparición de la primera.
  function deduplicar(preguntas) {
    var mejor = {}, orden = [];
    preguntas.forEach(function (p) {
      var k = claveDedup(p);
      if (!(k in mejor)) { orden.push(k); mejor[k] = p; }
      else if (prioridad(p) > prioridad(mejor[k])) mejor[k] = p;
    });
    return orden.map(function (k) { return mejor[k]; });
  }

  // ---------- Azar con semilla (mulberry32) ----------
  function azar(semilla) {
    var a = semilla >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function barajar(lista, rnd) {
    var a = lista.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1));
      var x = a[i]; a[i] = a[j]; a[j] = x;
    }
    return a;
  }

  // ---------- Armar el examen ----------
  // o: {duracion: 25|40|60, temas: [1,2,3]}. Devuelve {ids, faltan: {tipo: n}}.
  function armar(preguntas, o, semilla) {
    var est = ESTRUCTURA[o.duracion];
    if (!est) throw new Error("Duración no válida: " + o.duracion);
    var temas = o.temas || [1, 2, 3];
    var rnd = azar(semilla);
    var base = deduplicar(preguntas.filter(function (p) {
      return temas.indexOf(p.tema) >= 0 && PUNTOS[p.tipo];
    }));
    var ids = [], faltan = {};
    SECCIONES.forEach(function (tipo) {
      var del_tipo = barajar(base.filter(function (p) { return p.tipo === tipo; }), rnd);
      var n = est[tipo];
      del_tipo.slice(0, n).forEach(function (p) { ids.push(p.id); });
      if (del_tipo.length < n) faltan[tipo] = n - del_tipo.length;
    });
    return { ids: ids, faltan: faltan };
  }

  // ---------- Puntaje ----------
  function esVerdadero(p) {
    for (var i = 0; i < p.opciones.length; i++) {
      if (p.opciones[i].id === p.correcta) return /^verdadero$/i.test(p.opciones[i].texto);
    }
    return false;
  }

  // Texto contra el que se autoevalúa una justificación de falso.
  function claveJustificacion(p) {
    return p.justificacion_oficial || p.explicacion || "";
  }

  // ¿Esta respuesta necesita autoevaluación?
  function necesitaAutoeval(p, resp) {
    resp = resp || {};
    if (p.tipo === "verdadero_falso") {
      return !esVerdadero(p) && resp.op === p.correcta && !!String(resp.justif || "").trim();
    }
    if (p.tipo === "respuesta_corta") return !!String(resp.texto || "").trim();
    return false;
  }

  // resp: SU/VF {op, justif}; RC {texto}. auto: VF {justifOk}; RC {marcados: [índices]}
  function puntaje(p, resp, auto) {
    resp = resp || {};
    auto = auto || {};
    var max = PUNTOS[p.tipo];
    var o = 0;
    if (p.tipo === "seleccion_unica") {
      o = resp.op === p.correcta ? 1 : 0;
    } else if (p.tipo === "verdadero_falso") {
      if (resp.op === p.correcta) {
        o = esVerdadero(p) ? 2 : 1 + (auto.justifOk && String(resp.justif || "").trim() ? 1 : 0);
      }
    } else if (p.tipo === "respuesta_corta") {
      var total = (p.puntos_clave || []).length;
      var m = String(resp.texto || "").trim() ? (auto.marcados || []).length : 0;
      o = total ? Math.round(Math.min(m, total) / total * max * 2) / 2 : 0;
    }
    return { obtenido: o, maximo: max, completo: o >= max };
  }

  // porId: id → pregunta. Devuelve totales, nota sobre 100 y desglose.
  function resultado(porId, estado) {
    var r = { puntos: 0, maximo: 0, nota: 0, partes: {}, items: [] };
    SECCIONES.forEach(function (t) { r.partes[t] = { obtenido: 0, maximo: 0, n: 0 }; });
    estado.ids.forEach(function (id) {
      var p = porId[id];
      var s = puntaje(p, estado.resp[id], estado.auto[id]);
      r.puntos += s.obtenido;
      r.maximo += s.maximo;
      r.partes[p.tipo].obtenido += s.obtenido;
      r.partes[p.tipo].maximo += s.maximo;
      r.partes[p.tipo].n++;
      r.items.push({ id: id, obtenido: s.obtenido, maximo: s.maximo, completo: s.completo });
    });
    r.nota = r.maximo ? Math.round(r.puntos / r.maximo * 1000) / 10 : 0;
    return r;
  }

  // ---------- Estado y tiempo ----------
  function nuevo(preguntas, o, ahora, semilla) {
    var a = armar(preguntas, o, semilla);
    return {
      v: 1,
      duracion: o.duracion,
      temas: (o.temas || [1, 2, 3]).slice(),
      semilla: semilla,
      ids: a.ids,
      faltan: a.faltan,
      inicio: ahora,
      fin: ahora + o.duracion * 60000,
      terminado: null,
      porTiempo: false,
      fase: "examen",          // examen → autoeval → resultado
      pos: 0,
      resp: {},
      auto: {},
      enviados: false
    };
  }

  function restante(estado, ahora) {
    return Math.max(0, estado.fin - ahora);
  }

  function vencido(estado, ahora) {
    return estado.fase === "examen" && ahora >= estado.fin;
  }

  // Cierra el examen. Si ya venció, el tiempo usado es la duración completa.
  function terminar(estado, porId, ahora) {
    var e = JSON.parse(JSON.stringify(estado));
    e.porTiempo = ahora >= e.fin;
    e.terminado = Math.min(ahora, e.fin);
    var hayAuto = e.ids.some(function (id) { return necesitaAutoeval(porId[id], e.resp[id]); });
    e.fase = hayAuto ? "autoeval" : "resultado";
    return e;
  }

  function tiempoUsado(estado) {
    return (estado.terminado == null ? estado.fin : estado.terminado) - estado.inicio;
  }

  function formatoTiempo(ms) {
    var s = Math.ceil(Math.max(0, ms) / 1000);
    var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), seg = s % 60;
    var dd = function (n) { return (n < 10 ? "0" : "") + n; };
    return (h ? h + ":" + dd(m) : m) + ":" + dd(seg);
  }

  var Examen = {
    ESTRUCTURA: ESTRUCTURA,
    PUNTOS: PUNTOS,
    SECCIONES: SECCIONES,
    normalizar: normalizar,
    claveDedup: claveDedup,
    deduplicar: deduplicar,
    armar: armar,
    esVerdadero: esVerdadero,
    claveJustificacion: claveJustificacion,
    necesitaAutoeval: necesitaAutoeval,
    puntaje: puntaje,
    resultado: resultado,
    nuevo: nuevo,
    restante: restante,
    vencido: vencido,
    terminar: terminar,
    tiempoUsado: tiempoUsado,
    formatoTiempo: formatoTiempo
  };

  if (typeof module !== "undefined" && module.exports) module.exports = Examen;
  else root.Examen = Examen;
})(typeof self !== "undefined" ? self : this);
