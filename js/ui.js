// Piezas de interfaz compartidas: fuente legible, aviso de verificar, figura,
// botón de reporte y filtros.
(function () {
  "use strict";

  var CORREO_REPORTES = "castroramirez702@gmail.com";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function fuentes(item) {
    var refs = item.fuente || [];
    var lineas = [];
    if (item.examen) {
      lineas.push(Datos.etiquetaExamen(item.examen) + " — " + Datos.textoFuente({ doc: item.examen.doc, pag: item.examen.pag }));
    }
    lineas = lineas.concat(Datos.textosFuentes(refs));
    if (!lineas.length) return "";
    return '<div class="fuentes"><p class="fuentes__titulo">Fuente</p><ul>' +
      lineas.map(function (l) { return "<li>" + esc(l) + "</li>"; }).join("") + "</ul></div>";
  }

  function verificar(texto) {
    if (!texto) return "";
    return '<div class="verificar" role="note"><p class="verificar__titulo">⚠ Verificar con el profe</p><p>' +
      esc(texto) + "</p></div>";
  }

  function figura(fig) {
    if (!fig) return "";
    var f = Datos.textosFuentes(fig.fuente).join("; ");
    return '<figure class="figura"><img src="' + esc(fig.src) + '" alt="' + esc(fig.alt) +
      '" loading="lazy" decoding="async"><figcaption>' + esc(fig.alt) +
      (f ? " <span>(Fuente: " + esc(f) + ")</span>" : "") + "</figcaption></figure>";
  }

  function enlaceReporte(id, seccion) {
    var asunto = "Error en Materiales IC-0604: " + id;
    var cuerpo = "Ítem: " + id + "\n" +
      "Versión: " + self.APP_VERSION + "\n" +
      "Sección: " + seccion + "\n\n" +
      "Describí el error (qué dice y qué debería decir):\n\n";
    return "mailto:" + CORREO_REPORTES + "?subject=" + encodeURIComponent(asunto) +
      "&body=" + encodeURIComponent(cuerpo);
  }

  function reportar(id, seccion) {
    return '<p class="reportar"><a class="btn btn--texto btn--chico" href="' + esc(enlaceReporte(id, seccion)) +
      '" aria-label="Reportar un error en el ítem ' + esc(id) + '">⚑ Reportar un error</a></p>';
  }

  // ---------- Filtros ----------
  // estado: {tema: "" | "1".., subtema: "" | "2A".., origen: "" | "examen" | "teoria"}
  function opcionesSubtema(tema, sel) {
    var html = '<option value="">Todos</option>';
    Datos.temas.forEach(function (t) {
      if (tema && String(t.tema) !== tema) return;
      Object.keys(t.subtemas).forEach(function (c) {
        html += '<option value="' + c + '"' + (c === sel ? " selected" : "") + ">" +
          esc(c + " · " + t.subtemas[c]) + "</option>";
      });
    });
    return html;
  }

  function resumenFiltros(f, conOrigen) {
    var partes = [];
    partes.push(f.tema ? "Tema " + f.tema : "Todos los temas");
    if (f.subtema) partes.push(f.subtema);
    if (conOrigen && f.origen) partes.push(f.origen === "examen" ? "de examen" : "de teoría");
    return partes.join(" · ");
  }

  function filtros(prefijo, f, conOrigen) {
    var temas = '<option value="">Todos</option>' + Datos.temas.map(function (t) {
      return '<option value="' + t.tema + '"' + (String(t.tema) === f.tema ? " selected" : "") + ">" +
        esc(t.tema + ". " + t.titulo) + "</option>";
    }).join("");
    var origen = conOrigen ?
      '<div class="campo"><label for="' + prefijo + '-origen">Origen</label><select id="' + prefijo + '-origen" data-filtro="origen">' +
      '<option value="">Todos</option>' +
      '<option value="examen"' + (f.origen === "examen" ? " selected" : "") + ">Examen anterior</option>" +
      '<option value="teoria"' + (f.origen === "teoria" ? " selected" : "") + ">Teoría</option>" +
      "</select></div>" : "";
    return '<details class="filtros"><summary>Filtros <span class="filtros__resumen">' +
      esc(resumenFiltros(f, conOrigen)) + "</span></summary>" +
      '<div class="filtros__cuerpo">' +
      '<div class="campo"><label for="' + prefijo + '-tema">Tema</label><select id="' + prefijo + '-tema" data-filtro="tema">' + temas + "</select></div>" +
      '<div class="campo"><label for="' + prefijo + '-subtema">Subtema</label><select id="' + prefijo + '-subtema" data-filtro="subtema">' +
      opcionesSubtema(f.tema, f.subtema) + "</select></div>" +
      origen + "</div></details>";
  }

  // Conecta los select de filtros. alCambiar(f) se llama con el estado nuevo.
  function conectarFiltros(raiz, f, conOrigen, alCambiar) {
    raiz.querySelectorAll("[data-filtro]").forEach(function (sel) {
      sel.addEventListener("change", function () {
        var nuevo = { tema: f.tema, subtema: f.subtema, origen: f.origen || "" };
        nuevo[sel.getAttribute("data-filtro")] = sel.value;
        if (sel.getAttribute("data-filtro") === "tema" && nuevo.subtema && nuevo.tema &&
            nuevo.subtema.charAt(0) !== nuevo.tema) {
          nuevo.subtema = "";
        }
        alCambiar(nuevo);
      });
    });
  }

  function cumpleFiltro(item, f) {
    if (f.tema && String(item.tema) !== f.tema) return false;
    if (f.subtema && item.subtema !== f.subtema) return false;
    if (f.origen && item.origen !== f.origen) return false;
    return true;
  }

  // ---------- Repaso de hoy y meta diaria ----------
  var SEG_POR_ITEM = 45; // equivalencia para la meta: 40 min ≈ 53 ítems
  var OPCIONES_META = {
    minutos: [20, 30, 40, 45, 60, 75, 90, 120, 150, 180],
    items: [27, 40, 53, 60, 80, 100, 120, 160, 200, 240]
  };
  var MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre"];
  var DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];

  function fechaLarga(dia) {
    var p = dia.split("-");
    var f = new Date(+p[0], +p[1] - 1, +p[2], 12);
    return DIAS[f.getDay()] + " " + f.getDate() + " de " + MESES[f.getMonth()];
  }

  function modo(prefijo, actual) {
    function b(valor, texto) {
      return '<button type="button" class="modo__opcion" data-modo="' + valor + '" aria-pressed="' +
        (actual === valor) + '">' + texto + "</button>";
    }
    return '<div class="modo" role="group" aria-label="Modo de estudio" id="' + prefijo + '-modo">' +
      b("repaso", "Repaso de hoy") + b("tema", "Por tema") + "</div>";
  }

  function conectarModo(raiz, alCambiar) {
    raiz.querySelectorAll("[data-modo]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.getAttribute("aria-pressed") === "true") return;
        alCambiar(btn.getAttribute("data-modo"));
      });
    });
  }

  // Contador de la meta diaria. Es un desplegable: al tocarlo se configura la meta.
  function barraMeta() {
    var hoy = SRS.hoy();
    var d = Store.dia(hoy);
    var m = Store.meta();
    var min = Math.floor(d.seg / 60);
    var hecho = m.unidad === "minutos" ? d.seg / 60 : d.items;
    var pct = Math.min(100, Math.round(hecho / m.valor * 100));
    var texto = m.unidad === "minutos" ?
      min + " / " + m.valor + " min · " + d.items + (d.items === 1 ? " ítem" : " ítems") :
      d.items + " / " + m.valor + " ítems · " + min + " min";
    var cumplida = pct >= 100;
    var valores = OPCIONES_META[m.unidad].slice();
    if (valores.indexOf(m.valor) < 0) { valores.push(m.valor); valores.sort(function (a, b) { return a - b; }); }
    return '<details class="meta' + (cumplida ? " meta--cumplida" : "") + '" data-panel="meta">' +
      '<summary aria-label="Meta diaria: ' + esc((cumplida ? "cumplida, " : "") + texto) + '. Tocá para cambiarla.">' +
      '<span class="meta__fila"><span class="meta__texto" aria-live="polite">' +
      (cumplida ? "✓ Meta cumplida: " : "Hoy: ") + esc(texto) + "</span>" +
      '<span class="meta__cambiar" aria-hidden="true">Meta ▾</span></span>' +
      '<span class="meta__barra" aria-hidden="true"><span style="width:' + pct + '%"></span></span></summary>' +
      '<div class="filtros__cuerpo">' +
      '<div class="campo"><label for="meta-unidad">Medir en</label>' +
      '<select id="meta-unidad" data-meta="unidad">' +
      '<option value="minutos"' + (m.unidad === "minutos" ? " selected" : "") + ">Minutos</option>" +
      '<option value="items"' + (m.unidad === "items" ? " selected" : "") + ">Ítems</option></select></div>" +
      '<div class="campo"><label for="meta-valor">Meta por día</label>' +
      '<select id="meta-valor" data-meta="valor">' +
      valores.map(function (v) {
        return '<option value="' + v + '"' + (v === m.valor ? " selected" : "") + ">" + v +
          (m.unidad === "minutos" ? " min" : " ítems") + "</option>";
      }).join("") + "</select></div>" +
      '<p class="nota">Equivalencia: 40 min ≈ 53 ítems (unos ' + SEG_POR_ITEM + " s por ítem). " +
      "El tiempo cuenta desde que aparece un ítem hasta que lo calificás, con un tope de 3 min por ítem.</p>" +
      "</div></details>";
  }

  function conectarMeta(raiz, alCambiar) {
    raiz.querySelectorAll("[data-meta]").forEach(function (sel) {
      sel.addEventListener("change", function () {
        var m = Store.meta();
        var nueva = { unidad: m.unidad, valor: m.valor };
        if (sel.getAttribute("data-meta") === "unidad") {
          nueva.unidad = sel.value;
          if (nueva.unidad !== m.unidad) {
            nueva.valor = nueva.unidad === "items" ?
              Math.round(m.valor * 60 / SEG_POR_ITEM) : Math.round(m.valor * SEG_POR_ITEM / 60);
          }
        } else {
          nueva.valor = parseInt(sel.value, 10);
        }
        Store.meta(nueva);
        alCambiar();
      });
    });
  }

  // Antes de redibujar: guarda en s si los paneles (meta y filtros) están abiertos.
  // Se lee del DOM porque el evento «toggle» llega tarde si el cambio es inmediato.
  function recordarPaneles(vista, s) {
    var m = vista.querySelector("details.meta");
    var f = vista.querySelector("details.filtros:not([data-panel])");
    if (m) s.metaAbierta = m.open;
    if (f) s.filtrosAbiertos = f.open;
  }

  // Suma al día el tiempo desde «inicio» (ms), con tope de 3 min, y un ítem.
  function registrarTiempo(inicio) {
    var seg = Math.min(180, Math.max(0, (Date.now() - inicio) / 1000));
    Store.sumarDia(SRS.hoy(), seg, 1);
  }

  // res: resultado de SRS.colaRepaso; nombres: {fallados, vencidos, nuevos} en plural
  function resumenRepaso(res, conVerificar, nombres) {
    var hoy = SRS.hoy();
    var examen = Datos.indice.examen;
    var faltan = SRS.diferencia(hoy, examen);
    var cuando = faltan > 1 ? "faltan " + faltan + " días para el examen" :
      faltan === 1 ? "mañana es el examen" : faltan === 0 ? "hoy es el examen" : "el examen ya pasó";
    var chips = [
      res.fallados + " " + nombres.fallados,
      res.vencidos + " " + nombres.vencidos,
      res.nuevos + " " + nombres.nuevos
    ];
    return '<section class="repaso" aria-label="Repaso de hoy">' +
      '<p class="repaso__fecha"><strong>' + esc(fechaLarga(hoy).replace(/^./, function (c) { return c.toUpperCase(); })) +
      "</strong> · " + esc(cuando) + "</p>" +
      '<div class="chips">' + chips.map(function (c, i) {
        return '<span class="chip' + (i === 0 && res.fallados ? " chip--fallado" : "") + '">' + esc(c) + "</span>";
      }).join("") +
      (conVerificar ? '<span class="chip chip--verificar">' + conVerificar + " con ⚠ Verificar</span>" : "") +
      "</div></section>";
  }

  window.UI = {
    esc: esc,
    fuentes: fuentes,
    verificar: verificar,
    figura: figura,
    reportar: reportar,
    enlaceReporte: enlaceReporte,
    filtros: filtros,
    conectarFiltros: conectarFiltros,
    cumpleFiltro: cumpleFiltro,
    fechaLarga: fechaLarga,
    modo: modo,
    conectarModo: conectarModo,
    barraMeta: barraMeta,
    conectarMeta: conectarMeta,
    registrarTiempo: registrarTiempo,
    recordarPaneles: recordarPaneles,
    resumenRepaso: resumenRepaso,
    correoReportes: CORREO_REPORTES
  };
})();
