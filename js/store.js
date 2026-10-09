// Progreso en localStorage. Todo acceso va en try/catch: si el navegador bloquea el
// almacenamiento, la app sigue funcionando en memoria y avisa con discreción.
// La clave lleva el nombre del proyecto porque en GitHub Pages todos los repos del
// usuario comparten el mismo origen (usuario.github.io).
//
// Estado guardado:
//   tarjetas[id]  = {r, n, t, caja, vence, visto}            (r: sabia | dudosa | no)
//   preguntas[id] = {r, n, t, caja, vence, visto, bien, resp} (r: bien | parcial | mal)
//   diario[AAAA-MM-DD] = {seg, items}   tiempo e ítems calificados ese día
//   prefs = filtros, modo de cada sección y meta diaria
// Los registros viejos (sin caja) se convierten al cargar con SRS.normalizar.
(function () {
  "use strict";

  var CLAVE = "pryecto_materiales:progreso:v1";
  var META_DEFECTO = { unidad: "minutos", valor: 90 };
  var estado = { tarjetas: {}, preguntas: {}, diario: {}, prefs: {} };
  var disponible = true;
  var oyentes = [];

  function avisar() {
    oyentes.forEach(function (f) { try { f(disponible); } catch (e) { /* nada */ } });
  }

  var convertidos = 0;

  function convertir(mapa) {
    var out = {};
    Object.keys(mapa || {}).forEach(function (id) {
      try { out[id] = SRS.normalizar(mapa[id]); } catch (e) { out[id] = mapa[id]; }
      if (out[id] !== mapa[id]) convertidos++;
    });
    return out;
  }

  try {
    var ls = window.localStorage;
    var crudo = ls.getItem(CLAVE);
    if (crudo) {
      var leido = JSON.parse(crudo);
      if (leido && typeof leido === "object") {
        estado.tarjetas = convertir(leido.tarjetas);
        estado.preguntas = convertir(leido.preguntas);
        estado.diario = leido.diario || {};
        estado.prefs = leido.prefs || {};
      }
    }
    ls.setItem(CLAVE + ":prueba", "1");
    ls.removeItem(CLAVE + ":prueba");
  } catch (e) {
    disponible = false;
  }

  function guardar() {
    if (!disponible) return false;
    try {
      window.localStorage.setItem(CLAVE, JSON.stringify(estado));
      return true;
    } catch (e) {
      disponible = false;
      avisar();
      return false;
    }
  }

  if (convertidos) guardar(); // deja guardado el progreso ya convertido

  function pref(clave, valor) {
    if (arguments.length === 1) return estado.prefs[clave];
    estado.prefs[clave] = valor;
    guardar();
  }

  window.Store = {
    clave: CLAVE,
    disponible: function () { return disponible; },
    alCambiarDisponibilidad: function (f) { oyentes.push(f); },
    tarjeta: function (id) { return estado.tarjetas[id] || null; },
    pregunta: function (id) { return estado.preguntas[id] || null; },
    guardarTarjeta: function (id, reg) { estado.tarjetas[id] = reg; guardar(); },
    guardarPregunta: function (id, reg) { estado.preguntas[id] = reg; guardar(); },
    // Suma tiempo (segundos) e ítems calificados al día indicado.
    sumarDia: function (dia, seg, items) {
      var d = estado.diario[dia] || { seg: 0, items: 0 };
      d.seg = Math.round((d.seg + seg) * 10) / 10;
      d.items += items;
      estado.diario[dia] = d;
      guardar();
    },
    dia: function (dia) { return estado.diario[dia] || { seg: 0, items: 0 }; },
    meta: function (nueva) {
      if (nueva) { pref("meta", nueva); return nueva; }
      var m = estado.prefs.meta;
      return m && m.valor > 0 && (m.unidad === "minutos" || m.unidad === "items") ? m : META_DEFECTO;
    },
    pref: pref
  };
})();
