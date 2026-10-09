// Núcleo de la sección Buscar: búsqueda sin tildes ni mayúsculas con resaltado,
// glosario alfabético, índice de figuras y lista de ítems «verificar».
// Módulo puro: funciona en el navegador (window.Buscar) y en Node (module.exports).
(function (root) {
  "use strict";

  var TIPOS = ["glosario", "tarjeta", "pregunta"];
  var NOMBRE_TIPO = { glosario: "Glosario", tarjeta: "Tarjetas", pregunta: "Preguntas" };

  // ---------- Normalización con mapa de posiciones ----------
  // Devuelve el texto en minúsculas y sin tildes, y para cada carácter normalizado la
  // posición del carácter original (para resaltar sobre el texto con tildes).
  function normalizarConMapa(texto) {
    var s = String(texto == null ? "" : texto);
    var n = "", mapa = [];
    for (var i = 0; i < s.length; i++) {
      var d = s[i].normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
      for (var j = 0; j < d.length; j++) { n += d[j]; mapa.push(i); }
    }
    return { n: n, mapa: mapa };
  }

  function normalizar(texto) { return normalizarConMapa(texto).n; }

  function palabras(consulta) {
    return normalizar(consulta).split(/\s+/).filter(function (w) { return w.length > 0; });
  }

  // ---------- Índice ----------
  function textoPregunta(p) {
    var partes = [];
    (p.opciones || []).forEach(function (o) { partes.push(o.texto); });
    if (p.respuesta_modelo) partes.push(p.respuesta_modelo);
    (p.puntos_clave || []).forEach(function (k) { partes.push(k); });
    if (p.explicacion) partes.push(p.explicacion);
    if (p.justificacion_oficial) partes.push(p.justificacion_oficial);
    return partes.join(" · ");
  }

  function entrada(tipo, item, titulo, cuerpo, orden) {
    return {
      tipo: tipo, id: item.id, tema: item.tema, subtema: item.subtema, item: item, orden: orden,
      titulo: titulo, cuerpo: cuerpo, nt: normalizar(titulo), nc: normalizar(cuerpo)
    };
  }

  function indexar(tarjetas, preguntas, glosario) {
    var idx = [], k = 0;
    (glosario || []).forEach(function (g) { idx.push(entrada("glosario", g, g.termino, g.definicion, k++)); });
    (tarjetas || []).forEach(function (t) { idx.push(entrada("tarjeta", t, t.frente, t.reverso, k++)); });
    (preguntas || []).forEach(function (p) { idx.push(entrada("pregunta", p, p.enunciado, textoPregunta(p), k++)); });
    return idx;
  }

  // ---------- Búsqueda ----------
  // Todas las palabras deben aparecer (en el título o en el cuerpo). Desde 2 letras.
  function buscar(indice, consulta) {
    var ws = palabras(consulta);
    var frase = ws.join(" ");
    if (frase.replace(/\s/g, "").length < 2) return [];
    var out = [];
    indice.forEach(function (e) {
      var puntos = 0;
      for (var i = 0; i < ws.length; i++) {
        var w = ws[i];
        var enTitulo = e.nt.indexOf(w) >= 0;
        if (!enTitulo && e.nc.indexOf(w) < 0) return;
        puntos += enTitulo ? 10 : 1;
        if (enTitulo && (e.nt.indexOf(w) === 0 || e.nt.indexOf(" " + w) >= 0)) puntos += 3;
      }
      if (ws.length > 1 && e.nt.indexOf(frase) >= 0) puntos += 20;
      out.push({ e: e, puntos: puntos });
    });
    out.sort(function (a, b) {
      return b.puntos - a.puntos || TIPOS.indexOf(a.e.tipo) - TIPOS.indexOf(b.e.tipo) ||
        a.e.tema - b.e.tema || a.e.orden - b.e.orden;
    });
    return out.map(function (x) { return x.e; });
  }

  // [{tipo, nombre, total, temas: [{tema, items}]}] en orden glosario, tarjetas, preguntas.
  function agrupar(resultados) {
    return TIPOS.map(function (tipo) {
      var del_tipo = resultados.filter(function (e) { return e.tipo === tipo; });
      var temas = [];
      del_tipo.forEach(function (e) {
        var g = temas.filter(function (x) { return x.tema === e.tema; })[0];
        if (!g) { g = { tema: e.tema, items: [] }; temas.push(g); }
        g.items.push(e);
      });
      temas.sort(function (a, b) { return a.tema - b.tema; });
      return { tipo: tipo, nombre: NOMBRE_TIPO[tipo], total: del_tipo.length, temas: temas };
    }).filter(function (g) { return g.total > 0; });
  }

  // ---------- Resaltado ----------
  // Segmentos [{t, m}] del texto original; m = true en lo que coincide con alguna palabra.
  function resaltar(texto, consulta) {
    var s = String(texto == null ? "" : texto);
    var ws = palabras(consulta);
    var nm = normalizarConMapa(s);
    var marcas = [];
    ws.forEach(function (w) {
      var desde = 0, i;
      while (w && (i = nm.n.indexOf(w, desde)) >= 0) {
        marcas.push([nm.mapa[i], nm.mapa[i + w.length - 1] + 1]);
        desde = i + w.length;
      }
    });
    marcas.sort(function (a, b) { return a[0] - b[0]; });
    var unidas = [];
    marcas.forEach(function (m) {
      var u = unidas[unidas.length - 1];
      if (u && m[0] <= u[1]) u[1] = Math.max(u[1], m[1]);
      else unidas.push([m[0], m[1]]);
    });
    var segs = [], pos = 0;
    unidas.forEach(function (m) {
      if (m[0] > pos) segs.push({ t: s.slice(pos, m[0]), m: false });
      segs.push({ t: s.slice(m[0], m[1]), m: true });
      pos = m[1];
    });
    if (pos < s.length) segs.push({ t: s.slice(pos), m: false });
    return segs;
  }

  // Trozo del texto alrededor de la primera coincidencia (o el principio si no hay).
  function fragmento(texto, consulta, largo) {
    var s = String(texto == null ? "" : texto).replace(/\s+/g, " ");
    largo = largo || 140;
    if (s.length <= largo) return s;
    var nm = normalizarConMapa(s);
    var primera = -1;
    palabras(consulta).forEach(function (w) {
      var i = nm.n.indexOf(w);
      if (i >= 0 && (primera < 0 || nm.mapa[i] < primera)) primera = nm.mapa[i];
    });
    var ini = primera < 0 ? 0 : Math.max(0, primera - Math.floor(largo / 3));
    var fin = Math.min(s.length, ini + largo);
    ini = Math.max(0, fin - largo);
    return (ini > 0 ? "…" : "") + s.slice(ini, fin).trim() + (fin < s.length ? "…" : "");
  }

  // ---------- Glosario ----------
  function letraDe(termino) {
    var c = String(termino).trim().charAt(0);
    if (c === "ñ" || c === "Ñ") return "Ñ";
    return normalizar(c).toUpperCase();
  }

  // [{letra, terminos}] ordenado alfabéticamente en español.
  function glosarioPorLetra(terminos) {
    var orden = terminos.slice().sort(function (a, b) {
      return a.termino.localeCompare(b.termino, "es", { sensitivity: "base" });
    });
    var grupos = [];
    orden.forEach(function (t) {
      var l = letraDe(t.termino);
      var g = grupos[grupos.length - 1];
      if (!g || g.letra !== l) { g = { letra: l, terminos: [] }; grupos.push(g); }
      g.terminos.push(t);
    });
    return grupos;
  }

  // ---------- Figuras ----------
  // [{src, alt, fuente, usos: [{tipo, id, item}]}]: primero las de ensayos, en orden de datos.
  function figuras(tarjetas, preguntas) {
    var por = {}, orden = [];
    function agregar(tipo, x) {
      if (!x.figura || !x.figura.src) return;
      var f = por[x.figura.src];
      if (!f) {
        f = { src: x.figura.src, alt: x.figura.alt, fuente: x.figura.fuente || [], usos: [] };
        por[x.figura.src] = f;
        orden.push(x.figura.src);
      }
      f.usos.push({ tipo: tipo, id: x.id, item: x });
    }
    (tarjetas || []).forEach(function (t) { agregar("tarjeta", t); });
    (preguntas || []).forEach(function (p) { agregar("pregunta", p); });
    return orden.map(function (k) { return por[k]; });
  }

  // ---------- Verificar ----------
  function aVerificar(tarjetas, preguntas, glosario) {
    var out = [];
    [["glosario", glosario], ["tarjeta", tarjetas], ["pregunta", preguntas]].forEach(function (par) {
      (par[1] || []).forEach(function (x) {
        if (x.verificar) out.push({ tipo: par[0], id: x.id, tema: x.tema, subtema: x.subtema, item: x });
      });
    });
    return out;
  }

  function tituloDe(tipo, x) {
    return tipo === "glosario" ? x.termino : tipo === "tarjeta" ? x.frente : x.enunciado;
  }

  // Texto plano para mandarle al profe. textoFuente(ref) da la fuente legible.
  function textoParaProfe(lista, textoFuente) {
    var lineas = ["Consultas para el profe (IC-0604, I examen): " + lista.length + " ítems", ""];
    lista.forEach(function (v, i) {
      var x = v.item;
      lineas.push((i + 1) + ". [" + v.id + "] " + String(tituloDe(v.tipo, x)).replace(/\s+/g, " "));
      lineas.push("   Duda: " + x.verificar);
      var refs = (x.fuente || []).map(textoFuente);
      if (refs.length) lineas.push("   Fuente: " + refs.join("; "));
      lineas.push("");
    });
    return lineas.join("\n");
  }

  var Buscar = {
    NOMBRE_TIPO: NOMBRE_TIPO,
    normalizar: normalizar,
    normalizarConMapa: normalizarConMapa,
    indexar: indexar,
    buscar: buscar,
    agrupar: agrupar,
    resaltar: resaltar,
    fragmento: fragmento,
    letraDe: letraDe,
    glosarioPorLetra: glosarioPorLetra,
    figuras: figuras,
    aVerificar: aVerificar,
    tituloDe: tituloDe,
    textoParaProfe: textoParaProfe
  };

  if (typeof module !== "undefined" && module.exports) module.exports = Buscar;
  else root.Buscar = Buscar;
})(typeof self !== "undefined" ? self : this);
