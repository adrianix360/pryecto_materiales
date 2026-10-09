// Practicar: selección única, selección múltiple y F/V con retroalimentación inmediata;
// respuesta corta con autocalificación.
// Modo «Repaso de hoy» (por defecto): cola de SRS.colaRepaso (falladas, vencidas y nuevas
// del día). Modo «Por tema»: filtros; orden sin responder, luego mal, parcial y bien.
// En la sesión, una pregunta respondida mal vuelve 4 lugares después.
// Las opciones no se barajan: las explicaciones citan las letras («Correcta la B»).
(function () {
  "use strict";

  var PRIORIDAD = { mal: 1, parcial: 2, bien: 3 };
  var TIPOS = {
    seleccion_unica: "Selección única",
    seleccion_multiple: "Selección múltiple",
    verdadero_falso: "Falso o verdadero",
    respuesta_corta: "Respuesta corta"
  };
  var RESULTADO = { bien: "Bien", parcial: "Parcial", mal: "Mal" };
  var REINSERTAR_MAL = 4;
  var MAS_NUEVAS = 10;
  var NOMBRES_RESUMEN = { fallados: "falladas", vencidos: "vencidas", nuevos: "nuevas" };

  var s = {
    modo: null, f: null, cola: [], pos: 0, porId: null, filtrosAbiertos: false, metaAbierta: false,
    marcadas: [], texto: "", fase: "pregunta", resultado: null, extra: null, dia: null, inicio: Date.now()
  };

  function leer(id) { return Store.pregunta(id); }

  function filtroInicial() {
    var f = Store.pref("filtroPracticar") || {};
    return { tema: f.tema || "", subtema: f.subtema || "", origen: f.origen || "" };
  }

  function reiniciarPregunta() {
    s.marcadas = [];
    s.texto = "";
    s.fase = "pregunta";
    s.resultado = null;
    s.inicio = Date.now();
  }

  function nuevaCola(ids, extra) {
    s.cola = ids;
    s.pos = 0;
    s.extra = extra || null;
    s.dia = SRS.hoy();
    reiniciarPregunta();
  }

  function armarRepaso() {
    nuevaCola(SRS.colaRepaso(Datos.preguntas, leer, SRS.hoy(), Datos.indice.examen).ids.slice());
  }

  function armar() { if (s.modo === "repaso") armarRepaso(); else armarCola(); }

  function cabecera() {
    var html = UI.barraMeta() + UI.modo("pra", s.modo);
    if (s.modo === "repaso") {
      var res = SRS.colaRepaso(Datos.preguntas, leer, SRS.hoy(), Datos.indice.examen);
      var conVerif = s.cola.slice(s.pos).filter(function (id) { return s.porId[id].verificar; });
      html += UI.resumenRepaso(res, new Set(conVerif).size, NOMBRES_RESUMEN);
    } else {
      html += UI.filtros("pra", s.f, true);
    }
    if (s.extra) {
      html += '<p class="extra">' + UI.esc(s.extra === "nuevas" ? "Extra: preguntas nuevas" :
        s.extra === "adelantar" ? "Extra: repaso adelantado" : s.extra) + "</p>";
    }
    return html;
  }

  function armarCola() {
    var lista = Datos.preguntas.filter(function (p) { return UI.cumpleFiltro(p, s.f); });
    lista = lista.map(function (p, i) { return { p: p, i: i, r: leer(p.id) }; });
    lista.sort(function (a, b) {
      var pa = a.r ? PRIORIDAD[a.r.r] || 3 : 0;
      var pb = b.r ? PRIORIDAD[b.r.r] || 3 : 0;
      if (pa !== pb) return pa - pb;
      if (a.r && b.r && a.r.t !== b.r.t) return a.r.t - b.r.t;
      return a.i - b.i;
    });
    nuevaCola(lista.map(function (x) { return x.p.id; }));
  }

  function correctas(p) {
    return Array.isArray(p.correcta) ? p.correcta : [p.correcta];
  }

  function evaluar(p) {
    var ok = correctas(p);
    if (p.tipo !== "seleccion_multiple") return s.marcadas[0] === ok[0] ? "bien" : "mal";
    var malas = s.marcadas.filter(function (m) { return ok.indexOf(m) < 0; }).length;
    var buenas = s.marcadas.filter(function (m) { return ok.indexOf(m) >= 0; }).length;
    if (!malas && buenas === ok.length) return "bien";
    if (!malas && buenas > 0) return "parcial";
    return "mal";
  }

  function letras(ids) {
    return ids.map(function (x) { return x.toUpperCase(); }).join(", ").replace(/, ([^,]*)$/, " y $1");
  }

  function htmlOpciones(p) {
    var ok = correctas(p);
    var multiple = p.tipo === "seleccion_multiple";
    var resuelta = s.fase === "respondida";
    return '<ul class="opciones" role="list">' + p.opciones.map(function (o) {
      var marcada = s.marcadas.indexOf(o.id) >= 0;
      var esOk = ok.indexOf(o.id) >= 0;
      var clase = "opcion";
      var estado = "";
      if (resuelta) {
        if (esOk) { clase += " es-correcta"; estado = marcada ? "✓ Tu respuesta" : (multiple ? "✓ Faltó" : "✓ Correcta"); }
        else if (marcada) { clase += " es-incorrecta"; estado = "✗ Tu respuesta"; }
      }
      var attrs = multiple ?
        ' role="checkbox" aria-checked="' + marcada + '"' : "";
      return '<li><button type="button" class="' + clase + '" data-opcion="' + UI.esc(o.id) + '"' + attrs +
        (resuelta ? " disabled" : "") + ">" +
        '<span class="opcion__letra" aria-hidden="true">' + UI.esc(o.id.toUpperCase()) + "</span>" +
        '<span class="opcion__texto"><span class="solo-lector">Opción ' + UI.esc(o.id.toUpperCase()) + ": </span>" +
        UI.esc(o.texto) + "</span>" +
        (estado ? '<span class="opcion__estado">' + UI.esc(estado) + "</span>" : "") +
        "</button></li>";
    }).join("") + "</ul>";
  }

  function htmlDetalles(p) {
    var html = "";
    if (p.explicacion) html += '<div class="bloque"><p class="bloque__titulo">Explicación</p><p>' + UI.esc(p.explicacion) + "</p></div>";
    if (p.justificacion_oficial) html += '<div class="bloque"><p class="bloque__titulo">Justificación de la clave</p><p>' + UI.esc(p.justificacion_oficial) + "</p></div>";
    html += UI.verificar(p.verificar);
    html += UI.fuentes(p);
    return html;
  }

  function htmlRetro(p) {
    if (p.tipo === "respuesta_corta") {
      if (s.fase === "pregunta") return "";
      var html = '<div class="retro' + (s.resultado ? " retro--" + (s.resultado === "bien" ? "bien" : s.resultado === "mal" ? "mal" : "duda") : "") +
        '" id="retro" tabindex="-1" aria-live="polite">';
      html += '<h3 class="retro__titulo">' + (s.resultado ? "Te calificaste: " + RESULTADO[s.resultado] : "Comparala con tu respuesta") + "</h3>";
      if (s.texto.trim()) html += '<div class="bloque"><p class="bloque__titulo">Tu respuesta</p><p>' + UI.esc(s.texto) + "</p></div>";
      html += '<div class="bloque"><p class="bloque__titulo">Respuesta modelo</p><p>' + UI.esc(p.respuesta_modelo) + "</p></div>";
      html += '<div class="bloque"><p class="bloque__titulo">Puntos clave</p><ul class="puntos">' +
        (p.puntos_clave || []).map(function (k) { return "<li>" + UI.esc(k) + "</li>"; }).join("") + "</ul></div>";
      if (p.clave === "pendiente") html += '<div class="bloque"><p>Esta pregunta no tiene clave oficial.</p></div>';
      return html + htmlDetalles(p) + "</div>";
    }
    if (s.fase !== "respondida") return "";
    var r = s.resultado;
    var titulo = r === "bien" ? "✓ ¡Correcto!" :
      r === "parcial" ? "◐ Incompleto. Las correctas son " + letras(correctas(p)) + "." :
      "✗ Incorrecto. " + (correctas(p).length > 1 ? "Las correctas son " : "La correcta es la ") + letras(correctas(p)) + ".";
    return '<div class="retro retro--' + (r === "bien" ? "bien" : r === "mal" ? "mal" : "duda") +
      '" id="retro" tabindex="-1" aria-live="polite"><h3 class="retro__titulo">' + UI.esc(titulo) + "</h3>" +
      htmlDetalles(p) + "</div>";
  }

  function htmlAcciones(p) {
    var a = '<div class="acciones"';
    if (s.fase === "respondida") {
      return a + '><button type="button" class="btn btn--primario" data-accion="siguiente">Siguiente →</button></div>';
    }
    if (p.tipo === "respuesta_corta" && s.fase === "vista") {
      return a + ' role="group" aria-label="Autocalificación">' +
        '<button type="button" class="btn btn--mal" data-autocalificar="mal">Mal</button>' +
        '<button type="button" class="btn btn--duda" data-autocalificar="parcial">Parcial</button>' +
        '<button type="button" class="btn btn--bien" data-autocalificar="bien">Bien</button></div>';
    }
    var saltar = '<button type="button" class="btn" data-accion="saltar">Saltar</button>';
    if (p.tipo === "respuesta_corta") {
      return a + ">" + saltar + '<button type="button" class="btn btn--primario" data-accion="ver">Ver respuesta</button></div>';
    }
    if (p.tipo === "seleccion_multiple") {
      return a + ">" + saltar + '<button type="button" class="btn btn--primario" data-accion="revisar"' +
        (s.marcadas.length ? "" : " disabled") + ">Revisar</button></div>";
    }
    return a + ">" + saltar + "</div>";
  }

  function pantallaFin(vista) {
    var html = cabecera();
    if (s.extra && s.extra !== "nuevas" && s.extra !== "adelantar") {
      html += '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">Terminaste la lista</h2>' +
        "<p>Pasaste por " + new Set(s.cola).size + " preguntas de «" + UI.esc(s.extra) + "».</p></section>" +
        '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="volver">Volver al ' +
        (s.modo === "repaso" ? "repaso de hoy" : "modo por tema") + "</button></div>";
    } else if (s.modo === "repaso") {
      var nuevas = SRS.masNuevos(Datos.preguntas, leer, MAS_NUEVAS, []);
      var adel = SRS.adelantar(Datos.preguntas, leer, SRS.hoy());
      var titulo = s.extra ? "Terminaste el extra" :
        s.cola.length ? "Terminaste el repaso de hoy" : "No tenés preguntas pendientes hoy";
      var botones = "";
      html += '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">' + titulo + "</h2>" +
        "<p>" + (s.cola.length ? "Pasaste por " + new Set(s.cola).size + " preguntas. " : "") +
        "Lo que vence mañana aparecerá en el repaso de mañana.</p></section>";
      if (nuevas.length) botones += '<button type="button" class="btn btn--primario" data-accion="nuevas">Seguir con ' + nuevas.length + " nuevas</button>";
      if (adel.length) botones += '<button type="button" class="btn" data-accion="adelantar">Adelantar repaso (' + adel.length + ")</button>";
      if (botones) html += '<div class="botones-fin">' + botones + "</div>";
    } else {
      html += '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">Ronda terminada</h2>' +
        "<p>Pasaste por las " + new Set(s.cola).size + " preguntas de este filtro.</p></section>" +
        '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="otra">Empezar otra ronda</button></div>';
    }
    vista.innerHTML = html;
    conectar(vista);
  }

  function render(vista) {
    UI.recordarPaneles(vista, s);
    var html = cabecera();
    if (s.modo === "tema" && !s.cola.length) {
      vista.innerHTML = html + '<p class="vacio">No hay preguntas con ese filtro.</p>';
      conectar(vista);
      return;
    }
    if (s.pos >= s.cola.length) { pantallaFin(vista); return; }

    var p = s.porId[s.cola[s.pos]];
    var prev = leer(p.id);
    html += '<p class="contador">Pregunta ' + (s.pos + 1) + " de " + s.cola.length + "</p>";
    html += '<div class="chips">' +
      '<span class="chip">' + UI.esc(TIPOS[p.tipo]) + "</span>" +
      (p.origen === "examen" ?
        '<span class="chip chip--examen">' + UI.esc(Datos.etiquetaExamen(p.examen)) + "</span>" :
        '<span class="chip">Teoría</span>') +
      '<span class="chip">' + UI.esc(p.subtema) + "</span>" +
      (prev ? '<span class="chip">Última vez: ' + UI.esc(RESULTADO[prev.r] || prev.r) + "</span>" : '<span class="chip">Nueva</span>') +
      (p.verificar ? '<span class="chip chip--verificar">⚠ Verificar</span>' : "") +
      "</div>";

    html += '<section class="pregunta" data-id="' + UI.esc(p.id) + '" data-tipo="' + p.tipo + '" aria-labelledby="enunciado">';
    html += '<h2 class="pregunta__enunciado" id="enunciado">' + UI.esc(p.enunciado) + "</h2>";
    html += UI.figura(p.figura);
    if (p.tipo === "respuesta_corta") {
      html += '<label class="bloque__titulo" for="respuesta">Tu respuesta</label>' +
        '<textarea id="respuesta" class="respuesta-texto" rows="4"' + (s.fase !== "pregunta" ? " readonly" : "") +
        ' placeholder="Escribila antes de ver la respuesta modelo">' + UI.esc(s.texto) + "</textarea>";
    } else {
      if (p.tipo === "seleccion_multiple" && s.fase === "pregunta") {
        html += '<p class="contador">Marcá todas las correctas y tocá «Revisar».</p>';
      }
      html += htmlOpciones(p);
    }
    html += htmlRetro(p);
    html += UI.reportar(p.id, "Practicar");
    html += "</section>";
    html += htmlAcciones(p);
    vista.innerHTML = html;
    conectar(vista);
  }

  function cerrar(vista, p, resultado, resp) {
    s.resultado = resultado;
    s.fase = "respondida";
    var prev = leer(p.id);
    var reg = SRS.aplicar(prev, resultado, {
      id: p.id, hoy: SRS.hoy(), examen: Datos.indice.examen, verificar: !!p.verificar, ahora: Date.now()
    });
    reg.bien = (prev && prev.bien || 0) + (resultado === "bien" ? 1 : 0);
    reg.resp = resp;
    Store.guardarPregunta(p.id, reg);
    UI.registrarTiempo(s.inicio);
    if (resultado === "mal") {
      s.cola.splice(Math.min(s.pos + 1 + REINSERTAR_MAL, s.cola.length), 0, p.id);
    }
    render(vista);
    var r = vista.querySelector("#retro");
    if (r) r.focus();
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
      Store.pref("modoPracticar", m);
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
    UI.conectarFiltros(vista, s.f, true, function (nuevo) {
      s.f = nuevo;
      Store.pref("filtroPracticar", nuevo);
      armarCola();
      render(vista);
      var sel = vista.querySelector("[data-filtro]");
      if (sel) sel.focus();
    });

    var p = s.porId[s.cola[s.pos]];

    vista.querySelectorAll("[data-opcion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-opcion");
        if (p.tipo === "seleccion_multiple") {
          var i = s.marcadas.indexOf(id);
          if (i >= 0) s.marcadas.splice(i, 1); else s.marcadas.push(id);
          render(vista);
          var mismo = vista.querySelector('[data-opcion="' + id + '"]');
          if (mismo) mismo.focus();
          return;
        }
        s.marcadas = [id];
        cerrar(vista, p, evaluar(p), id);
      });
    });

    var ta = vista.querySelector("#respuesta");
    if (ta) ta.addEventListener("input", function () { s.texto = ta.value; });

    vista.querySelectorAll("[data-accion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var acc = b.getAttribute("data-accion");
        if (acc === "revisar") {
          cerrar(vista, p, evaluar(p), s.marcadas.slice());
        } else if (acc === "ver") {
          s.fase = "vista";
          render(vista);
          var r = vista.querySelector("#retro");
          if (r) r.focus();
        } else if (acc === "siguiente" || acc === "saltar") {
          s.pos++;
          reiniciarPregunta();
          render(vista);
          var c = vista.querySelector("#enunciado");
          if (c) { c.setAttribute("tabindex", "-1"); c.focus(); }
          window.scrollTo(0, 0);
        } else if (acc === "otra") {
          armarCola();
          render(vista);
        } else if (acc === "volver") {
          armar();
          render(vista);
        } else if (acc === "nuevas") {
          nuevaCola(SRS.masNuevos(Datos.preguntas, leer, MAS_NUEVAS, []), "nuevas");
          render(vista);
        } else if (acc === "adelantar") {
          nuevaCola(SRS.adelantar(Datos.preguntas, leer, SRS.hoy()), "adelantar");
          render(vista);
        }
      });
    });

    vista.querySelectorAll("[data-autocalificar]").forEach(function (b) {
      b.addEventListener("click", function () {
        cerrar(vista, p, b.getAttribute("data-autocalificar"), s.texto.slice(0, 2000));
      });
    });
  }

  function asegurarIndice() {
    if (!s.porId) {
      s.porId = {};
      Datos.preguntas.forEach(function (p) { s.porId[p.id] = p; });
    }
  }

  window.Practicar = {
    titulo: "Practicar",
    // Abre una cola con estas preguntas (desde Buscar). etiqueta: texto que se muestra arriba.
    abrirLista: function (ids, etiqueta) {
      asegurarIndice();
      if (!s.modo) {
        s.modo = Store.pref("modoPracticar") === "tema" ? "tema" : "repaso";
        s.f = filtroInicial();
      }
      nuevaCola(ids.filter(function (id) { return s.porId[id]; }), etiqueta);
      s.rearmar = false;
    },
    // El Simulacro mandó fallos al repaso: rearmar la cola la próxima vez que se muestre.
    recargar: function () { s.rearmar = true; },
    // Progreso abrió un subtema: volver a leer modo y filtros de las preferencias.
    reiniciar: function () { s.modo = null; },
    mostrar: function (vista) {
      asegurarIndice();
      if (!s.modo) {
        s.modo = Store.pref("modoPracticar") === "tema" ? "tema" : "repaso";
        s.f = filtroInicial();
        armar();
      } else if (s.modo === "repaso" && !s.extra && (s.dia !== SRS.hoy() || s.rearmar) && s.fase === "pregunta") {
        armarRepaso(); // cambió el día con la app abierta o llegaron fallos del simulacro
      }
      s.rearmar = false;
      render(vista);
    }
  };
})();
