// Normas: entrenamiento de memoria de las normas ASTM («cuál es cuál»).
// Dos tipos de ficha por norma (lógica en js/normas-logica.js, repetición espaciada en js/srs.js):
//   · Escribir: se lee qué determina y se escribe el número de la norma, como en el examen.
//   · ¿Qué determina?: se ve la norma y se elige entre opciones de normas parecidas.
// Inicio: repaso de hoy (SRS), parejas que se confunden, práctica por familia y lista de consulta.
// Una ficha respondida mal vuelve 4 lugares después, igual que en Practicar.
(function () {
  "use strict";

  var NL = window.NormasLogica;
  var REINSERTAR_MAL = 4;
  var MAS_NUEVAS = 10;
  var NOMBRES_RESUMEN = { fallados: "fichas falladas", vencidos: "vencidas", nuevos: "nuevas" };
  var PAREJAS_A_PRACTICAR = 3;
  var PAREJAS_A_MOSTRAR = 5;

  var s = {
    vista: "hub", cola: [], pos: 0, extra: null, fase: "pregunta", letra: "C", texto: "",
    resultado: null, resp: null, opciones: null, inicio: Date.now(), metaAbierta: false
  };

  function leer(clave) { return Store.norma(clave); }
  function esc(x) { return UI.esc(x); }

  var cacheItems = null;
  function todos() {
    if (!cacheItems) {
      cacheItems = NL.items(Datos.normas, Datos.familias);
      cacheItems.porId = {};
      cacheItems.forEach(function (it) { cacheItems.porId[it.id] = it; });
    }
    return cacheItems;
  }

  function designacion(id) { return Datos.normaPorId[id] ? Datos.normaPorId[id].designacion : "ASTM " + id; }

  function nuevaCola(ids, extra) {
    s.vista = "sesion";
    s.cola = ids;
    s.pos = 0;
    s.extra = extra || null;
    reiniciarFicha();
  }

  function reiniciarFicha() {
    s.fase = "pregunta";
    s.letra = "C";
    s.texto = "";
    s.resultado = null;
    s.resp = null;
    s.opciones = null;
    s.inicio = Date.now();
  }

  // ---------- Inicio ----------
  function conteoFamilia(f) {
    var delas = Datos.normas.filter(function (n) { return n.familia === f.id; });
    var dom = delas.filter(function (n) { return NL.dominada(leer(NL.claveE(n.id))); }).length;
    return { total: delas.length, dominadas: dom };
  }

  function htmlHub() {
    var hoy = SRS.hoy();
    var res = SRS.colaRepaso(todos(), leer, hoy, Datos.indice.examen);
    var dom = Datos.normas.filter(function (n) { return NL.dominada(leer(NL.claveE(n.id))); }).length;
    var total = Datos.normas.length;
    var html = UI.barraMeta() +
      '<section class="pagina" aria-labelledby="h-normas"><h2 id="h-normas">Normas ASTM de memoria</h2>' +
      "<p>El examen pide escribir el número de la norma. Acá practicás justo eso, y también el camino inverso: " +
      "qué determina cada una. Una norma queda <strong>dominada</strong> cuando la escribís bien en " + NL.DIAS_DOMINIO +
      " días distintos.</p>" +
      '<p class="norma-progreso"><strong>' + dom + " de " + total + "</strong> normas dominadas</p>" +
      '<span class="nbarra" aria-hidden="true"><span style="width:' + Math.round(dom / total * 100) + '%"></span></span>' +
      UI.resumenRepaso(res, 0, NOMBRES_RESUMEN);
    if (res.ids.length) {
      html += '<div class="botones-fin"><button type="button" class="btn btn--primario" data-accion="repaso">Entrenar hoy · ' +
        res.ids.length + (res.ids.length === 1 ? " ficha" : " fichas") + "</button></div>";
    } else {
      var nuevas = SRS.masNuevos(todos(), leer, MAS_NUEVAS, []);
      var adel = SRS.adelantar(todos(), leer, hoy);
      html += '<p class="nota">No tenés fichas pendientes hoy. Lo que vence mañana sale en el repaso de mañana.</p><div class="botones-fin">';
      if (nuevas.length) html += '<button type="button" class="btn btn--primario" data-accion="nuevas">Seguir con ' + nuevas.length + " nuevas</button>";
      if (adel.length) html += '<button type="button" class="btn" data-accion="adelantar">Adelantar repaso (' + adel.length + ")</button>";
      html += "</div>";
    }

    var pares = NL.parejas(Datos.normas, leer);
    if (pares.length) {
      html += '<h3 class="norma-sub">Parejas que confundís</h3><ul class="fam-lista">' +
        pares.slice(0, PAREJAS_A_MOSTRAR).map(function (p) {
          return '<li class="fam-item"><div class="fam-item__fila"><span>' + esc(designacion(p.a)) + " ↔ " + esc(designacion(p.b)) +
            "</span><span>" + p.n + (p.n === 1 ? " fallo" : " fallos") + "</span></div></li>";
        }).join("") + '</ul><div class="botones-fin"><button type="button" class="btn" data-accion="parejas">Practicar estas parejas</button></div>';
    }

    html += '<h3 class="norma-sub">Por familia</h3><ul class="fam-lista">' + Datos.familias.map(function (f) {
      var c = conteoFamilia(f);
      return '<li class="fam-item"><div class="fam-item__fila"><span>' + esc(f.titulo) + "</span><span>" +
        c.dominadas + "/" + c.total + '</span></div><span class="nbarra" aria-hidden="true"><span style="width:' +
        Math.round(c.dominadas / c.total * 100) + '%"></span></span>' +
        '<button type="button" class="btn btn--chico" data-familia="' + esc(f.id) + '">Practicar ' + esc(f.titulo.split(":")[0].toLowerCase()) + "</button></li>";
    }).join("") + "</ul>" +
      '<div class="botones-fin"><button type="button" class="btn" data-accion="lista">Ver la lista de normas</button></div></section>';
    return html;
  }

  // ---------- Lista de consulta ----------
  function htmlLista() {
    var html = '<section class="pagina" aria-labelledby="h-lista"><h2 id="h-lista">Lista de normas</h2>' +
      '<div class="botones-fin"><button type="button" class="btn btn--chico" data-accion="hub">← Volver a Normas</button></div>' +
      '<p>Léela antes de practicar. Cada norma trae una ayuda de memoria y con cuáles se confunde.</p>';
    Datos.familias.forEach(function (f) {
      html += '<h3 class="norma-sub">' + esc(f.titulo) + "</h3>";
      Datos.normas.filter(function (n) { return n.familia === f.id; }).forEach(function (n) {
        html += '<article class="tarjeta-info norma-ficha"><p class="norma-codigo">' + esc(n.designacion) + "</p>" +
          "<p>" + esc(n.mide) + "</p>" +
          (n.detalle ? '<p class="norma-detalle">' + esc(n.detalle) + "</p>" : "") +
          '<p class="norma-gancho"><strong>Ayuda de memoria:</strong> ' + esc(n.gancho) + "</p>" +
          '<p class="norma-detalle">Se confunde con: ' + n.confunde_con.map(function (id) { return esc(designacion(id)); }).join(", ") + ".</p>" +
          UI.verificar(n.verificar) + UI.fuentes(n) + "</article>";
      });
    });
    return html + "</section>";
  }

  // ---------- Ficha ----------
  function chips(it, n, prev) {
    var fam = Datos.familias.filter(function (f) { return f.id === n.familia; })[0];
    return '<div class="chips"><span class="chip">' + (it.tipo === "e" ? "Escribir la norma" : "¿Qué determina?") + "</span>" +
      '<span class="chip">' + esc(fam ? fam.titulo : n.familia) + "</span>" +
      '<span class="chip">' + (prev ? "Última vez: " + (prev.r === "bien" ? "Bien" : "Mal") : "Nueva") + "</span>" +
      (n.verificar ? '<span class="chip chip--verificar">⚠ Verificar</span>' : "") + "</div>";
  }

  function htmlRetro(it, n) {
    var ok = s.resultado === "bien";
    var titulo, extra = "";
    if (ok) {
      titulo = "✓ Correcto: " + n.designacion;
    } else if (it.tipo === "e") {
      titulo = "✗ Era " + n.designacion;
      if (s.resp && Datos.normaPorId[s.resp]) {
        extra = "<p>Escribiste " + esc(designacion(s.resp)) + ": " + esc(Datos.normaPorId[s.resp].mide) + ".</p>";
      } else if (s.resp) {
        extra = "<p>Escribiste «" + esc(s.resp) + "», que no está en la lista.</p>";
      } else {
        extra = "<p>Respondiste «No sé».</p>";
      }
    } else {
      titulo = "✗ Incorrecto. " + n.designacion + " determina:";
      var elegida = s.resp && Datos.normaPorId[s.resp];
      if (elegida) extra = "<p>Elegiste lo que determina la " + esc(elegida.designacion) + ": " + esc(elegida.mide) + ".</p>";
    }
    return '<div class="retro retro--' + (ok ? "bien" : "mal") + '" id="retro" tabindex="-1" aria-live="polite">' +
      '<h3 class="retro__titulo">' + esc(titulo) + "</h3>" + extra +
      '<div class="bloque"><p class="bloque__titulo">Qué determina</p><p>' + esc(n.mide) + "</p>" +
      (n.detalle ? '<p class="norma-detalle">' + esc(n.detalle) + "</p>" : "") + "</div>" +
      '<div class="bloque"><p class="bloque__titulo">Ayuda de memoria</p><p>' + esc(n.gancho) + "</p></div>" +
      '<div class="bloque"><p class="bloque__titulo">Se confunde con</p><p>' +
      n.confunde_con.map(function (id) { return esc(designacion(id) + ": " + Datos.normaPorId[id].mide); }).join("\n") + "</p></div>" +
      UI.verificar(n.verificar) + UI.fuentes(n) + "</div>";
  }

  function htmlFichaEscribir(n) {
    var resuelta = s.fase === "respondida";
    return '<h2 class="pregunta__enunciado" id="enunciado">¿Qué norma ASTM es?</h2><p class="norma-mide">' + esc(n.mide) + "</p>" +
      '<form id="forma-norma" autocomplete="off"><div class="norma-letras" role="group" aria-label="Letra de la norma">' +
      NL.LETRAS.map(function (l) {
        return '<button type="button" class="norma-letra" data-letra="' + l + '" aria-pressed="' + (s.letra === l) + '"' + (resuelta ? " disabled" : "") + ">" + l + "</button>";
      }).join("") + "</div>" +
      '<div class="norma-entrada"><span class="prefijo" aria-hidden="true">ASTM ' + esc(s.letra) + '</span>' +
      '<input id="numero" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="5" enterkeyhint="done" autocomplete="off" ' +
      'autocapitalize="off" spellcheck="false" aria-label="Número de la norma" placeholder="000" value="' + esc(s.texto) + '"' +
      (resuelta ? " readonly" : "") + "></div></form>";
  }

  function htmlFichaInversa(n) {
    var resuelta = s.fase === "respondida";
    return '<h2 class="pregunta__enunciado" id="enunciado"><span class="norma-codigo">' + esc(n.designacion) + "</span><br>¿Qué determina?</h2>" +
      '<ul class="opciones" role="list">' + s.opciones.map(function (o, i) {
        var clase = "opcion", estado = "";
        if (resuelta) {
          if (o.norma === n.id) { clase += " es-correcta"; estado = s.resp === o.norma ? "✓ Tu respuesta" : "✓ Correcta"; }
          else if (s.resp === o.norma) { clase += " es-incorrecta"; estado = "✗ Tu respuesta"; }
        }
        var letra = "ABCD".charAt(i);
        return '<li><button type="button" class="' + clase + '" data-opcion="' + esc(o.norma) + '"' + (resuelta ? " disabled" : "") + ">" +
          '<span class="opcion__letra" aria-hidden="true">' + letra + "</span>" +
          '<span class="opcion__texto"><span class="solo-lector">Opción ' + letra + ": </span>" + esc(o.texto) + "</span>" +
          (estado ? '<span class="opcion__estado">' + esc(estado) + "</span>" : "") + "</button></li>";
      }).join("") + "</ul>";
  }

  function htmlAcciones(it) {
    if (s.fase === "respondida") {
      return '<div class="acciones"><button type="button" class="btn btn--primario" data-accion="siguiente">Siguiente →</button></div>';
    }
    if (it.tipo === "e") {
      return '<div class="acciones"><button type="button" class="btn" data-accion="nose">No sé</button>' +
        '<button type="submit" form="forma-norma" class="btn btn--primario">Comprobar</button></div>';
    }
    return "";
  }

  function htmlFin() {
    var hoy = SRS.hoy();
    var nuevas = SRS.masNuevos(todos(), leer, MAS_NUEVAS, []);
    var adel = SRS.adelantar(todos(), leer, hoy);
    var titulo = s.cola.length ? "Terminaste la ronda" : "No hay fichas para esta ronda";
    var html = '<section class="tarjeta-info" aria-labelledby="h-fin"><h2 id="h-fin">' + titulo + "</h2>" +
      (s.cola.length ? "<p>Pasaste por " + new Set(s.cola).size + " fichas.</p>" : "") + "</section>" +
      '<div class="botones-fin">';
    if (nuevas.length) html += '<button type="button" class="btn btn--primario" data-accion="nuevas">Seguir con ' + nuevas.length + " nuevas</button>";
    if (adel.length) html += '<button type="button" class="btn" data-accion="adelantar">Adelantar repaso (' + adel.length + ")</button>";
    html += '<button type="button" class="btn" data-accion="hub">Volver a Normas</button></div>';
    return html;
  }

  function render(vista) {
    if (s.vista === "hub") {
      var m = vista.querySelector("details.meta");
      if (m) s.metaAbierta = m.open;
      vista.innerHTML = htmlHub();
      return conectar(vista);
    }
    if (s.vista === "lista") { vista.innerHTML = htmlLista(); return conectar(vista); }
    if (s.pos >= s.cola.length) { vista.innerHTML = htmlFin(); return conectar(vista); }

    var it = todos().porId[s.cola[s.pos]];
    var n = Datos.normaPorId[it.norma];
    var prev = leer(it.id);
    if (it.tipo === "i" && !s.opciones) s.opciones = NL.opcionesInversa(n, Datos.normas, Datos.normaPorId);
    var html = '<p class="contador"><button type="button" class="btn btn--texto btn--chico" data-accion="hub">← Salir</button> ' +
      "Ficha " + Math.min(s.pos + 1, s.cola.length) + " de " + s.cola.length +
      (s.extra ? " · " + esc(s.extra) : "") + "</p>" + chips(it, n, prev) +
      '<section class="pregunta" data-id="' + esc(it.id) + '" aria-labelledby="enunciado">' +
      (it.tipo === "e" ? htmlFichaEscribir(n) : htmlFichaInversa(n)) +
      (s.fase === "respondida" ? htmlRetro(it, n) + UI.reportar(it.id, "Normas") : "") +
      "</section>" + htmlAcciones(it);
    vista.innerHTML = html;
    conectar(vista);
  }

  function cerrar(vista, it, ok, resp, conf) {
    s.resultado = ok ? "bien" : "mal";
    s.resp = resp;
    s.fase = "respondida";
    var reg = NL.registrar(leer(it.id), it.tipo, ok, {
      id: it.id, hoy: SRS.hoy(), examen: Datos.indice.examen, verificar: it.verificar, ahora: Date.now(), conf: conf
    });
    Store.guardarNorma(it.id, reg);
    UI.registrarTiempo(s.inicio);
    if (!ok) s.cola.splice(Math.min(s.pos + 1 + REINSERTAR_MAL, s.cola.length), 0, it.id);
    render(vista);
    var r = vista.querySelector("#retro");
    if (r) r.focus();
  }

  function siguiente(vista) {
    s.pos++;
    reiniciarFicha();
    render(vista);
    var inp = vista.querySelector("#numero");
    var e = inp || vista.querySelector("#enunciado");
    if (e) { if (!inp) e.setAttribute("tabindex", "-1"); e.focus({ preventScroll: true }); }
    window.scrollTo(0, 0);
  }

  function conectar(vista) {
    var det = vista.querySelector("details.meta");
    if (det) {
      det.open = s.metaAbierta;
      det.addEventListener("toggle", function () { s.metaAbierta = det.open; });
    }
    UI.conectarMeta(vista, function () {
      render(vista);
      var sel = vista.querySelector("[data-meta]");
      if (sel) sel.focus();
    });

    vista.querySelectorAll("[data-familia]").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-familia");
        var ids = Datos.normas.filter(function (n) { return n.familia === f; }).map(function (n) { return n.id; });
        nuevaCola(NL.itemsDe(todos(), ids).map(function (it) { return it.id; }), "familia");
        render(vista); window.scrollTo(0, 0);
      });
    });

    var it = s.vista === "sesion" && s.pos < s.cola.length ? todos().porId[s.cola[s.pos]] : null;
    var n = it ? Datos.normaPorId[it.norma] : null;

    vista.querySelectorAll("[data-letra]").forEach(function (b) {
      b.addEventListener("click", function () {
        s.letra = b.getAttribute("data-letra");
        vista.querySelectorAll("[data-letra]").forEach(function (x) {
          x.setAttribute("aria-pressed", String(x === b));
        });
        var pref = vista.querySelector(".prefijo");
        if (pref) pref.textContent = "ASTM " + s.letra;
        var inp = vista.querySelector("#numero");
        if (inp) inp.focus({ preventScroll: true });
      });
    });

    var inp = vista.querySelector("#numero");
    var forma = vista.querySelector("#forma-norma");
    if (inp) {
      inp.addEventListener("input", function () { s.texto = inp.value; });
      if (s.fase === "pregunta") inp.focus({ preventScroll: true });
    }
    if (forma) {
      forma.addEventListener("submit", function (e) {
        e.preventDefault();
        if (s.fase !== "pregunta") return;
        var resp = NL.parsear(s.letra, s.texto);
        if (!resp) { inp.focus(); return; } // sin número no se califica
        var r = NL.evaluarEscribir(n, resp, Datos.normaPorId);
        cerrar(vista, it, r.ok, resp, r.conf);
      });
    }

    vista.querySelectorAll("[data-opcion]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (s.fase !== "pregunta") return;
        var id = b.getAttribute("data-opcion");
        cerrar(vista, it, id === n.id, id, id === n.id ? null : id);
      });
    });

    vista.querySelectorAll("[data-accion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var acc = b.getAttribute("data-accion");
        var hoy = SRS.hoy();
        if (acc === "nose") {
          if (s.fase === "pregunta") cerrar(vista, it, false, null, null);
        } else if (acc === "siguiente") {
          siguiente(vista);
        } else if (acc === "hub") {
          s.vista = "hub"; render(vista); window.scrollTo(0, 0);
        } else if (acc === "lista") {
          s.vista = "lista"; render(vista); window.scrollTo(0, 0);
        } else if (acc === "repaso") {
          nuevaCola(SRS.colaRepaso(todos(), leer, hoy, Datos.indice.examen).ids.slice(), "repaso de hoy");
          render(vista); window.scrollTo(0, 0);
        } else if (acc === "nuevas") {
          nuevaCola(SRS.masNuevos(todos(), leer, MAS_NUEVAS, []), "nuevas");
          render(vista); window.scrollTo(0, 0);
        } else if (acc === "adelantar") {
          nuevaCola(SRS.adelantar(todos(), leer, hoy), "repaso adelantado");
          render(vista); window.scrollTo(0, 0);
        } else if (acc === "parejas") {
          var ids = [];
          NL.parejas(Datos.normas, leer).slice(0, PAREJAS_A_PRACTICAR).forEach(function (p) {
            [p.a, p.b].forEach(function (id) { if (ids.indexOf(id) < 0) ids.push(id); });
          });
          nuevaCola(NL.itemsDe(todos(), ids).map(function (x) { return x.id; }), "parejas que confundís");
          render(vista); window.scrollTo(0, 0);
        }
      });
    });
  }

  window.Normas = {
    titulo: "Normas",
    mostrar: function (vista) {
      if (s.vista === "sesion" && s.pos >= s.cola.length) s.vista = "hub";
      render(vista);
    }
  };
})();
