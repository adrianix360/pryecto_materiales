// Orden aleatorio de las opciones de selección única y múltiple, para que la respuesta
// correcta no caiga siempre en la misma letra. Las letras que se muestran siguen siendo
// A, B, C… en orden; lo que cambia es qué opción va en cada letra.
// Las explicaciones citan las opciones por su letra original («Correcta la B. La A es…»):
// reletrar() las cambia por la letra que se ve.
// Módulo puro: funciona en el navegador (window.Opciones) y en Node (module.exports).
(function (root) {
  "use strict";

  var LETRAS = "ABCDEFGH";

  function barajar(lista, rnd) {
    rnd = rnd || Math.random;
    var a = lista.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1));
      var x = a[i]; a[i] = a[j]; a[j] = x;
    }
    return a;
  }

  // Opciones que dependen de su lugar («Ninguna de las anteriores»): no se mueven.
  var FIJA = /\banteriores?\b/i;

  // Orden de los ids de opción para mostrar. Falso o verdadero queda fijo (V, F).
  function ordenPara(p, rnd) {
    var ops = p.opciones || [];
    var ids = ops.map(function (o) { return o.id; });
    if (p.tipo !== "seleccion_unica" && p.tipo !== "seleccion_multiple") return ids;
    var libres = barajar(ops.filter(function (o) { return !FIJA.test(o.texto); })
      .map(function (o) { return o.id; }), rnd);
    return ops.map(function (o) { return FIJA.test(o.texto) ? o.id : libres.shift(); });
  }

  // Letra que se muestra para una opción (por su id original).
  function letra(orden, id) {
    var i = orden.indexOf(id);
    return i < 0 ? String(id).toUpperCase() : LETRAS[i];
  }

  // {letra original en mayúscula: letra que se muestra}
  function mapa(orden) {
    var m = {};
    orden.forEach(function (id, i) { m[String(id).toUpperCase()] = LETRAS[i]; });
    return m;
  }

  // Cambia en el texto solo las letras que nombran una opción: después de «la», «las»,
  // «La», «Las», «y», «e», «(» o «, ». No toca una letra seguida de «=» o «→» (variables
  // como «w = D» o las graduaciones «A → 12»), ni letras que no sean opciones.
  var CITA = /((?:^|[^A-Za-zÀ-ÿ])(?:[Ll]as?|y|e) |\(|, )([A-H])(?![A-Za-zÀ-ÿ0-9])(?!\s*[→=])/g;

  function reletrar(texto, m) {
    if (texto == null) return texto;
    return String(texto).replace(CITA, function (todo, antes, l) {
      return antes + (m[l] || l);
    });
  }

  var Opciones = {
    LETRAS: LETRAS,
    barajar: barajar,
    ordenPara: ordenPara,
    letra: letra,
    mapa: mapa,
    reletrar: reletrar
  };

  if (typeof module !== "undefined" && module.exports) module.exports = Opciones;
  else root.Opciones = Opciones;
})(typeof self !== "undefined" ? self : this);
