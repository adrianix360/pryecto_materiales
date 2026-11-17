// Carga el contenido de data/ (esquema en docs/ESQUEMA.md). Solo lectura: la app no
// modifica los JSON. Todas las rutas son relativas para funcionar bajo /nombre-del-repo/.
(function () {
  "use strict";

  var D = {
    indice: null,
    fuentes: {},
    glosario: [],
    temas: [],        // [{tema, titulo, subtemas: {codigo: titulo}}]
    subtemas: {},     // codigo -> titulo
    tarjetas: [],     // solo las del examen seleccionado (ver D.seleccionar)
    preguntas: [],
    todasTarjetas: [],  // las de todos los temas
    todasPreguntas: [],
    todoGlosario: [],
    todosTemas: [],
    examenes: [],     // [{id, titulo, fecha, temas, simulacro}]
    examenId: 1,
    familias: [],     // familias de normas, en orden de estudio
    normas: [],       // normas ASTM del entrenamiento «Normas»
    normaPorId: {}
  };

  var CLAVE_EXAMEN = "pryecto_materiales:examen:v1"; // aparte del progreso: no cambia el formato guardado
  var oyentes = [];

  // Un tema sin archivo (todavía no escrito) cuenta como vacío: la app no se rompe.
  function jsonOpcional(ruta, vacio) {
    return json(ruta).catch(function () { return vacio; });
  }

  function json(ruta) {
    return fetch(ruta).then(function (r) {
      if (!r.ok) throw new Error("No se pudo cargar " + ruta + " (" + r.status + ")");
      return r.json();
    });
  }

  D.cargar = function () {
    return Promise.all([json("data/indice.json"), json("data/fuentes.json"), json("data/glosario.json"), json("data/normas.json")])
      .then(function (r) {
        D.indice = r[0];
        D.fuentes = r[1].fuentes;
        D.todoGlosario = r[2].terminos;
        D.familias = r[3].familias;
        D.normas = r[3].normas;
        D.normas.forEach(function (n) { D.normaPorId[n.id] = n; });
        D.todosTemas = D.indice.temas.map(function (t) {
          Object.keys(t.subtemas).forEach(function (c) { D.subtemas[c] = t.subtemas[c]; });
          return { tema: t.tema, titulo: t.titulo, subtemas: t.subtemas };
        });
        // Índice viejo (sin «examenes»): un solo examen con todos los temas.
        var todos = D.todosTemas.map(function (t) { return t.tema; });
        D.examenes = (D.indice.examenes && D.indice.examenes.length) ? D.indice.examenes :
          [{ id: 1, titulo: "I examen", fecha: D.indice.examen, temas: todos, simulacro: todos }];
        return Promise.all(D.indice.temas.map(function (t) {
          return Promise.all([jsonOpcional(t.tarjetas, { tarjetas: [] }), jsonOpcional(t.preguntas, { preguntas: [] })]);
        }));
      })
      .then(function (porTema) {
        porTema.forEach(function (par) {
          D.todasTarjetas = D.todasTarjetas.concat(par[0].tarjetas || []);
          D.todasPreguntas = D.todasPreguntas.concat(par[1].preguntas || []);
        });
        D.seleccionar(leerExamen(), true);
        return D;
      });
  };

  // ---------- Examen seleccionado (I o II) ----------
  function leerExamen() {
    var id = 0;
    if (typeof window.__examenPrueba === "number") id = window.__examenPrueba;
    else {
      try { id = +window.localStorage.getItem(CLAVE_EXAMEN); } catch (e) { id = 0; }
    }
    if (D.examenes.some(function (x) { return x.id === id; })) return id;
    // Por defecto, el examen más próximo en el calendario: el último de la lista (el II).
    return D.examenes[D.examenes.length - 1].id;
  }

  function enExamen(lista, temas) {
    return lista.filter(function (x) { return temas.indexOf(x.tema) >= 0; });
  }

  // Cambia el examen y recalcula lo que ven Estudiar, Practicar, Progreso y Buscar.
  // silencioso: no avisa a los oyentes (carga inicial).
  D.seleccionar = function (id, silencioso) {
    var ex = D.examenes.filter(function (x) { return x.id === id; })[0] || D.examenes[0];
    D.examenId = ex.id;
    D.tarjetas = enExamen(D.todasTarjetas, ex.temas);
    D.preguntas = enExamen(D.todasPreguntas, ex.temas);
    D.glosario = enExamen(D.todoGlosario, ex.temas);
    D.temas = D.todosTemas.filter(function (t) { return ex.temas.indexOf(t.tema) >= 0; });
    if (silencioso) return;
    if (typeof window.__examenPrueba !== "number") {
      try { window.localStorage.setItem(CLAVE_EXAMEN, String(ex.id)); } catch (e) { /* sin almacenamiento */ }
    } else window.__examenPrueba = ex.id;
    oyentes.forEach(function (f) { try { f(ex); } catch (e) { if (window.console) console.error(e); } });
  };

  D.alCambiarExamen = function (f) { oyentes.push(f); };
  D.examen = function () {
    return D.examenes.filter(function (x) { return x.id === D.examenId; })[0] || D.examenes[0];
  };
  D.fechaExamen = function () { return D.examen().fecha; };
  // Preguntas y temas del Simulacro: el II examen es acumulativo (incluye los temas del I).
  D.preguntasSimulacro = function () { return enExamen(D.todasPreguntas, D.examen().simulacro); };
  D.temasSimulacro = function () {
    var sim = D.examen().simulacro;
    return D.todosTemas.filter(function (t) { return sim.indexOf(t.tema) >= 0; });
  };

  // «Título, pág. 8 (impresa 97), F/V 6»
  D.textoFuente = function (ref) {
    var f = D.fuentes[ref.doc];
    var t = (f ? f.titulo : "Documento " + ref.doc) + ", pág. " + ref.pag;
    if (ref.impresa) t += " (impresa " + ref.impresa + ")";
    if (ref.pregunta) t += ", " + ref.pregunta;
    return t;
  };

  // Agrupa referencias seguidas al mismo documento: «Título, págs. 11, 12 y 14».
  // Las que traen página impresa o pregunta se dejan aparte para no perder ese dato.
  D.textosFuentes = function (refs) {
    var grupos = [];
    (refs || []).forEach(function (r) {
      var ult = grupos[grupos.length - 1];
      var simple = !r.impresa && !r.pregunta;
      if (simple && ult && ult.simple && ult.doc === r.doc) {
        if (ult.pags.indexOf(r.pag) < 0) ult.pags.push(r.pag);
      } else {
        grupos.push({ doc: r.doc, pags: [r.pag], simple: simple, ref: r });
      }
    });
    return grupos.map(function (g) {
      if (!g.simple || g.pags.length === 1) return D.textoFuente(g.ref);
      var f = D.fuentes[g.doc];
      var lista = g.pags.join(", ").replace(/, ([^,]*)$/, " y $1");
      return (f ? f.titulo : "Documento " + g.doc) + ", págs. " + lista;
    });
  };

  // «Examen I-2025 · 1, pregunta 3»
  D.etiquetaExamen = function (ex) {
    if (!ex) return "";
    var periodo = String(ex.periodo || "");
    if (/^Sin /.test(periodo)) periodo = periodo.charAt(0).toLowerCase() + periodo.slice(1);
    return "Examen " + periodo + " · " + ex.pregunta;
  };

  D.tituloTema = function (n) {
    for (var i = 0; i < D.todosTemas.length; i++) if (D.todosTemas[i].tema === n) return D.todosTemas[i].titulo;
    return "Tema " + n;
  };

  window.Datos = D;
})();
