// Pantalla Progreso: cuenta regresiva, pendiente de hoy, racha, tiempo por día (SVG),
// dominio por tema y subtema (barras CSS), subtemas para reforzar y tus datos
// (exportar, importar y borrar). Los cálculos están en js/progreso.js.
(function () {
  "use strict";

  var DIAS_CORTOS = ["D", "L", "K", "M", "J", "V", "S"];
  var CLAVE_AVISO = "pryecto_materiales:aviso-progreso";
  var s = { vista: null, importado: null, error: "", confirmarBorrar: false };

  function num(n) { return String(n).replace(".", ","); }
  function plural(n, uno, varios) { return n + " " + (n === 1 ? uno : varios); }

  function diaSemana(dia) {
    var p = dia.split("-");
    return new Date(+p[0], +p[1] - 1, +p[2], 12).getDay();
  }

  function metaEnMinutos() {
    var m = Store.meta();
    return m.unidad === "minutos" ? m.valor : Math.round(m.valor * 45 / 60);
  }

  // ---------- Bloques ----------
  function cuentaRegresiva(hoy) {
    var examen = Datos.indice.examen;
    var faltan = SRS.diferencia(hoy, examen);
    var titulo = faltan > 1 ? '<p class="cuenta__num">' + faltan + '</p><p class="cuenta__texto">días para el I examen</p>' :
      faltan === 1 ? '<p class="cuenta__num">1</p><p class="cuenta__texto">día: mañana es el I examen</p>' :
      faltan === 0 ? '<p class="cuenta__texto cuenta__texto--grande">Hoy es el I examen</p>' :
      '<p class="cuenta__texto cuenta__texto--grande">El I examen ya pasó</p>';
    return '<section class="cuenta" aria-label="Cuenta regresiva">' + titulo +
      '<p class="nota">' + UI.esc(UI.fechaLarga(examen).replace(/^./, function (c) { return c.toUpperCase(); })) +
      ", 8:00 a. m.</p></section>";
  }

  function resumen(hoy) {
    var examen = Datos.indice.examen;
    var colaT = SRS.colaRepaso(Datos.tarjetas, Store.tarjeta, hoy, examen);
    var colaP = SRS.colaRepaso(Datos.preguntas, Store.pregunta, hoy, examen);
    var sinVer = Datos.tarjetas.filter(function (t) { return !Store.tarjeta(t.id); }).length +
      Datos.preguntas.filter(function (p) { return !Store.pregunta(p.id); }).length;
    var r = Progreso.racha(Store.todo().diario, hoy);
    var pend = colaT.ids.length + colaP.ids.length;
    return '<div class="kpis">' +
      '<div class="kpi kpi--ancho"><p class="kpi__valor">' + pend + '</p><p class="kpi__nombre">pendientes hoy</p>' +
      '<p class="kpi__detalle">' + plural(colaT.ids.length, "tarjeta", "tarjetas") + " · " + plural(colaP.ids.length, "pregunta", "preguntas") + "</p></div>" +
      '<div class="kpi"><p class="kpi__valor">' + sinVer + '</p><p class="kpi__nombre">sin ver</p>' +
      '<p class="kpi__detalle">de ' + (Datos.tarjetas.length + Datos.preguntas.length) + " ítems</p></div>" +
      '<div class="kpi"><p class="kpi__valor">' + r.dias + '</p><p class="kpi__nombre">' + (r.dias === 1 ? "día" : "días") + " de racha</p>" +
      '<p class="kpi__detalle">' + (r.incluyeHoy ? "incluye hoy" : r.dias ? "estudiá hoy para seguirla" : "empieza hoy") + "</p></div>" +
      "</div>";
  }

  function graficoTiempo(hoy) {
    var dias = Progreso.porDia(Store.todo().diario, hoy, 7);
    var meta = metaEnMinutos();
    var max = Math.max(meta, 1, Math.max.apply(null, dias.map(function (d) { return d.min; }))) * 1.18;
    var W = 350, H = 190, base = 150, alto = 120, paso = W / 7, ancho = 30;
    var y = function (v) { return base - v / max * alto; };
    var svg = '<svg class="grafico" viewBox="0 0 ' + W + " " + H + '" aria-hidden="true" focusable="false">';
    svg += '<line class="grafico__eje" x1="0" x2="' + W + '" y1="' + base + '" y2="' + base + '"/>';
    dias.forEach(function (d, i) {
      var x = i * paso + (paso - ancho) / 2;
      var cx = i * paso + paso / 2;
      var h = Math.max(d.min ? 3 : 0, base - y(d.min));
      var clase = d.dia === hoy ? "grafico__barra grafico__barra--hoy" : "grafico__barra";
      svg += '<rect class="' + clase + '" x="' + x + '" y="' + (base - h) + '" width="' + ancho + '" height="' + h + '" rx="4"/>';
      svg += '<text class="grafico__valor" x="' + cx + '" y="' + (base - h - 6) + '" text-anchor="middle">' + d.min + "</text>";
      svg += '<text class="grafico__dia" x="' + cx + '" y="' + (base + 24) + '" text-anchor="middle">' +
        DIAS_CORTOS[diaSemana(d.dia)] + " " + (+d.dia.slice(8)) + "</text>";
    });
    svg += '<line class="grafico__meta" x1="0" x2="' + W + '" y1="' + y(meta) + '" y2="' + y(meta) + '"/>';
    svg += '<text class="grafico__meta-texto" x="' + W + '" y="' + (y(meta) - 6) + '" text-anchor="end">meta ' + meta + "</text>";
    svg += "</svg>";
    var lista = '<ul class="solo-lector">' + dias.map(function (d) {
      return "<li>" + UI.esc(UI.fechaLarga(d.dia)) + ": " + d.min + " min, " + plural(d.items, "ítem", "ítems") + "</li>";
    }).join("") + "</ul>";
    var hoyD = dias[dias.length - 1];
    var semana = dias.reduce(function (a, d) { return a + d.min; }, 0);
    return '<section class="bloque-progreso" aria-labelledby="h-tiempo"><h3 id="h-tiempo">Tiempo de estudio</h3>' +
      '<p class="nota">Hoy: ' + hoyD.min + " / " + meta + " min · últimos 7 días: " + semana + " min</p>" +
      svg + lista + "</section>";
  }

  function barra(valor, etiqueta) {
    return '<span class="medidor" aria-hidden="true"><span style="width:' + valor + '%"></span></span>' +
      '<span class="medidor__valor">' + (etiqueta || valor + " %") + "</span>";
  }

  function dominio() {
    var d = Progreso.dominio(Datos.tarjetas, Datos.preguntas, Store.tarjeta, Store.pregunta);
    var g = d.global;
    var html = '<section class="bloque-progreso" aria-labelledby="h-dominio"><h3 id="h-dominio">Dominio por tema</h3>' +
      '<p class="nota">Dominio: ítems cuya última calificación fue «la sabía» o «bien». Aciertos: respuestas bien entre todos los intentos.</p>' +
      '<p class="dominio__global"><strong>General: ' + g.dominio + " % dominado</strong>" +
      (g.aciertos == null ? "" : " · " + g.aciertos + " % de aciertos") + "</p>";
    d.temas.forEach(function (t) {
      html += '<details class="dominio" data-tema="' + t.tema + '"><summary>' +
        '<span class="dominio__nombre">' + UI.esc(t.tema + ". " + Datos.tituloTema(t.tema)) + "</span>" +
        '<span class="dominio__fila">' + barra(t.dominio) + "</span></summary>" +
        '<ul class="dominio__subtemas">' + t.subtemas.map(function (sub) {
          return '<li data-subtema="' + sub.subtema + '"><span class="dominio__nombre">' +
            UI.esc(sub.subtema + " · " + (Datos.subtemas[sub.subtema] || "")) + "</span>" +
            '<span class="dominio__fila">' + barra(sub.dominio) + "</span>" +
            '<span class="nota">' + sub.vistos + " de " + sub.total + " vistos" +
            (sub.aciertos == null ? "" : " · " + sub.aciertos + " % de aciertos") + "</span></li>";
        }).join("") + "</ul></details>";
    });
    html += "</section>";

    var deb = Progreso.debiles(d.subtemas, 3);
    var nada = Progreso.sinVer(d.subtemas);
    html += '<section class="bloque-progreso" aria-labelledby="h-reforzar"><h3 id="h-reforzar">Para reforzar</h3>';
    if (!deb.length) {
      html += '<p class="nota">Todavía no hay datos: estudiá o practicá un rato y aquí aparecen tus subtemas más débiles.</p>';
    } else {
      html += '<ul class="reforzar">' + deb.map(function (sub) {
        return '<li><p class="dominio__nombre">' + UI.esc(sub.subtema + " · " + (Datos.subtemas[sub.subtema] || "")) + "</p>" +
          '<p class="nota">' + sub.dominio + " % dominado" + (sub.aciertos == null ? "" : " · " + sub.aciertos + " % de aciertos") + "</p>" +
          '<button type="button" class="btn btn--chico" data-reforzar="' + sub.subtema + '" data-tema="' + sub.tema + '">Practicar ' + sub.subtema + "</button></li>";
      }).join("") + "</ul>";
    }
    if (nada.length) {
      html += '<p class="nota">Sin empezar: ' + nada.map(function (x) { return UI.esc(x.subtema); }).join(", ") + ".</p>";
    }
    return html + "</section>";
  }

  function datos() {
    var html = '<section class="bloque-progreso" aria-labelledby="h-datos"><h3 id="h-datos">Tus datos</h3>' +
      '<p class="nota">Tu progreso vive solo en este navegador. Para pasarlo a otro teléfono, exportalo aquí e importalo allá.</p>' +
      '<div class="botones-fin">' +
      '<button type="button" class="btn" data-accion="exportar">Exportar progreso (.json)</button>' +
      '<label class="btn btn--archivo">Importar progreso<input type="file" id="archivo-progreso" class="solo-lector" accept=".json,application/json"></label>' +
      "</div>";
    if (s.error) html += '<p class="error" role="alert">' + UI.esc(s.error) + "</p>";
    if (s.importado) {
      var r = s.importado.resumen;
      html += '<div class="verificar confirmar" role="alertdialog" aria-labelledby="h-imp" aria-describedby="p-imp">' +
        '<p class="verificar__titulo" id="h-imp">¿Cargar este progreso?</p>' +
        '<p id="p-imp">El archivo trae ' + plural(r.tarjetas, "tarjeta", "tarjetas") + ", " + plural(r.preguntas, "pregunta", "preguntas") + ", " +
        (r.normas ? plural(r.normas, "norma", "normas") + ", " : "") +
        plural(r.dias, "día", "días") + " de estudio y " + plural(r.simulacros, "simulacro", "simulacros") +
        (r.exportado ? " (exportado el " + UI.esc(UI.fechaLarga(SRS.diaDe(new Date(r.exportado)))) + ")" : "") + ".</p>" +
        '<p class="nota"><strong>Combinar</strong> conserva lo de este teléfono y agrega lo del archivo (de cada ítem queda lo más reciente). ' +
        "<strong>Reemplazar</strong> borra lo de este teléfono y deja solo lo del archivo.</p>" +
        '<div class="botones-fin">' +
        '<button type="button" class="btn btn--primario" data-accion="combinar">Combinar (recomendado)</button>' +
        '<button type="button" class="btn" data-accion="reemplazar">Reemplazar</button>' +
        '<button type="button" class="btn btn--texto" data-accion="cancelar-importar">Cancelar</button></div></div>';
    }
    html += '<div class="zona-peligro"><button type="button" class="btn btn--mal btn--ancho" data-accion="borrar">Borrar mi progreso</button></div>';
    if (s.confirmarBorrar) {
      html += '<div class="verificar confirmar" role="alertdialog" aria-labelledby="h-borrar" aria-describedby="p-borrar">' +
        '<p class="verificar__titulo" id="h-borrar">¿Borrar todo tu progreso?</p>' +
        '<p id="p-borrar">Se borran tarjetas, preguntas, normas, tiempo de estudio, racha y simulacros de este navegador. No se puede deshacer. ' +
        "La meta y los filtros se conservan. Si querés guardarlo, exportalo antes.</p>" +
        '<div class="botones-fin">' +
        '<button type="button" class="btn btn--mal" data-accion="confirmar-borrar">Sí, borrar todo</button>' +
        '<button type="button" class="btn" data-accion="exportar">Exportar primero</button>' +
        '<button type="button" class="btn btn--texto" data-accion="cancelar-borrar">Cancelar</button></div></div>';
    }
    return html + "</section>";
  }

  // ---------- Acciones ----------
  function exportar() {
    var archivo = Progreso.exportar(Store.todo(), self.APP_VERSION, Date.now());
    var blob = new Blob([JSON.stringify(archivo, null, 1)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "progreso-materiales-" + SRS.hoy() + ".json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }

  function avisarYRecargar(texto) {
    try { sessionStorage.setItem(CLAVE_AVISO, texto); } catch (e) { /* sin aviso */ }
    location.reload();
  }

  function leerArchivo(file) {
    s.error = "";
    s.importado = null;
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) { s.error = "El archivo es demasiado grande para ser un progreso."; render(); return; }
    var lector = new FileReader();
    lector.onload = function () {
      var obj;
      try { obj = JSON.parse(lector.result); } catch (e) { obj = null; }
      var v = Progreso.validar(obj);
      if (!v.ok) s.error = v.error;
      else s.importado = v;
      render();
      var foco = s.vista.querySelector(s.importado ? '[data-accion="combinar"]' : ".error");
      if (foco) { foco.setAttribute("tabindex", foco.tagName === "BUTTON" ? "0" : "-1"); foco.focus(); }
    };
    lector.onerror = function () { s.error = "No se pudo leer el archivo."; render(); };
    lector.readAsText(file);
  }

  function conectar() {
    var v = s.vista;
    v.querySelectorAll("[data-reforzar]").forEach(function (b) {
      b.addEventListener("click", function () {
        Store.pref("filtroPracticar", { tema: b.getAttribute("data-tema"), subtema: b.getAttribute("data-reforzar"), origen: "" });
        Store.pref("modoPracticar", "tema");
        if (window.Practicar && Practicar.reiniciar) Practicar.reiniciar();
        location.hash = "#/practicar";
      });
    });
    var inp = v.querySelector("#archivo-progreso");
    inp.addEventListener("change", function () { leerArchivo(inp.files && inp.files[0]); });
    v.querySelectorAll("[data-accion]").forEach(function (b) {
      b.addEventListener("click", function () {
        var acc = b.getAttribute("data-accion");
        if (acc === "exportar") exportar();
        else if (acc === "cancelar-importar") { s.importado = null; render(); }
        else if (acc === "combinar") {
          Store.reemplazarTodo(Progreso.combinar(Store.todo(), s.importado.progreso));
          s.importado = null;
          avisarYRecargar("Progreso combinado con el archivo.");
        } else if (acc === "reemplazar") {
          Store.reemplazarTodo(s.importado.progreso);
          s.importado = null;
          avisarYRecargar("Progreso reemplazado por el del archivo.");
        } else if (acc === "borrar") {
          s.confirmarBorrar = true;
          render();
          var c = v.querySelector('[data-accion="cancelar-borrar"]');
          if (c) { c.focus(); c.scrollIntoView({ block: "center" }); }
        } else if (acc === "cancelar-borrar") { s.confirmarBorrar = false; render(); }
        else if (acc === "confirmar-borrar") {
          Store.borrarProgreso();
          s.confirmarBorrar = false;
          avisarYRecargar("Se borró tu progreso.");
        }
      });
    });
  }

  function render() {
    var hoy = SRS.hoy();
    var aviso = "";
    try {
      aviso = sessionStorage.getItem(CLAVE_AVISO) || "";
      if (aviso) sessionStorage.removeItem(CLAVE_AVISO);
    } catch (e) { aviso = ""; }
    if (aviso) s.ultimoAviso = aviso;
    var html = (s.ultimoAviso ? '<p class="enviado" role="status">✓ ' + UI.esc(s.ultimoAviso) + "</p>" : "") +
      '<section class="pagina" aria-label="Tu progreso">' +
      cuentaRegresiva(hoy) + resumen(hoy) + graficoTiempo(hoy) + dominio() + datos() + "</section>";
    s.vista.innerHTML = html;
    conectar();
  }

  window.PantallaProgreso = {
    titulo: "Progreso",
    mostrar: function (vista) {
      s.vista = vista;
      s.ultimoAviso = "";
      s.error = "";
      render();
    }
  };
})();
