// Arranque, router por hash (#/estudiar, #/practicar…), avisos y service worker.
(function () {
  "use strict";

  var vista = document.getElementById("vista");
  var titulo = document.getElementById("titulo");
  var NOMBRE_APP = "Materiales IC-0604";

  var Acerca = {
    titulo: "Acerca de",
    mostrar: function (v) {
      v.innerHTML =
        '<section class="pagina" aria-labelledby="h-acerca">' +
        '<h2 id="h-acerca">Acerca de esta herramienta</h2>' +
        '<div class="tarjeta-info">' +
        "<p><strong>Adrián Castro Ramírez</strong><br>Estudiante de Ingeniería Civil de la UCR</p>" +
        "<p>Versión " + UI.esc(self.APP_VERSION) + " · " + UI.esc(self.APP_FECHA) + "</p>" +
        "</div>" +
        '<div class="verificar" role="note"><p class="verificar__titulo">Aviso</p>' +
        "<p>El contenido se basa en el material del curso IC-0604 Materiales de Construcción (UCR). " +
        "Los ítems marcados «⚠ Verificar» deben confirmarse con el profesor.</p></div>" +
        '<div class="tarjeta-info tarjeta-info--separada">' +
        "<p>Prepara la teoría de los exámenes parciales: I examen (sábado 17 de octubre de 2026, temas 1, 2 y 3) y " +
        "II examen (miércoles 2 de diciembre de 2026, temas 4 y 8 más lo anterior).</p>" +
        "<p>Examen seleccionado: " + UI.esc(Datos.examen().titulo) + ".</p>" +
        "<p>Contenido: " + Datos.tarjetas.length + " tarjetas, " + Datos.preguntas.length + " preguntas y " +
        Datos.glosario.length + " términos de glosario.</p>" +
        "<p>Progreso: " + (Store.disponible() ?
          "se guarda en este navegador." :
          "este navegador no permite guardarlo; se pierde al cerrar la página.") + "</p>" +
        "</div>" +
        UI.reportar("general", "Acerca de") +
        "</section>";
    }
  };

  var RUTAS = {
    estudiar: window.Estudiar,
    practicar: window.Practicar,
    normas: window.Normas,
    simulacro: window.Simulacro,
    progreso: window.PantallaProgreso,
    buscar: window.PantallaBuscar,
    acerca: Acerca
  };

  function rutaActual() {
    var r = (location.hash || "").replace(/^#\/?/, "").split(/[/?]/)[0];
    return RUTAS[r] ? r : "estudiar";
  }

  function mostrar(enfocar) {
    var r = rutaActual();
    var pantalla = RUTAS[r];
    titulo.textContent = pantalla.titulo;
    document.title = pantalla.titulo + " · " + NOMBRE_APP;
    document.querySelectorAll("[data-ruta]").forEach(function (a) {
      if (a.getAttribute("data-ruta") === r) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
    var acerca = document.querySelector(".barra__acerca");
    if (r === "acerca") acerca.setAttribute("aria-current", "page"); else acerca.removeAttribute("aria-current");
    document.body.setAttribute("data-pantalla", r);
    // Normas no depende del examen: ahí el selector no se muestra.
    var sel = document.getElementById("selector-examen");
    if (sel && Datos.examenes.length > 1) sel.hidden = (r === "normas");
    try {
      pantalla.mostrar(vista);
    } catch (e) {
      vista.innerHTML = '<p class="vacio">Algo falló al mostrar esta sección. Recargá la página.</p>';
      if (window.console) console.error(e);
    }
    if (enfocar) { window.scrollTo(0, 0); vista.focus({ preventScroll: true }); }
  }

  // Selector «Examen 1 / Examen 2»: filtra Estudiar, Practicar, Simulacro y Buscar.
  function dibujarSelector() {
    var caja = document.getElementById("selector-examen");
    var grupo = document.getElementById("grupo-examen");
    if (Datos.examenes.length < 2) { caja.hidden = true; return; }
    caja.hidden = false;
    grupo.style.gridTemplateColumns = "repeat(" + Datos.examenes.length + ", 1fr)";
    grupo.innerHTML = Datos.examenes.map(function (x) {
      return '<button type="button" class="modo__opcion" data-examen="' + x.id + '" aria-pressed="' +
        (x.id === Datos.examenId) + '">Examen ' + x.id + "</button>";
    }).join("");
    grupo.querySelectorAll("[data-examen]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = +b.getAttribute("data-examen");
        if (id === Datos.examenId) return;
        Datos.seleccionar(id);
        dibujarSelector();
        mostrar(false);
        var nuevo = grupo.querySelector('[data-examen="' + id + '"]');
        if (nuevo) nuevo.focus();
      });
    });
    var curso = document.querySelector(".nav__marca-curso");
    if (curso) curso.textContent = "IC-0604 · " + Datos.examen().titulo;
  }

  function avisoAlmacen(ok) {
    var el = document.getElementById("aviso-almacen");
    if (ok) { el.hidden = true; return; }
    el.textContent = "Este navegador no permite guardar el progreso. La app funciona, pero lo que hagás se pierde al cerrarla.";
    el.hidden = false;
  }

  function registrarSW() {
    if (!("serviceWorker" in navigator) || location.protocol === "file:") return;
    // Solo se recarga cuando el usuario pidió actualizar (no en la primera instalación).
    var pidioActualizar = false;
    navigator.serviceWorker.addEventListener("controllerchange", function () {
      if (!pidioActualizar) return;
      pidioActualizar = false;
      location.reload();
    });
    navigator.serviceWorker.register("sw.js", { updateViaCache: "none" }).then(function (reg) {
      function ofrecer(sw) {
        var aviso = document.getElementById("aviso-version");
        aviso.hidden = false;
        document.getElementById("btn-actualizar").onclick = function () {
          pidioActualizar = true;
          sw.postMessage("activar");
        };
      }
      if (reg.waiting && navigator.serviceWorker.controller) ofrecer(reg.waiting);
      reg.addEventListener("updatefound", function () {
        var nuevo = reg.installing;
        if (!nuevo) return;
        nuevo.addEventListener("statechange", function () {
          if (nuevo.state === "installed" && navigator.serviceWorker.controller) ofrecer(nuevo);
        });
      });
    }).catch(function () { /* sin SW: la app sigue funcionando en línea */ });
  }

  avisoAlmacen(Store.disponible());
  Store.alCambiarDisponibilidad(avisoAlmacen);

  Datos.cargar().then(function () {
    dibujarSelector();
    window.addEventListener("hashchange", function () { mostrar(true); });
    mostrar(false);
    document.body.setAttribute("data-listo", "1");
  }).catch(function (e) {
    vista.innerHTML = '<p class="vacio">No se pudo cargar el contenido. Revisá la conexión y recargá.<br><small>' +
      UI.esc(e.message) + "</small></p>";
  });

  registrarSW();
})();
