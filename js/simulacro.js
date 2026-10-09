// Simulacro: examen cronometrado como el I examen del curso (ver js/examen.js).
// Fases: configurar → examen (sin retroalimentación) → autoevaluación → resultado.
// El examen en curso vive en Store.simulacro(): el tiempo restante se calcula con la hora
// de fin guardada, así que sobrevive al bloqueo de pantalla y a una recarga.
(function () {
  "use strict";

  var DURACIONES = [25, 40, 60];
  var NOMBRE_TIPO = {
    seleccion_unica: "Selección única",
    verdadero_falso: "Falso o verdadero",
    respuesta_corta: "Respuesta corta"
  };
  var PARTE = { seleccion_unica: 1, verdadero_falso: 2, respuesta_corta: 3 };

  var s = { porId: null, vista: null, reloj: null, confirmar: false, avisos: {}, tiempoAcabado: false };

  function ahora() { return Date.now(); }
  function est() { return Store.simulacro(); }
  function guardar(e) { Store.simulacro(e); }
  function num(n) { return String(n).replace(".", ","); }
  function pts(n) { return num(n) + (n === 1 ? " punto" : " puntos"); }

  function config() {
    var c = Store.pref("simulacroConfig") || {};
    var temas = (c.temas || []).filter(function (t) { return [1, 2, 3].indexOf(t) >= 0; });
    return {
      duracion: DURACIONES.indexOf(c.duracion) >= 0 ? c.duracion : 25,
      temas: c.temas ? temas : [1, 2, 3]
    };
  }

  function respondida(id, e) {
    var r = e.resp[id] || {};
    var p = s.porId[id];
    return p.tipo === "respuesta_corta" ? !!String(r.texto || "").trim() : !!r.op;
  }

  // «C. texto», con la letra que se vio en el examen.
  function textoOpcion(p, op, orden) {
    if (!op) return "Sin responder";
    for (var i = 0; i < p.opciones.length; i++) {
      if (p.opciones[i].id === op) return Opciones.letra(orden, op) + ". " + p.opciones[i].texto;
    }
    return op;
  }

  // ---------- Reloj ----------
  function detenerReloj() {
    if (s.reloj) { clearInterval(s.reloj); s.reloj = null; }
  }

  function tick() {
    var el = document.getElementById("reloj-tiempo");
    var e = est();
    if (!el || !e || e.fase !== "examen" || document.body.getAttribute("data-pantalla") !== "simulacro") {
      detenerReloj();
      return;
    }
    var resta = Examen.restante(e, ahora());
    el.textContent = Examen.formatoTiempo(resta);
    var caja = document.getElementById("reloj");
    if (caja) caja.classList.toggle("reloj--poco", resta <= 5 * 60000);
    var aviso = document.getElementById("aviso-tiempo");
    [[5, "Quedan 5 minutos."], [1, "Queda 1 minuto."]].forEach(function (x) {
      if (resta <= x[0] * 60000 && resta > 0 && !s.avisos[x[0]]) {
        s.avisos[x[0]] = true;
        if (aviso) aviso.textContent = x[1];
      }
    });
    if (resta <= 0) {
      s.tiempoAcabado = true;
      guardar(Examen.terminar(e, s.porId, ahora()));
      render();
    }
  }

  function iniciarReloj() {
    detenerReloj();
    s.reloj = setInterval(tick, 1000);
    tick();
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") tick();
  });

  // ---------- Configurar ----------
  function renderConfig() {
    var c = config();
    var armado = c.temas.length ? Examen.armar(Datos.preguntas, c, 1) : { ids: [], faltan: {} };
    var est_ = Examen.ESTRUCTURA[c.duracion];
    var total = 0;
    var filas = Examen.SECCIONES.map(function (t) {
      var n = est_[t] - (armado.faltan[t] || 0);
      total += n * Examen.PUNTOS[t];
      return "<li>" + n + " de " + NOMBRE_TIPO[t].toLowerCase() + " × " + pts(Examen.PUNTOS[t]) +
        (armado.faltan[t] ? ' <span class="falta">(faltan ' + armado.faltan[t] + " con estos temas)</span>" : "") + "</li>";
    }).join("");
    var hist = Store.historial().slice(0, 5);
    var html = '<section class="pagina" aria-labelledby="h-sim">' +
      '<h2 id="h-sim">Simulacro de examen</h2>' +
      '<p class="nota">Como el I examen: selección única, falso o verdadero con justificación de los falsos ' +
      "y respuesta corta. No vas a saber si acertaste hasta terminar.</p>" +
      '<fieldset class="grupo"><legend>Duración</legend><div class="modo modo--3">' +
      DURACIONES.map(function (d) {
        return '<button type="button" class="modo__opcion" data-duracion="' + d + '" aria-pressed="' + (d === c.duracion) + '">' + d + " min</button>";
      }).join("") + "</div></fieldset>" +
      '<fieldset class="grupo"><legend>Temas</legend>' +
      Datos.temas.map(function (t) {
        return '<label class="casilla"><input type="checkbox" data-tema="' + t.tema + '"' +
          (c.temas.indexOf(t.tema) >= 0 ? " checked" : "") + "> " + UI.esc(t.tema + ". " + t.titulo) + "</label>";
      }).join("") + "</fieldset>" +
      '<div class="tarjeta-info"><p class="bloque__titulo">Estructura</p><ul class="puntos">' + filas + "</ul>" +
      "<p><strong>Total: " + pts(total) + "</strong></p></div>";
    if (!Store.disponible()) {
      html += '<p class="nota">Este navegador no guarda datos: si recargás la página durante el examen, se pierde.</p>';
    }
    if (hist.length) {
      html += '<div class="tarjeta-info"><p class="bloque__titulo">Tus últimos simulacros</p><ul class="puntos">' +
        hist.map(function (h) {
          return "<li>" + UI.esc(UI.fechaLarga(h.fecha)) + ": <strong>" + num(h.nota) + "</strong> (" +
            num(h.puntos) + " de " + h.maximo + ", " + h.duracion + " min, " + Examen.formatoTiempo(h.usado) + " usados)</li>";
        }).join("") + "</ul></div>";
    }
    html += "</section>" +
      '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="empezar"' +
      (c.temas.length ? "" : " disabled") + ">" + (c.temas.length ? "Empezar simulacro" : "Elegí al menos un tema") + "</button></div>";
    s.vista.innerHTML = html;

    s.vista.querySelectorAll("[data-duracion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var c2 = config();
        c2.duracion = +b.getAttribute("data-duracion");
        Store.pref("simulacroConfig", c2);
        render();
        s.vista.querySelector('[data-duracion="' + c2.duracion + '"]').focus();
      });
    });
    s.vista.querySelectorAll("[data-tema]").forEach(function (chk) {
      chk.addEventListener("change", function () {
        var c2 = config();
        var t = +chk.getAttribute("data-tema");
        c2.temas = c2.temas.filter(function (x) { return x !== t; });
        if (chk.checked) c2.temas.push(t);
        c2.temas.sort();
        Store.pref("simulacroConfig", c2);
        render();
        s.vista.querySelector('[data-tema="' + t + '"]').focus();
      });
    });
    var emp = s.vista.querySelector('[data-accion="empezar"]');
    emp.addEventListener("click", function () {
      var c2 = config();
      var semilla = (ahora() ^ Math.floor(Math.random() * 1e9)) >>> 0;
      guardar(Examen.nuevo(Datos.preguntas, c2, ahora(), semilla));
      s.avisos = {};
      s.confirmar = false;
      s.tiempoAcabado = false;
      render();
      enfocarEnunciado();
    });
  }

  // ---------- Examen ----------
  function enfocarEnunciado() {
    var h = s.vista.querySelector("#enunciado");
    if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
    window.scrollTo(0, 0);
  }

  function renderExamen(e) {
    var id = e.ids[e.pos];
    var p = s.porId[id];
    var r = e.resp[id] || {};
    var n = e.ids.length;
    var hechas = e.ids.filter(function (x) { return respondida(x, e); }).length;
    var html = '<div class="reloj" id="reloj"><span>⏱ <span id="reloj-tiempo" role="timer" aria-label="Tiempo restante">' +
      Examen.formatoTiempo(Examen.restante(e, ahora())) + "</span></span>" +
      "<span>Pregunta " + (e.pos + 1) + " de " + n + "</span></div>" +
      '<p id="aviso-tiempo" class="solo-lector" aria-live="assertive"></p>';
    html += '<p class="seccion">Parte ' + PARTE[p.tipo] + " · " + NOMBRE_TIPO[p.tipo] + " · " + pts(Examen.PUNTOS[p.tipo]) +
      (p.tipo === "verdadero_falso" ? " (justificá los falsos)" : "") + "</p>";
    html += '<section class="pregunta" data-id="' + UI.esc(id) + '" data-tipo="' + p.tipo + '" aria-labelledby="enunciado">' +
      '<h2 class="pregunta__enunciado" id="enunciado">' + (e.pos + 1) + ". " + UI.esc(p.enunciado) + "</h2>" +
      UI.figura(p.figura);
    if (p.tipo === "respuesta_corta") {
      html += '<label class="bloque__titulo" for="resp-texto">Tu respuesta</label>' +
        '<textarea id="resp-texto" class="respuesta-texto" rows="4">' + UI.esc(r.texto || "") + "</textarea>";
    } else {
      var orden = Examen.ordenDe(e, p);
      html += '<ul class="opciones" role="list">' + orden.map(function (oid, i) {
        var o = p.opciones.filter(function (x) { return x.id === oid; })[0];
        var letra = Opciones.LETRAS[i];
        return '<li><button type="button" class="opcion" data-opcion="' + UI.esc(o.id) + '" aria-pressed="' + (r.op === o.id) + '">' +
          '<span class="opcion__letra" aria-hidden="true">' + letra + "</span>" +
          '<span class="opcion__texto"><span class="solo-lector">Opción ' + letra + ": </span>" +
          UI.esc(o.texto) + "</span></button></li>";
      }).join("") + "</ul>";
      if (p.tipo === "verdadero_falso" && r.op && /^falso$/i.test(textoOpcion(p, r.op, orden).slice(3))) {
        html += '<label class="bloque__titulo bloque" for="resp-justif">Justificá por qué es falso</label>' +
          '<textarea id="resp-justif" class="respuesta-texto" rows="3">' + UI.esc(r.justif || "") + "</textarea>";
      }
    }
    html += UI.reportar(id, "Simulacro") + "</section>";

    html += '<details class="filtros mapa" data-panel="mapa"><summary>Ir a otra pregunta <span class="filtros__resumen">' +
      hechas + " de " + n + " respondidas</span></summary>" +
      '<div class="filtros__cuerpo"><div class="mapa__grilla">' +
      e.ids.map(function (x, i) {
        return '<button type="button" class="mapa__btn' + (respondida(x, e) ? " respondida" : "") + '" data-ir="' + i + '"' +
          (i === e.pos ? ' aria-current="step"' : "") + ' aria-label="Pregunta ' + (i + 1) +
          (respondida(x, e) ? ", respondida" : ", sin responder") + '">' + (i + 1) + "</button>";
      }).join("") + "</div>" +
      '<button type="button" class="btn btn--ancho" data-accion="terminar">Terminar examen</button></div></details>';

    if (s.confirmar) {
      var faltan = n - hechas;
      html += '<div class="verificar confirmar" role="alertdialog" aria-labelledby="h-conf" aria-describedby="p-conf">' +
        '<p class="verificar__titulo" id="h-conf">¿Terminar el examen?</p>' +
        '<p id="p-conf">' + (faltan ? "Te quedan " + faltan + " sin responder." : "Respondiste todas.") +
        " Después ya no podés cambiar respuestas.</p></div>";
    }

    html += s.confirmar ?
      '<div class="acciones" role="group" aria-label="Confirmar">' +
      '<button type="button" class="btn" data-accion="cancelar">Seguir respondiendo</button>' +
      '<button type="button" class="btn btn--primario" data-accion="confirmar">Sí, terminar</button></div>' :
      '<div class="acciones">' +
      '<button type="button" class="btn" data-accion="anterior"' + (e.pos === 0 ? " disabled" : "") + ">← Anterior</button>" +
      (e.pos < n - 1 ?
        '<button type="button" class="btn btn--primario" data-accion="siguiente">Siguiente →</button>' :
        '<button type="button" class="btn btn--primario" data-accion="terminar">Terminar</button>') +
      "</div>";
    s.vista.innerHTML = html;
    var mapa = s.vista.querySelector(".mapa");
    mapa.open = !!s.mapaAbierto;
    mapa.addEventListener("toggle", function () { s.mapaAbierto = mapa.open; });

    s.vista.querySelectorAll("[data-opcion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var e2 = est();
        var prev = e2.resp[id] || {};
        e2.resp[id] = { op: b.getAttribute("data-opcion"), justif: prev.justif || "" };
        guardar(e2);
        render();
        var mismo = s.vista.querySelector('[data-opcion="' + b.getAttribute("data-opcion") + '"]');
        if (mismo) mismo.focus();
      });
    });
    var ta = s.vista.querySelector("#resp-texto");
    if (ta) ta.addEventListener("input", function () {
      var e2 = est();
      e2.resp[id] = { texto: ta.value.slice(0, 3000) };
      guardar(e2);
    });
    var tj = s.vista.querySelector("#resp-justif");
    if (tj) tj.addEventListener("input", function () {
      var e2 = est();
      e2.resp[id] = { op: (e2.resp[id] || {}).op, justif: tj.value.slice(0, 3000) };
      guardar(e2);
    });
    s.vista.querySelectorAll("[data-ir]").forEach(function (b) {
      b.addEventListener("click", function () { ir(+b.getAttribute("data-ir")); });
    });
    s.vista.querySelectorAll("[data-accion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var acc = b.getAttribute("data-accion");
        if (acc === "anterior") ir(est().pos - 1);
        else if (acc === "siguiente") ir(est().pos + 1);
        else if (acc === "terminar") {
          s.confirmar = true;
          render();
          var panel = s.vista.querySelector(".confirmar");
          if (panel) panel.scrollIntoView({ block: "center" });
          var c = s.vista.querySelector('[data-accion="confirmar"]');
          if (c) c.focus({ preventScroll: true });
        } else if (acc === "cancelar") {
          s.confirmar = false;
          render();
        } else if (acc === "confirmar") {
          s.confirmar = false;
          s.tiempoAcabado = false;
          guardar(Examen.terminar(est(), s.porId, ahora()));
          render();
          window.scrollTo(0, 0);
        }
      });
    });
    iniciarReloj();
  }

  function ir(i) {
    var e = est();
    e.pos = Math.max(0, Math.min(e.ids.length - 1, i));
    guardar(e);
    s.confirmar = false;
    render();
    enfocarEnunciado();
  }

  // ---------- Autoevaluación ----------
  function puntosClaveHTML(p, id, marcados, editable) {
    return '<fieldset class="grupo"><legend>Puntos clave que cubriste</legend>' +
      (p.puntos_clave || []).map(function (k, i) {
        var on = marcados.indexOf(i) >= 0;
        return editable ?
          '<label class="casilla"><input type="checkbox" data-punto="' + i + '" data-id="' + UI.esc(id) + '"' + (on ? " checked" : "") + "> " + UI.esc(k) + "</label>" :
          '<p class="casilla casilla--fija">' + (on ? "✓ " : "✗ ") + UI.esc(k) + "</p>";
      }).join("") + "</fieldset>";
  }

  function renderAutoeval(e) {
    var pend = e.ids.filter(function (id) { return Examen.necesitaAutoeval(s.porId[id], e.resp[id]); });
    var sinJuzgar = pend.filter(function (id) {
      return s.porId[id].tipo === "verdadero_falso" && typeof (e.auto[id] || {}).justifOk !== "boolean";
    }).length;
    var html = '<section class="pagina" aria-labelledby="h-auto"><h2 id="h-auto">Autoevaluación</h2>';
    if (e.porTiempo) html += '<div class="verificar" role="note"><p class="verificar__titulo">⏱ Se acabó el tiempo</p><p>El examen se cerró solo. Se califica lo que alcanzaste a responder.</p></div>';
    html += '<p class="nota">Compará cada respuesta con la clave y sé honesto. La selección única y los verdaderos se califican solos.</p>';
    pend.forEach(function (id) {
      var p = s.porId[id];
      var r = e.resp[id] || {};
      var a = e.auto[id] || {};
      var i = e.ids.indexOf(id);
      html += '<article class="pregunta autoeval" data-id="' + UI.esc(id) + '">' +
        '<p class="seccion">Pregunta ' + (i + 1) + " · " + (p.tipo === "verdadero_falso" ? "justificación del falso (1 punto)" : "respuesta corta (2 puntos)") + "</p>" +
        '<h3 class="pregunta__enunciado">' + UI.esc(p.enunciado) + "</h3>";
      if (p.tipo === "verdadero_falso") {
        html += '<div class="bloque"><p class="bloque__titulo">Tu justificación</p><p>' + UI.esc(r.justif) + "</p></div>" +
          '<div class="bloque"><p class="bloque__titulo">' + (p.justificacion_oficial ? "Justificación de la clave" : "Explicación") + "</p><p>" +
          UI.esc(Examen.claveJustificacion(p)) + "</p></div>" +
          '<div class="botones-fin dos" role="group" aria-label="¿Tu justificación es correcta?">' +
          '<button type="button" class="btn btn--bien" data-justif="si" data-id="' + UI.esc(id) + '" aria-pressed="' + (a.justifOk === true) + '">Correcta (+1)</button>' +
          '<button type="button" class="btn btn--mal" data-justif="no" data-id="' + UI.esc(id) + '" aria-pressed="' + (a.justifOk === false) + '">Incorrecta (0)</button></div>';
      } else {
        var sc = Examen.puntaje(p, r, a);
        html += UI.figura(p.figura) +
          '<div class="bloque"><p class="bloque__titulo">Tu respuesta</p><p>' + UI.esc(r.texto) + "</p></div>" +
          '<div class="bloque"><p class="bloque__titulo">Respuesta modelo</p><p>' + UI.esc(p.respuesta_modelo) + "</p></div>" +
          puntosClaveHTML(p, id, a.marcados || [], true) +
          '<p class="puntaje" aria-live="polite">Puntaje: ' + num(sc.obtenido) + " / 2</p>";
      }
      html += "</article>";
    });
    html += "</section>" +
      '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="resultado"' + (sinJuzgar ? " disabled" : "") + ">" +
      (sinJuzgar ? "Calificá " + sinJuzgar + (sinJuzgar === 1 ? " justificación" : " justificaciones") : "Ver resultado") + "</button></div>";
    s.vista.innerHTML = html;

    s.vista.querySelectorAll("[data-justif]").forEach(function (b) {
      b.addEventListener("click", function () {
        var e2 = est();
        var id = b.getAttribute("data-id");
        e2.auto[id] = { justifOk: b.getAttribute("data-justif") === "si" };
        guardar(e2);
        var y = window.scrollY;
        render();
        window.scrollTo(0, y);
        var mismo = s.vista.querySelector('[data-justif="' + b.getAttribute("data-justif") + '"][data-id="' + id + '"]');
        if (mismo) mismo.focus({ preventScroll: true });
      });
    });
    s.vista.querySelectorAll("[data-punto]").forEach(function (chk) {
      chk.addEventListener("change", function () {
        var e2 = est();
        var id = chk.getAttribute("data-id");
        var m = s.vista.querySelectorAll('[data-punto][data-id="' + id + '"]');
        var marcados = [];
        m.forEach(function (x) { if (x.checked) marcados.push(+x.getAttribute("data-punto")); });
        e2.auto[id] = { marcados: marcados };
        guardar(e2);
        var art = chk.closest("article");
        var sc = Examen.puntaje(s.porId[id], e2.resp[id], e2.auto[id]);
        art.querySelector(".puntaje").textContent = "Puntaje: " + num(sc.obtenido) + " / 2";
      });
    });
    s.vista.querySelector('[data-accion="resultado"]').addEventListener("click", function () {
      var e2 = est();
      e2.fase = "resultado";
      guardar(e2);
      render();
      window.scrollTo(0, 0);
    });
  }

  // ---------- Resultado ----------
  function mandarAlRepaso(e, r) {
    var hoy = SRS.hoy();
    r.items.forEach(function (it) {
      if (it.completo) return;
      var p = s.porId[it.id];
      var prev = Store.pregunta(it.id);
      var reg = SRS.aplicar(prev, "mal", {
        id: it.id, hoy: hoy, examen: Datos.indice.examen, verificar: !!p.verificar, ahora: ahora()
      });
      reg.bien = prev && prev.bien || 0;
      var resp = e.resp[it.id] || {};
      reg.resp = p.tipo === "respuesta_corta" ? String(resp.texto || "").slice(0, 2000) : (resp.op || null);
      Store.guardarPregunta(it.id, reg);
    });
    if (window.Practicar && Practicar.recargar) Practicar.recargar();
  }

  function renderResultado(e) {
    var r = Examen.resultado(s.porId, e);
    var usado = Examen.tiempoUsado(e);
    if (!e.enHistorial) {
      Store.agregarHistorial({
        fecha: SRS.hoy(), duracion: e.duracion, temas: e.temas,
        puntos: r.puntos, maximo: r.maximo, nota: r.nota, usado: usado
      });
      e.enHistorial = true;
      guardar(e);
    }
    var fallos = r.items.filter(function (x) { return !x.completo; }).length;
    var html = '<section class="pagina" aria-labelledby="h-res"><h2 id="h-res">Resultado del simulacro</h2>' +
      '<div class="nota-final"><p class="nota-final__valor">' + num(r.nota) + '<span> / 100</span></p>' +
      "<p>" + num(r.puntos) + " de " + r.maximo + " puntos</p>" +
      "<p>Tiempo usado: " + Examen.formatoTiempo(usado) + " de " + e.duracion + ":00" +
      (e.porTiempo ? " (se acabó el tiempo)" : "") + "</p></div>" +
      '<ul class="partes">' + Examen.SECCIONES.filter(function (t) { return r.partes[t].n; }).map(function (t) {
        return "<li><span>" + NOMBRE_TIPO[t] + "</span><strong>" + num(r.partes[t].obtenido) + " / " + r.partes[t].maximo + "</strong></li>";
      }).join("") + "</ul>";
    if (fallos) {
      html += e.enviados ?
        '<p class="enviado" role="status">✓ ' + fallos + (fallos === 1 ? " pregunta quedó" : " preguntas quedaron") +
        ' en <a href="#/practicar">Repaso de hoy (Practicar)</a>.</p>' :
        '<button type="button" class="btn btn--ancho" data-accion="mandar">Mandar ' + fallos +
        (fallos === 1 ? " fallo" : " fallos") + " a Repaso de hoy</button>";
    }
    html += '<h3 class="revision__titulo">Revisión</h3>';
    r.items.forEach(function (it, i) {
      var p = s.porId[it.id];
      var resp = e.resp[it.id] || {};
      var a = e.auto[it.id] || {};
      var icono = it.completo ? "✓" : it.obtenido > 0 ? "◐" : "✗";
      var clase = it.completo ? "bien" : it.obtenido > 0 ? "duda" : "mal";
      html += '<details class="revision revision--' + clase + '" data-id="' + UI.esc(it.id) + '"><summary>' +
        '<span class="revision__estado" aria-hidden="true">' + icono + "</span>" +
        "<span>" + (i + 1) + ". " + UI.esc(p.enunciado.replace(/\s+/g, " ").slice(0, 80)) + (p.enunciado.length > 80 ? "…" : "") + "</span>" +
        '<span class="revision__puntos">' + num(it.obtenido) + "/" + it.maximo + "</span></summary>" +
        '<div class="revision__cuerpo">' +
        '<p class="pregunta__enunciado">' + UI.esc(p.enunciado) + "</p>" + UI.figura(p.figura);
      if (p.tipo === "respuesta_corta") {
        html += '<div class="bloque"><p class="bloque__titulo">Tu respuesta</p><p>' + UI.esc(resp.texto || "Sin responder") + "</p></div>" +
          '<div class="bloque"><p class="bloque__titulo">Respuesta modelo</p><p>' + UI.esc(p.respuesta_modelo) + "</p></div>" +
          puntosClaveHTML(p, it.id, a.marcados || [], false);
      } else {
        var ord = Examen.ordenDe(e, p);
        html += '<div class="bloque"><p class="bloque__titulo">Tu respuesta</p><p>' + UI.esc(textoOpcion(p, resp.op, ord)) + "</p></div>" +
          '<div class="bloque"><p class="bloque__titulo">Respuesta correcta</p><p>' + UI.esc(textoOpcion(p, p.correcta, ord)) + "</p></div>";
        if (p.tipo === "verdadero_falso" && !Examen.esVerdadero(p) && resp.justif) {
          html += '<div class="bloque"><p class="bloque__titulo">Tu justificación' +
            (typeof a.justifOk === "boolean" ? (a.justifOk ? " (correcta)" : " (incorrecta)") : "") + "</p><p>" + UI.esc(resp.justif) + "</p></div>";
        }
      }
      var letras = Opciones.mapa(Examen.ordenDe(e, p));
      if (p.explicacion) html += '<div class="bloque"><p class="bloque__titulo">Explicación</p><p>' + UI.esc(Opciones.reletrar(p.explicacion, letras)) + "</p></div>";
      if (p.justificacion_oficial) html += '<div class="bloque"><p class="bloque__titulo">Justificación de la clave</p><p>' + UI.esc(p.justificacion_oficial) + "</p></div>";
      html += UI.verificar(Opciones.reletrar(p.verificar, letras)) + UI.fuentes(p) + UI.reportar(it.id, "Simulacro") + "</div></details>";
    });
    html += "</section>" +
      '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="nuevo">Nuevo simulacro</button></div>';
    s.vista.innerHTML = html;

    var m = s.vista.querySelector('[data-accion="mandar"]');
    if (m) m.addEventListener("click", function () {
      var e2 = est();
      mandarAlRepaso(e2, r);
      e2.enviados = true;
      guardar(e2);
      render();
      var ok = s.vista.querySelector(".enviado");
      if (ok) { ok.setAttribute("tabindex", "-1"); ok.focus(); }
    });
    s.vista.querySelector('[data-accion="nuevo"]').addEventListener("click", function () {
      guardar(null);
      render();
      window.scrollTo(0, 0);
    });
  }

  // ---------- Entrada ----------
  function render() {
    detenerReloj();
    var e = est();
    if (e && e.fase === "examen" && Examen.vencido(e, ahora())) {
      s.tiempoAcabado = true;
      e = Examen.terminar(e, s.porId, ahora());
      guardar(e);
    }
    if (!e) renderConfig();
    else if (e.fase === "examen") renderExamen(e);
    else if (e.fase === "autoeval") renderAutoeval(e);
    else renderResultado(e);
  }

  window.Simulacro = {
    titulo: "Simulacro",
    mostrar: function (vista) {
      if (!s.porId) {
        s.porId = {};
        Datos.preguntas.forEach(function (p) { s.porId[p.id] = p; });
      }
      var e = est();
      if (e && e.ids && e.ids.some(function (id) { return !s.porId[id]; })) {
        guardar(null); // el examen guardado usa preguntas que ya no existen
      }
      s.vista = vista;
      render();
    }
  };
})();
