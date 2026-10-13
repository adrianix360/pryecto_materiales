// Estudiar: tarjetas que se voltean al tocarlas y se califican con tres botones.
// Modo «Repaso de hoy» (por defecto): cola de SRS.colaRepaso (falladas, vencidas y nuevas
// del día). Modo «Por tema»: filtros por tema y subtema; también actualiza el repaso.
// En la sesión, una tarjeta marcada «no» vuelve 4 lugares después; una «dudosa», 8 después.
// Las colas salen barajadas (SRS.azar) y el botón «Barajar» mezcla otra vez lo que falta.
(function () {
  "use strict";

  var PRIORIDAD = { no: 1, dudosa: 2, sabia: 3 };
  var REINSERTAR = { no: 4, dudosa: 8 };
  var MAS_NUEVAS = 10;
  var NOMBRES = { sabia: "La sabía", dudosa: "Dudosa", no: "No la sabía" };
  var TIPOS = {
    concepto: "Concepto", dato: "Dato", clasificacion: "Clasificación", formula: "Fórmula",
    norma: "Norma", proceso: "Proceso", equipo: "Equipo", parametros: "Parámetros", criterio: "Criterio"
  };
  var NOMBRES_RESUMEN = { fallados: "falladas", vencidos: "vencidas", nuevos: "nuevas" };

  var s = {
    modo: null, f: null, cola: [], pos: 0, volteada: false, porId: null,
    filtrosAbiertos: false, metaAbierta: false, extra: null, dia: null, inicio: Date.now(),
    barajadas: 0
  };

  function leer(id) { return Store.tarjeta(id); }

  function filtroInicial() {
    var f = Store.pref("filtroEstudiar") || {};
    return { tema: f.tema || "", subtema: f.subtema || "" };
  }

  function nuevaCola(ids, extra) {
    s.cola = ids;
    s.pos = 0;
    s.volteada = false;
    s.extra = extra || null;
    s.dia = SRS.hoy();
    s.inicio = Date.now();
    s.barajadas = 0;
  }

  function armarRepaso() {
    nuevaCola(SRS.colaRepaso(Datos.tarjetas, leer, SRS.hoy(), Datos.indice.examen, SRS.azar()).ids.slice());
  }

  function armarTema() {
    var rnd = SRS.azar();
    var lista = Datos.tarjetas.filter(function (t) { return UI.cumpleFiltro(t, s.f); });
    if (rnd) lista = SRS.barajar(lista, rnd);
    lista = lista.map(function (t, i) { return { t: t, i: i, p: leer(t.id) }; });
    // Por nivel (sin ver, no, dudosa, sabía); dentro de cada nivel, al azar (o por fecha si el orden es fijo).
    lista.sort(function (a, b) {
      var pa = a.p ? PRIORIDAD[a.p.r] || 3 : 0;
      var pb = b.p ? PRIORIDAD[b.p.r] || 3 : 0;
      if (pa !== pb) return pa - pb;
      if (!rnd && a.p && b.p && a.p.t !== b.p.t) return a.p.t - b.p.t;
      return a.i - b.i;
    });
    nuevaCola(lista.map(function (x) { return x.t.id; }));
  }

  function armar() { if (s.modo === "repaso") armarRepaso(); else armarTema(); }

  function etiquetaExtra() {
    return s.extra === "nuevas" ? "Extra: tarjetas nuevas" :
      s.extra === "adelantar" ? "Extra: repaso adelantado" : s.extra;
  }

  function cabecera() {
    var html = UI.barraMeta() + UI.modo("est", s.modo);
    if (s.modo === "repaso") {
      var res = SRS.colaRepaso(Datos.tarjetas, leer, SRS.hoy(), Datos.indice.examen);
      var conVerif = s.cola.slice(s.pos).filter(function (id) { return s.porId[id].verificar; });
      html += UI.resumenRepaso(res, new Set(conVerif).size, NOMBRES_RESUMEN);
    } else {
      html += UI.filtros("est", s.f, false);
    }
    if (s.extra) html += '<p class="extra">' + UI.esc(etiquetaExtra()) + "</p>";
    return html;
  }

  function pantallaFin(vista) {
    var html = cabecera();
    var botones = "";
    if (s.extra && s.extra !== "nuevas" && s.extra !== "adelantar") {
      html += '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">Terminaste la lista</h2>' +
        "<p>Repasaste " + new Set(s.cola).size + " tarjetas de «" + UI.esc(s.extra) + "».</p></section>" +
        '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="volver">Volver al ' +
        (s.modo === "repaso" ? "repaso de hoy" : "modo por tema") + "</button></div>";
    } else if (s.modo === "repaso") {
      var nuevas = SRS.masNuevos(Datos.tarjetas, leer, MAS_NUEVAS, []);
      var adel = SRS.adelantar(Datos.tarjetas, leer, SRS.hoy());
      var titulo = s.extra ? "Terminaste el extra" :
        s.cola.length ? "Terminaste el repaso de hoy" : "No tenés tarjetas pendientes hoy";
      html += '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">' + titulo + "</h2>" +
        "<p>" + (s.cola.length ? "Repasaste " + new Set(s.cola).size + " tarjetas. " : "") +
        "Lo que vence mañana aparecerá en el repaso de mañana.</p></section>";
      if (nuevas.length) botones += '<button type="button" class="btn btn--primario" data-accion="nuevas">Seguir con ' + nuevas.length + " nuevas</button>";
      if (adel.length) botones += '<button type="button" class="btn" data-accion="adelantar">Adelantar repaso (' + adel.length + ")</button>";
      if (botones) html += '<div class="botones-fin">' + botones + "</div>";
    } else {
      html += '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">Ronda terminada</h2>' +
        "<p>Repasaste las " + new Set(s.cola).size + " tarjetas de este filtro.</p></section>" +
        '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="otra">Empezar otra ronda</button></div>';
    }
    vista.innerHTML = html;
    conectar(vista);
  }

  function render(vista) {
    UI.recordarPaneles(vista, s);
    if (s.modo === "tema" && !s.cola.length) {
      vista.innerHTML = cabecera() + '<p class="vacio">No hay tarjetas con ese filtro.</p>';
      conectar(vista);
      return;
    }
    if (s.pos >= s.cola.length) { pantallaFin(vista); return; }

    var t = s.porId[s.cola[s.pos]];
    var prev = leer(t.id);
    var html = cabecera();
    html += UI.contador("Tarjeta " + (s.pos + 1) + " de " + s.cola.length, s.cola.length - s.pos - 1, s.barajadas);
    s.barajadas = 0;
    html += '<div class="chips">' +
      '<span class="chip">' + UI.esc(t.subtema + " · " + (Datos.subtemas[t.subtema] || "")) + "</span>" +
      '<span class="chip">' + UI.esc(TIPOS[t.tipo] || t.tipo) + "</span>" +
      (prev ? '<span class="chip">Última vez: ' + UI.esc(NOMBRES[prev.r] || prev.r) + "</span>" : '<span class="chip">Nueva</span>') +
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

  function calificar(r) {
    var id = s.cola[s.pos];
    var t = s.porId[id];
    Store.guardarTarjeta(id, SRS.aplicar(leer(id), r, {
      id: id, hoy: SRS.hoy(), examen: Datos.indice.examen, verificar: !!t.verificar, ahora: Date.now()
    }));
    UI.registrarTiempo(s.inicio);
    if (REINSERTAR[r]) {
      var destino = Math.min(s.pos + 1 + REINSERTAR[r], s.cola.length);
      s.cola.splice(destino, 0, id);
    }
    s.pos++;
    s.volteada = false;
    s.inicio = Date.now();
  }

  function enfocar(vista) {
    var c = vista.querySelector(".tarjeta") || vista.querySelector(".botones-fin .btn, .acciones .btn");
    if (c) c.focus();
  }

  function conectar(vista) {
    vista.querySelectorAll("details.filtros, details.meta").forEach(function (det) {
      var esMeta = det.getAttribute("data-panel") === "meta";
      det.open = esMeta ? s.metaAbierta : s.filtrosAbiertos;
      det.addEventListener("toggle", function () {
        if (esMeta) s.metaAbierta = det.open; else s.filtrosAbiertos = det.open;
      });
    });
    UI.conectarModo(vista, function (m) {
      s.modo = m;
      Store.pref("modoEstudiar", m);
      armar();
      render(vista);
      var b = vista.querySelector('[data-modo="' + m + '"]');
      if (b) b.focus();
    });
    UI.conectarMeta(vista, function () {
      render(vista);
      var sel = vista.querySelector("[data-meta]");
      if (sel) sel.focus();
    });
    UI.conectarFiltros(vista, s.f, false, function (nuevo) {
      s.f = nuevo;
      Store.pref("filtroEstudiar", nuevo);
      armarTema();
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
    var bar = vista.querySelector('[data-accion="barajar"]');
    if (bar) bar.addEventListener("click", function () {
      s.barajadas = s.cola.length - s.pos - 1;
      s.cola = SRS.barajarResto(s.cola, s.pos, Math.random);
      render(vista);
      var b = vista.querySelector('[data-accion="barajar"]');
      if (b) b.focus();
    });
    vista.querySelectorAll("[data-calificar]").forEach(function (b) {
      b.addEventListener("click", function () {
        calificar(b.getAttribute("data-calificar"));
        render(vista);
        enfocar(vista);
      });
    });
    vista.querySelectorAll('[data-accion="otra"], [data-accion="nuevas"], [data-accion="adelantar"], [data-accion="volver"]').forEach(function (b) {
      b.addEventListener("click", function () {
        var acc = b.getAttribute("data-accion");
        if (acc === "otra") armarTema();
        else if (acc === "volver") armar();
        else if (acc === "nuevas") nuevaCola(SRS.masNuevos(Datos.tarjetas, leer, MAS_NUEVAS, [], SRS.azar()), "nuevas");
        else nuevaCola(SRS.adelantar(Datos.tarjetas, leer, SRS.hoy(), SRS.azar()), "adelantar");
        render(vista);
        enfocar(vista);
      });
    });
  }

  function asegurarIndice() {
    if (!s.porId) {
      s.porId = {};
      Datos.tarjetas.forEach(function (t) { s.porId[t.id] = t; });
    }
  }

  window.Estudiar = {
    titulo: "Estudiar",
    // Abre una cola con estas tarjetas (desde Buscar). etiqueta: texto que se muestra arriba.
    abrirLista: function (ids, etiqueta) {
      asegurarIndice();
      if (!s.modo) {
        s.modo = Store.pref("modoEstudiar") === "tema" ? "tema" : "repaso";
        s.f = filtroInicial();
      }
      nuevaCola(ids.filter(function (id) { return s.porId[id]; }), etiqueta);
    },
    mostrar: function (vista) {
      asegurarIndice();
      if (!s.modo) {
        s.modo = Store.pref("modoEstudiar") === "tema" ? "tema" : "repaso";
        s.f = filtroInicial();
        armar();
      } else if (s.modo === "repaso" && !s.extra && s.dia !== SRS.hoy()) {
        armarRepaso(); // cambió el día con la app abierta
      }
      render(vista);
    }
  };
})();
