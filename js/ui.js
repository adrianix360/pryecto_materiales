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

  function proximamente(nombre, texto) {
    return '<section class="pagina proximamente" aria-labelledby="h-prox">' +
      '<p class="proximamente__icono" aria-hidden="true">🚧</p>' +
      '<h2 id="h-prox">' + esc(nombre) + ": próximamente</h2>" +
      "<p>" + esc(texto) + "</p></section>";
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
    proximamente: proximamente,
    correoReportes: CORREO_REPORTES
  };
})();
