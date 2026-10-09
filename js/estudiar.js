// Estudiar: tarjetas que se voltean al tocarlas y se califican con tres botones.
// Orden de la ronda: nuevas, luego «no la sabía», «dudosa» y «la sabía» (las más viejas
// primero). Una tarjeta marcada «no» vuelve 4 lugares después; una «dudosa», 8 después.
(function () {
  "use strict";

  var PRIORIDAD = { no: 1, dudosa: 2, sabia: 3 };
  var REINSERTAR = { no: 4, dudosa: 8 };
  var NOMBRES = { sabia: "La sabía", dudosa: "Dudosa", no: "No la sabía" };
  var TIPOS = {
    concepto: "Concepto", dato: "Dato", clasificacion: "Clasificación", formula: "Fórmula",
    norma: "Norma", proceso: "Proceso", equipo: "Equipo", parametros: "Parámetros", criterio: "Criterio"
  };

  var s = { f: null, cola: [], pos: 0, volteada: false, filtrosAbiertos: false, porId: null };

  function filtroInicial() {
    var f = Store.pref("filtroEstudiar") || {};
    return { tema: f.tema || "", subtema: f.subtema || "" };
  }

  function armarCola() {
    var lista = Datos.tarjetas.filter(function (t) { return UI.cumpleFiltro(t, s.f); });
    lista = lista.map(function (t, i) { return { t: t, i: i, p: Store.tarjeta(t.id) }; });
    lista.sort(function (a, b) {
      var pa = a.p ? PRIORIDAD[a.p.r] || 3 : 0;
      var pb = b.p ? PRIORIDAD[b.p.r] || 3 : 0;
      if (pa !== pb) return pa - pb;
      if (a.p && b.p && a.p.t !== b.p.t) return a.p.t - b.p.t;
      return a.i - b.i;
    });
    s.cola = lista.map(function (x) { return x.t.id; });
    s.pos = 0;
    s.volteada = false;
  }

  function render(vista) {
    var html = UI.filtros("est", s.f, false);
    if (!s.cola.length) {
      vista.innerHTML = html + '<p class="vacio">No hay tarjetas con ese filtro.</p>';
      conectar(vista);
      return;
    }
    if (s.pos >= s.cola.length) {
      vista.innerHTML = html +
        '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">Ronda terminada</h2>' +
        "<p>Repasaste las " + new Set(s.cola).size + " tarjetas de este filtro.</p></section>" +
        '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="otra">Empezar otra ronda</button></div>';
      conectar(vista);
      return;
    }

    var t = s.porId[s.cola[s.pos]];
    var prev = Store.tarjeta(t.id);
    var nuevas = s.cola.slice(s.pos).filter(function (id) { return !Store.tarjeta(id); }).length;

    html += '<p class="contador" aria-live="polite">Tarjeta ' + (s.pos + 1) + " de " + s.cola.length +
      (nuevas ? " · " + nuevas + " sin ver" : "") + "</p>";
    html += '<div class="chips">' +
      '<span class="chip">' + UI.esc(t.subtema + " · " + (Datos.subtemas[t.subtema] || "")) + "</span>" +
      '<span class="chip">' + UI.esc(TIPOS[t.tipo] || t.tipo) + "</span>" +
      (prev ? '<span class="chip">Última vez: ' + UI.esc(NOMBRES[prev.r] || prev.r) + "</span>" : "") +
      (t.verificar ? '<span class="chip chip--verificar">⚠ Verificar</span>' : "") +
      "</div>";

    html += '<button type="button" class="tarjeta' + (s.volteada ? " volteada" : "") + '" data-accion="voltear" ' +
      'aria-expanded="' + s.volteada + '" aria-controls="reverso-' + UI.esc(t.id) + '">' +
      '<span class="tarjeta__lado">Pregunta</span>' +
      '<span class="tarjeta__frente">' + UI.esc(t.frente) + "</span>" +
      (s.volteada ?
        '<span class="tarjeta__reverso" id="reverso-' + UI.esc(t.id) + '"><span class="tarjeta__lado">Respuesta</span>' +
        UI.esc(t.reverso) + "</span>" :
        '<span class="tarjeta__pista" id="reverso-' + UI.esc(t.id) + '">Tocá la tarjeta para ver la respuesta.</span>') +
      "</button>";

    if (s.volteada) {
      html += UI.figura(t.figura) + UI.verificar(t.verificar) + UI.fuentes(t) + UI.reportar(t.id, "Estudiar");
      html += '<div class="acciones" role="group" aria-label="¿La sabías?">' +
        '<button type="button" class="btn btn--mal" data-calificar="no">No la sabía</button>' +
        '<button type="button" class="btn btn--duda" data-calificar="dudosa">Dudosa</button>' +
        '<button type="button" class="btn btn--bien" data-calificar="sabia">La sabía</button>' +
        "</div>";
    } else {
      html += UI.reportar(t.id, "Estudiar");
      html += '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="voltear">Mostrar respuesta</button></div>';
    }
    vista.innerHTML = html;
    conectar(vista);
  }

  function conectar(vista) {
    var det = vista.querySelector(".filtros");
    if (det) {
      det.open = s.filtrosAbiertos;
      det.addEventListener("toggle", function () { s.filtrosAbiertos = det.open; });
    }
    UI.conectarFiltros(vista, s.f, false, function (nuevo) {
      s.f = nuevo;
      Store.pref("filtroEstudiar", nuevo);
      armarCola();
      render(vista);
      var sel = vista.querySelector("[data-filtro]");
      if (sel) sel.focus();
    });
    vista.querySelectorAll('[data-accion="voltear"]').forEach(function (b) {
      b.addEventListener("click", function () {
        s.volteada = !s.volteada;
        render(vista);
        var c = vista.querySelector(".tarjeta");
        if (c) c.focus();
      });
    });
    vista.querySelectorAll("[data-calificar]").forEach(function (b) {
      b.addEventListener("click", function () {
        var r = b.getAttribute("data-calificar");
        var id = s.cola[s.pos];
        Store.calificarTarjeta(id, r);
        if (REINSERTAR[r]) {
          var destino = Math.min(s.pos + 1 + REINSERTAR[r], s.cola.length);
          s.cola.splice(destino, 0, id);
        }
        s.pos++;
        s.volteada = false;
        render(vista);
        var c = vista.querySelector(".tarjeta") || vista.querySelector("[data-accion]");
        if (c) c.focus();
      });
    });
    var otra = vista.querySelector('[data-accion="otra"]');
    if (otra) otra.addEventListener("click", function () { armarCola(); render(vista); });
  }

  window.Estudiar = {
    titulo: "Estudiar",
    mostrar: function (vista) {
      if (!s.porId) {
        s.porId = {};
        Datos.tarjetas.forEach(function (t) { s.porId[t.id] = t; });
      }
      if (!s.f) { s.f = filtroInicial(); armarCola(); }
      render(vista);
    }
  };
})();
