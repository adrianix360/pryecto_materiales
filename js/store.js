// Progreso en localStorage. Todo acceso va en try/catch: si el navegador bloquea el
// almacenamiento, la app sigue funcionando en memoria y avisa con discreción.
// La clave lleva el nombre del proyecto porque en GitHub Pages todos los repos del
// usuario comparten el mismo origen (usuario.github.io).
(function () {
  "use strict";

  var CLAVE = "pryecto_materiales:progreso:v1";
  var vacio = function () { return { tarjetas: {}, preguntas: {}, prefs: {} }; };
  var estado = vacio();
  var disponible = true;
  var oyentes = [];

  function avisar() {
    oyentes.forEach(function (f) { try { f(disponible); } catch (e) { /* nada */ } });
  }

  try {
    var ls = window.localStorage;
    var crudo = ls.getItem(CLAVE);
    if (crudo) {
      var leido = JSON.parse(crudo);
      if (leido && typeof leido === "object") {
        estado.tarjetas = leido.tarjetas || {};
        estado.preguntas = leido.preguntas || {};
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

  // r: "sabia" | "dudosa" | "no"
  function calificarTarjeta(id, r) {
    var prev = estado.tarjetas[id] || { n: 0 };
    estado.tarjetas[id] = { r: r, n: prev.n + 1, t: Date.now() };
    guardar();
  }

  // r: "bien" | "parcial" | "mal"; resp: ids marcados (lista o string) o texto escrito
  function responderPregunta(id, r, resp) {
    var prev = estado.preguntas[id] || { n: 0, bien: 0 };
    estado.preguntas[id] = {
      r: r,
      n: prev.n + 1,
      bien: prev.bien + (r === "bien" ? 1 : 0),
      resp: resp,
      t: Date.now()
    };
    guardar();
  }

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
    calificarTarjeta: calificarTarjeta,
    responderPregunta: responderPregunta,
    pref: pref
  };
})();
