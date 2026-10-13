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
    tarjetas: [],
    preguntas: [],
    familias: [],     // familias de normas, en orden de estudio
    normas: [],       // normas ASTM del entrenamiento «Normas»
    normaPorId: {}
  };

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
        D.glosario = r[2].terminos;
        D.familias = r[3].familias;
        D.normas = r[3].normas;
        D.normas.forEach(function (n) { D.normaPorId[n.id] = n; });
        D.temas = D.indice.temas.map(function (t) {
          Object.keys(t.subtemas).forEach(function (c) { D.subtemas[c] = t.subtemas[c]; });
          return { tema: t.tema, titulo: t.titulo, subtemas: t.subtemas };
        });
        return Promise.all(D.indice.temas.map(function (t) {
          return Promise.all([json(t.tarjetas), json(t.preguntas)]);
        }));
      })
      .then(function (porTema) {
        porTema.forEach(function (par) {
          D.tarjetas = D.tarjetas.concat(par[0].tarjetas);
          D.preguntas = D.preguntas.concat(par[1].preguntas);
        });
        return D;
      });
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
    for (var i = 0; i < D.temas.length; i++) if (D.temas[i].tema === n) return D.temas[i].titulo;
    return "Tema " + n;
  };

  window.Datos = D;
})();
