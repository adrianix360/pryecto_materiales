// Pantalla Buscar: búsqueda sin conexión, glosario alfabético, galería de figuras y
// lista de ítems «verificar». Los cálculos están en js/buscar.js.
(function () {
  "use strict";

  var PESTANAS = [["buscar", "Buscar"], ["glosario", "Glosario"], ["figuras", "Figuras"], ["verificar", "Verificar"]];
  var POR_GRUPO = 25;
  var TIPO_PREGUNTA = {
    seleccion_unica: "Selección única", seleccion_multiple: "Selección múltiple",
    verdadero_falso: "Falso o verdadero", respuesta_corta: "Respuesta corta"
  };
  var s = { vista: null, pestana: null, q: "", todos: {}, indice: null, figuras: null, verif: null, espera: null };

  function asegurar() {
    if (s.indice) return;
    s.indice = Buscar.indexar(Datos.tarjetas, Datos.preguntas, Datos.glosario);
    s.figuras = Buscar.figuras(Datos.tarjetas, Datos.preguntas);
    s.verif = Buscar.aVerificar(Datos.tarjetas, Datos.preguntas, Datos.glosario);
  }

  function hl(texto, q) {
    return Buscar.resaltar(texto, q).map(function (sg) {
      return sg.m ? "<mark>" + UI.esc(sg.t) + "</mark>" : UI.esc(sg.t);
    }).join("");
  }

  function corto(texto, n) {
    var t = String(texto).replace(/\s+/g, " ");
    return t.length > n ? t.slice(0, n - 1) + "…" : t;
  }

  function pestanas() {
    return '<div class="modo modo--4" role="group" aria-label="Secciones de Buscar">' +
      PESTANAS.map(function (p) {
        return '<button type="button" class="modo__opcion" data-pestana="' + p[0] + '" aria-pressed="' +
          (s.pestana === p[0]) + '">' + p[1] + "</button>";
      }).join("") + "</div>";
  }

  // ---------- Abrir en Estudiar / Practicar ----------
  function abrir(tipo, ids, etiqueta) {
    if (tipo === "tarjeta") { Estudiar.abrirLista(ids, etiqueta); location.hash = "#/estudiar"; }
    else { Practicar.abrirLista(ids, etiqueta); location.hash = "#/practicar"; }
  }

  // ---------- Detalle de un resultado ----------
  function detalle(tipo, x) {
    var html = "";
    if (tipo === "glosario") {
      html += "<p>" + UI.esc(x.definicion) + "</p>" + UI.fuentes(x);
      return html;
    }
    if (tipo === "tarjeta") {
      html += '<div class="bloque"><p class="bloque__titulo">Respuesta</p><p>' + UI.esc(x.reverso) + "</p></div>" +
        UI.figura(x.figura) + UI.verificar(x.verificar) + UI.fuentes(x) +
        '<button type="button" class="btn btn--chico" data-abrir="tarjeta" data-id="' + UI.esc(x.id) + '">Abrir en Estudiar</button>';
      return html;
    }
    html += '<p class="nota">' + UI.esc(TIPO_PREGUNTA[x.tipo] || x.tipo) +
      (x.examen ? " · " + UI.esc(Datos.etiquetaExamen(x.examen)) : " · Teoría") + "</p>";
    if (x.opciones) {
      var ok = Array.isArray(x.correcta) ? x.correcta : [x.correcta];
      html += '<ul class="puntos">' + x.opciones.map(function (o) {
        var bien = ok.indexOf(o.id) >= 0;
        return "<li" + (bien ? ' class="correcta"' : "") + ">" + UI.esc(o.id.toUpperCase() + ". " + o.texto) +
          (bien ? " <strong>✓ correcta</strong>" : "") + "</li>";
      }).join("") + "</ul>";
    } else {
      html += '<div class="bloque"><p class="bloque__titulo">Respuesta modelo</p><p>' + UI.esc(x.respuesta_modelo) + "</p></div>" +
        '<div class="bloque"><p class="bloque__titulo">Puntos clave</p><ul class="puntos">' +
        (x.puntos_clave || []).map(function (k) { return "<li>" + UI.esc(k) + "</li>"; }).join("") + "</ul></div>";
    }
    if (x.explicacion) html += '<div class="bloque"><p class="bloque__titulo">Explicación</p><p>' + UI.esc(x.explicacion) + "</p></div>";
    if (x.justificacion_oficial) html += '<div class="bloque"><p class="bloque__titulo">Justificación de la clave</p><p>' + UI.esc(x.justificacion_oficial) + "</p></div>";
    html += UI.figura(x.figura) + UI.verificar(x.verificar) + UI.fuentes(x) +
      '<button type="button" class="btn btn--chico" data-abrir="pregunta" data-id="' + UI.esc(x.id) + '">Abrir en Practicar</button>';
    return html;
  }

  function conectarDetalles(raiz) {
    raiz.querySelectorAll("details.resultado").forEach(function (d) {
      d.addEventListener("toggle", function () {
        var cuerpo = d.querySelector(".resultado__cuerpo");
        if (!d.open || cuerpo.childElementCount) return;
        var tipo = d.getAttribute("data-tipo");
        var id = d.getAttribute("data-id");
        var x = tipo === "glosario" ? Datos.glosario.filter(function (g) { return g.id === id; })[0] :
          tipo === "tarjeta" ? Datos.tarjetas.filter(function (t) { return t.id === id; })[0] :
          Datos.preguntas.filter(function (p) { return p.id === id; })[0];
        cuerpo.innerHTML = detalle(tipo, x);
        var b = cuerpo.querySelector("[data-abrir]");
        if (b) b.addEventListener("click", function () {
          abrir(tipo, [id], "De Buscar: " + corto(Buscar.tituloDe(tipo, x), 40));
        });
      });
    });
  }

  // ---------- Pestaña Buscar ----------
  function resultadosHTML() {
    var q = s.q.trim();
    if (q.replace(/\s/g, "").length < 2) {
      return { conteo: "Escribí al menos 2 letras. No importan las tildes ni las mayúsculas.", html: "" };
    }
    var res = Buscar.buscar(s.indice, q);
    if (!res.length) {
      return { conteo: "No hay resultados para «" + q + "». Probá con otra palabra o con menos palabras.", html: "" };
    }
    var grupos = Buscar.agrupar(res);
    var html = grupos.map(function (g) {
      var mostrar = s.todos[g.tipo] ? Infinity : POR_GRUPO;
      var usados = 0;
      var cuerpo = g.temas.map(function (t) {
        var items = t.items.slice(0, Math.max(0, mostrar - usados));
        usados += items.length;
        if (!items.length) return "";
        return '<h4 class="grupo-res__tema">Tema ' + t.tema + " · " + UI.esc(Datos.tituloTema(t.tema)) + "</h4>" +
          items.map(function (e) {
            var frag = Buscar.fragmento(e.cuerpo, q, 130);
            return '<details class="resultado" data-tipo="' + e.tipo + '" data-id="' + UI.esc(e.id) + '"><summary>' +
              '<span class="resultado__meta">' + UI.esc(e.subtema + " · " + (Datos.subtemas[e.subtema] || "")) +
              (e.item.verificar ? ' · <span class="texto-verificar">⚠ Verificar</span>' : "") + "</span>" +
              '<span class="resultado__titulo">' + hl(e.tipo === "pregunta" ? corto(e.titulo, 200) : e.titulo, q) + "</span>" +
              (frag ? '<span class="resultado__frag">' + hl(frag, q) + "</span>" : "") +
              '</summary><div class="resultado__cuerpo"></div></details>';
          }).join("");
      }).join("");
      var resto = g.total - Math.min(g.total, mostrar);
      return '<section class="grupo-res" aria-labelledby="g-' + g.tipo + '"><h3 id="g-' + g.tipo + '">' + g.nombre +
        ' <span class="grupo-res__n">(' + g.total + ")</span></h3>" + cuerpo +
        (resto > 0 ? '<button type="button" class="btn btn--ancho" data-todos="' + g.tipo + '">Ver ' + resto + " más</button>" : "") +
        "</section>";
    }).join("");
    var partes = grupos.map(function (g) { return g.total + " en " + g.nombre.toLowerCase(); });
    return { conteo: res.length + (res.length === 1 ? " resultado: " : " resultados: ") + partes.join(", ") + ".", html: html };
  }

  function pintarResultados() {
    var r = resultadosHTML();
    s.vista.querySelector("#conteo").textContent = r.conteo;
    var cont = s.vista.querySelector("#resultados");
    cont.innerHTML = r.html;
    conectarDetalles(cont);
    cont.querySelectorAll("[data-todos]").forEach(function (b) {
      b.addEventListener("click", function () {
        s.todos[b.getAttribute("data-todos")] = true;
        pintarResultados();
      });
    });
  }

  function pestanaBuscar() {
    return '<div class="campo campo--buscar"><label for="q">Buscar en tarjetas, preguntas y glosario</label>' +
      '<input type="search" id="q" value="' + UI.esc(s.q) + '" autocomplete="off" autocapitalize="off" spellcheck="false" ' +
      'enterkeyhint="search" placeholder="Ej.: exudación, C127, absorción"></div>' +
      '<p id="conteo" class="contador" role="status" aria-live="polite"></p><div id="resultados"></div>';
  }

  // ---------- Pestaña Glosario ----------
  function pestanaGlosario() {
    var grupos = Buscar.glosarioPorLetra(Datos.glosario);
    return '<p class="nota">' + Datos.glosario.length + " términos en orden alfabético.</p>" +
      '<div class="letras" role="group" aria-label="Ir a la letra">' + grupos.map(function (g) {
        return '<button type="button" class="letras__btn" data-letra="' + g.letra + '">' + g.letra + "</button>";
      }).join("") + "</div>" +
      grupos.map(function (g) {
        return '<section class="glosario" aria-labelledby="letra-' + g.letra + '"><h3 class="glosario__letra" id="letra-' + g.letra +
          '" tabindex="-1">' + g.letra + "</h3><dl>" + g.terminos.map(function (t) {
            return '<div class="glosario__termino" data-id="' + UI.esc(t.id) + '"><dt>' + UI.esc(t.termino) +
              ' <span class="chip">' + UI.esc(t.subtema) + "</span></dt><dd><p>" + UI.esc(t.definicion) + "</p>" +
              UI.fuentes(t) + "</dd></div>";
          }).join("") + "</dl></section>";
      }).join("");
  }

  // ---------- Pestaña Figuras ----------
  function etiquetaFigura(f) {
    var x = f.usos[0].item;
    if (f.usos[0].tipo === "pregunta" && x.examen) return Datos.etiquetaExamen(x.examen);
    return String(x.frente || "").split(" · ")[0];
  }

  function pestanaFiguras() {
    return '<p class="nota">' + s.figuras.length + " figuras. Tocá una para repasar las tarjetas o preguntas que la usan.</p>" +
      '<ul class="galeria">' + s.figuras.map(function (f, i) {
        var nT = f.usos.filter(function (u) { return u.tipo === "tarjeta"; }).length;
        var nP = f.usos.length - nT;
        var usa = nT ? "Abre " + nT + (nT === 1 ? " tarjeta" : " tarjetas") : "Abre " + nP + (nP === 1 ? " pregunta" : " preguntas");
        return '<li><button type="button" class="figura-btn" data-figura="' + i + '">' +
          '<img src="' + UI.esc(f.src) + '" alt="' + UI.esc(f.alt) + '" loading="lazy" decoding="async">' +
          '<span class="figura-btn__titulo">' + UI.esc(etiquetaFigura(f)) + "</span>" +
          '<span class="figura-btn__alt">' + UI.esc(f.alt) + "</span>" +
          '<span class="figura-btn__fuente">Fuente: ' + UI.esc(Datos.textosFuentes(f.fuente).join("; ")) + "</span>" +
          '<span class="figura-btn__usos">' + usa + " →</span></button></li>";
      }).join("") + "</ul>";
  }

  // ---------- Pestaña Verificar ----------
  function pestanaVerificar() {
    var nT = s.verif.filter(function (v) { return v.tipo === "tarjeta"; }).length;
    var nP = s.verif.filter(function (v) { return v.tipo === "pregunta"; }).length;
    var nG = s.verif.length - nT - nP;
    var html = '<p class="nota">' + s.verif.length + " ítems marcados «⚠ Verificar»: " + nT + " tarjetas y " + nP + " preguntas" +
      (nG ? " y " + nG + " términos" : "") + ". Consultalos con el profe.</p>" +
      '<div class="botones-fin">' +
      '<button type="button" class="btn btn--primario" data-accion="copiar">Copiar lista para el profe</button>' +
      (nT ? '<button type="button" class="btn" data-accion="repasar-tarjetas">Repasar las ' + nT + " tarjetas</button>" : "") +
      (nP ? '<button type="button" class="btn" data-accion="repasar-preguntas">Practicar las ' + nP + " preguntas</button>" : "") +
      '</div><p id="copiado" class="nota" role="status"></p><div id="copia-manual"></div>';
    ["glosario", "tarjeta", "pregunta"].forEach(function (tipo) {
      var lista = s.verif.filter(function (v) { return v.tipo === tipo; });
      if (!lista.length) return;
      html += '<h3 class="verif__grupo">' + Buscar.NOMBRE_TIPO[tipo] + " (" + lista.length + ")</h3>";
      var temas = [];
      lista.forEach(function (v) { if (temas.indexOf(v.tema) < 0) temas.push(v.tema); });
      temas.sort().forEach(function (t) {
        html += '<h4 class="grupo-res__tema">Tema ' + t + " · " + UI.esc(Datos.tituloTema(t)) + "</h4>";
        lista.filter(function (v) { return v.tema === t; }).forEach(function (v) {
          html += '<article class="verif-item" data-id="' + UI.esc(v.id) + '">' +
            '<p class="resultado__meta">' + UI.esc(v.id + " · " + v.subtema) + "</p>" +
            '<p class="verif-item__titulo">' + UI.esc(corto(Buscar.tituloDe(v.tipo, v.item), 220)) + "</p>" +
            UI.verificar(v.item.verificar) + UI.fuentes(v.item) +
            (v.tipo !== "glosario" ? '<button type="button" class="btn btn--chico" data-abrir="' + v.tipo + '" data-id="' + UI.esc(v.id) + '">Abrir</button>' : "") +
            "</article>";
        });
      });
    });
    return html;
  }

  function copiar() {
    var texto = Buscar.textoParaProfe(s.verif, Datos.textoFuente);
    var aviso = s.vista.querySelector("#copiado");
    function manual() {
      aviso.textContent = "No se pudo copiar solo: seleccioná el texto de abajo y copialo.";
      var box = s.vista.querySelector("#copia-manual");
      box.innerHTML = '<label class="bloque__titulo" for="texto-profe">Lista para el profe</label>' +
        '<textarea id="texto-profe" class="respuesta-texto" rows="8" readonly></textarea>';
      var ta = box.querySelector("textarea");
      ta.value = texto;
      ta.focus();
      ta.select();
    }
    try {
      navigator.clipboard.writeText(texto).then(function () {
        aviso.textContent = "✓ Lista copiada (" + s.verif.length + " ítems). Pegala en un correo o mensaje.";
      }, manual);
    } catch (e) { manual(); }
  }

  // ---------- Pantalla ----------
  function render() {
    var cuerpo = s.pestana === "glosario" ? pestanaGlosario() : s.pestana === "figuras" ? pestanaFiguras() :
      s.pestana === "verificar" ? pestanaVerificar() : pestanaBuscar();
    s.vista.innerHTML = pestanas() + '<div class="pestana" data-pestana-actual="' + s.pestana + '">' + cuerpo + "</div>";
    var v = s.vista;
    v.querySelectorAll("[data-pestana]").forEach(function (b) {
      b.addEventListener("click", function () {
        s.pestana = b.getAttribute("data-pestana");
        Store.pref("pestanaBuscar", s.pestana);
        render();
        v.querySelector('[data-pestana="' + s.pestana + '"]').focus();
      });
    });
    if (s.pestana === "buscar") {
      var q = v.querySelector("#q");
      q.addEventListener("input", function () {
        s.q = q.value;
        s.todos = {};
        clearTimeout(s.espera);
        s.espera = setTimeout(pintarResultados, 120);
      });
      q.addEventListener("keydown", function (e) { if (e.key === "Enter") q.blur(); });
      pintarResultados();
    }
    v.querySelectorAll("[data-letra]").forEach(function (b) {
      b.addEventListener("click", function () {
        var h = v.querySelector("#letra-" + b.getAttribute("data-letra"));
        h.scrollIntoView({ block: "start" });
        window.scrollBy(0, -64);
        h.focus({ preventScroll: true });
      });
    });
    v.querySelectorAll("[data-figura]").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = s.figuras[+b.getAttribute("data-figura")];
        var tarjetas = f.usos.filter(function (u) { return u.tipo === "tarjeta"; }).map(function (u) { return u.id; });
        var preguntas = f.usos.filter(function (u) { return u.tipo === "pregunta"; }).map(function (u) { return u.id; });
        var etiqueta = "De Buscar: figura " + etiquetaFigura(f);
        if (tarjetas.length) abrir("tarjeta", tarjetas, etiqueta);
        else abrir("pregunta", preguntas, etiqueta);
      });
    });
    v.querySelectorAll(".pestana > .verif-item [data-abrir], .verif-item [data-abrir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-id");
        abrir(b.getAttribute("data-abrir"), [id], "De Buscar: verificar " + id);
      });
    });
    v.querySelectorAll("[data-accion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var acc = b.getAttribute("data-accion");
        if (acc === "copiar") copiar();
        else if (acc === "repasar-tarjetas" || acc === "repasar-preguntas") {
          var tipo = acc === "repasar-tarjetas" ? "tarjeta" : "pregunta";
          abrir(tipo, s.verif.filter(function (x) { return x.tipo === tipo; }).map(function (x) { return x.id; }),
            "De Buscar: ítems a verificar");
        }
      });
    });
  }

  window.PantallaBuscar = {
    titulo: "Buscar",
    mostrar: function (vista) {
      asegurar();
      s.vista = vista;
      if (!s.pestana) {
        var p = Store.pref("pestanaBuscar");
        s.pestana = PESTANAS.some(function (x) { return x[0] === p; }) ? p : "buscar";
      }
      render();
    }
  };
})();
