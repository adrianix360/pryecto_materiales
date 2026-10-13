// Repetición espaciada (Leitner de 5 cajas) con compresión antes del examen.
// Módulo puro: no lee la fecha del sistema ni el almacenamiento; todo entra por parámetro.
// Funciona en el navegador (window.SRS) y en Node (module.exports) para las pruebas.
//
// Cajas e intervalos base:   caja 0 → hoy · 1 → 1 día · 2 → 2 días · 3 → 4 días · 4 → 7 días
// Calificación:  la sabía / bien     → sube una caja (si es la primera vez, entra a la caja 2:
//                                      ya la dominaba y no hace falta verla mañana)
//                dudosa / parcial    → baja una caja (mínimo 1)
//                no la sabía / mal   → caja 0 (fallado: vuelve hoy mismo)
// Compresión antes del examen («repaso final»):
//   · a cada ítem le toca un día de repaso final dentro de los 3 días antes del examen
//     (víspera, víspera − 1 o víspera − 2), repartidos en tercios según su id;
//   · mientras no llegue ese día, ningún intervalo lo salta: la fecha de repaso es como
//     máximo su día de repaso final;
//   · cuando ya se repasó en su día de repaso final o después, vuelve a los intervalos
//     normales: solo sale otra vez antes del examen si se falla (hoy mismo) o queda
//     dudoso (al día siguiente, si todavía no es la víspera).
// Ítems con «verificar»: caja máxima 2, para que vuelvan cada 2 días o antes.
// Nuevos por día: los que faltan por ver, repartidos entre los días que quedan antes de la
// ventana de repaso final (así esos 3 días quedan para repasar). Si ya se está en la
// ventana, se reparten hasta la víspera. Todo se ve al menos una vez antes del examen.
// Orden aleatorio: si las colas reciben «rnd» (una función que da [0, 1)), cada grupo sale
// barajado y los nuevos del día se eligen al azar; sin «rnd», el orden es el de los datos.
(function (root) {
  "use strict";

  var INTERVALOS = [0, 1, 2, 4, 7];
  var CAJA_MAX = INTERVALOS.length - 1;
  var CAJA_MAX_VERIFICAR = 2;
  var NUEVOS_SIN_EXAMEN = 20;
  var VENTANA_FINAL = 3;
  var SUBE = { sabia: true, bien: true };
  var FALLA = { no: true, mal: true };

  // ---------- Fechas como texto «AAAA-MM-DD» (día local) ----------
  function dos(n) { return (n < 10 ? "0" : "") + n; }

  function diaDe(fecha) {
    return fecha.getFullYear() + "-" + dos(fecha.getMonth() + 1) + "-" + dos(fecha.getDate());
  }

  function aNumero(dia) {
    var p = dia.split("-");
    return Math.round(Date.UTC(+p[0], +p[1] - 1, +p[2]) / 864e5);
  }

  function deNumero(n) {
    var f = new Date(n * 864e5);
    return f.getUTCFullYear() + "-" + dos(f.getUTCMonth() + 1) + "-" + dos(f.getUTCDate());
  }

  function sumar(dia, n) { return deNumero(aNumero(dia) + n); }

  // días de a hasta b (positivo si b es posterior)
  function diferencia(a, b) { return aNumero(b) - aNumero(a); }

  function vispera(examen) { return examen ? sumar(examen, -1) : null; }

  // ---------- Día de repaso final ----------
  function hash(texto) {
    var h = 5381;
    for (var i = 0; i < texto.length; i++) h = ((h * 33) ^ texto.charCodeAt(i)) >>> 0;
    return h;
  }

  // Uno de los últimos VENTANA_FINAL días antes del examen, fijo para cada id.
  function diaFinal(id, examen) {
    if (!examen) return null;
    return sumar(vispera(examen), -(hash(String(id)) % VENTANA_FINAL));
  }

  // ---------- Intervalo efectivo ----------
  function intervalo(caja, hoy, examen, id) {
    var base = INTERVALOS[caja];
    if (caja === 0) return 0;
    var tope = diaFinal(id == null ? "" : id, examen);
    if (!tope || hoy >= tope) return base; // ya tuvo su repaso final (o no hay examen)
    return Math.max(1, Math.min(base, diferencia(hoy, tope)));
  }

  // ---------- Registros ----------
  // Convierte un registro viejo ({r, n, t}) al formato con caja y fecha de repaso.
  function normalizar(reg) {
    if (!reg) return null;
    if (typeof reg.caja === "number" && reg.vence) return reg;
    var copia = {};
    Object.keys(reg).forEach(function (k) { copia[k] = reg[k]; });
    var dia = diaDe(new Date(reg.t || 0));
    copia.caja = FALLA[reg.r] ? 0 : 1;
    copia.vence = copia.caja ? sumar(dia, 1) : dia;
    copia.visto = reg.visto || dia;
    return copia;
  }

  // o: {id, hoy, examen, verificar, ahora}. Devuelve el registro nuevo (no modifica prev).
  function aplicar(prev, resultado, o) {
    var p = normalizar(prev);
    var caja = p ? p.caja : 0;
    if (FALLA[resultado]) caja = 0;
    else if (SUBE[resultado]) caja = p ? caja + 1 : 2;
    else caja = Math.max(1, caja - 1);
    caja = Math.min(caja, o.verificar ? CAJA_MAX_VERIFICAR : CAJA_MAX);
    var reg = {};
    if (p) Object.keys(p).forEach(function (k) { reg[k] = p[k]; });
    reg.r = resultado;
    reg.n = (p ? p.n || 0 : 0) + 1;
    reg.t = o.ahora;
    reg.caja = caja;
    var dias = intervalo(caja, o.hoy, o.examen, o.id);
    var v = vispera(o.examen);
    if (v && caja > 0 && !SUBE[resultado] && o.hoy < v && o.hoy >= diaFinal(o.id, o.examen)) {
      dias = 1; // dudosa en la recta final: vuelve mañana
    }
    reg.vence = sumar(o.hoy, dias);
    reg.visto = p && p.visto ? p.visto : o.hoy;
    return reg;
  }

  function estado(reg, hoy) {
    var r = normalizar(reg);
    if (!r) return "nuevo";
    if (r.caja === 0) return "fallado";
    if (r.vence <= hoy) return "vencido";
    return "al-dia";
  }

  // ---------- Cuota de nuevos y cola del día ----------
  function cuotaNuevos(restantes, vistosHoy, hoy, examen) {
    if (!restantes) return 0;
    var v = vispera(examen);
    var limite = v ? sumar(v, -VENTANA_FINAL) : null;
    if (limite && hoy > limite) limite = v;
    var dias = limite ? diferencia(hoy, limite) + 1 : 0;
    var porDia = dias >= 1 ? Math.ceil((restantes + vistosHoy) / dias) : NUEVOS_SIN_EXAMEN;
    return Math.max(0, Math.min(restantes, porDia - vistosHoy));
  }

  // Copia barajada de la lista (Fisher–Yates). rnd: función que da [0, 1).
  function barajar(lista, rnd) {
    var a = lista.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1));
      var x = a[i]; a[i] = a[j]; a[j] = x;
    }
    return a;
  }

  // «Barajar»: deja igual lo ya visto y el ítem actual (pos) y baraja lo que falta.
  function barajarResto(cola, pos, rnd) {
    return cola.slice(0, pos + 1).concat(barajar(cola.slice(pos + 1), rnd));
  }

  // Azar de las colas de la app. Las pruebas pueden fijar el orden con window.__ordenFijo = true.
  function azar() {
    return root && root.__ordenFijo ? null : Math.random;
  }

  // items: [{id}] en el orden de los datos; leer(id) → registro guardado o null.
  // Orden: fallados, vencidos y nuevos, en ese orden de grupos. Sin rnd: fallados de los más
  // viejos primero, vencidos de los más atrasados primero y nuevos en el orden de los datos.
  // Con rnd: cada grupo barajado y los nuevos del día elegidos al azar.
  function colaRepaso(items, leer, hoy, examen, rnd) {
    var fallados = [], vencidos = [], nuevos = [], vistosHoy = 0;
    items.forEach(function (it) {
      var r = normalizar(leer(it.id));
      if (!r) { nuevos.push(it.id); return; }
      if (r.visto === hoy) vistosHoy++;
      if (r.caja === 0) fallados.push({ id: it.id, t: r.t || 0 });
      else if (r.vence <= hoy) vencidos.push({ id: it.id, vence: r.vence, caja: r.caja });
    });
    fallados.sort(function (a, b) { return a.t - b.t; });
    vencidos.sort(function (a, b) {
      return a.vence < b.vence ? -1 : a.vence > b.vence ? 1 : a.caja - b.caja;
    });
    var cuota = cuotaNuevos(nuevos.length, vistosHoy, hoy, examen);
    if (rnd) {
      fallados = barajar(fallados, rnd);
      vencidos = barajar(vencidos, rnd);
      nuevos = barajar(nuevos, rnd);
    }
    var tomados = nuevos.slice(0, cuota);
    return {
      ids: fallados.map(function (x) { return x.id; })
        .concat(vencidos.map(function (x) { return x.id; }), tomados),
      fallados: fallados.length,
      vencidos: vencidos.length,
      nuevos: tomados.length,
      nuevosRestantes: nuevos.length
    };
  }

  // Ítems que todavía no vencen, empezando por los que vencen antes («Adelantar repaso»).
  // Con rnd, los que vencen el mismo día salen barajados.
  function adelantar(items, leer, hoy, rnd) {
    var lista = [];
    items.forEach(function (it) {
      var r = normalizar(leer(it.id));
      if (r && r.caja > 0 && r.vence > hoy) lista.push({ id: it.id, vence: r.vence, caja: r.caja });
    });
    if (rnd) lista = barajar(lista, rnd);
    lista.sort(function (a, b) {
      return a.vence < b.vence ? -1 : a.vence > b.vence ? 1 : rnd ? 0 : a.caja - b.caja;
    });
    return lista.map(function (x) { return x.id; });
  }

  // Siguientes n ítems nunca vistos que no estén en «excluir» («Seguir con nuevas»).
  // Con rnd, se eligen al azar entre todos los nunca vistos.
  function masNuevos(items, leer, n, excluir, rnd) {
    var fuera = {};
    (excluir || []).forEach(function (id) { fuera[id] = true; });
    if (rnd) items = barajar(items, rnd);
    var out = [];
    for (var i = 0; i < items.length && out.length < n; i++) {
      var id = items[i].id;
      if (!fuera[id] && !leer(id)) out.push(id);
    }
    return out;
  }

  // Fecha de hoy. Las pruebas pueden fijarla con window.__fechaPrueba = "AAAA-MM-DD".
  function hoy() {
    if (root && typeof root.__fechaPrueba === "string") return root.__fechaPrueba;
    return diaDe(new Date());
  }

  var SRS = {
    INTERVALOS: INTERVALOS,
    VENTANA_FINAL: VENTANA_FINAL,
    diaFinal: diaFinal,
    CAJA_MAX: CAJA_MAX,
    CAJA_MAX_VERIFICAR: CAJA_MAX_VERIFICAR,
    diaDe: diaDe,
    sumar: sumar,
    diferencia: diferencia,
    vispera: vispera,
    intervalo: intervalo,
    normalizar: normalizar,
    aplicar: aplicar,
    estado: estado,
    cuotaNuevos: cuotaNuevos,
    colaRepaso: colaRepaso,
    adelantar: adelantar,
    masNuevos: masNuevos,
    barajar: barajar,
    barajarResto: barajarResto,
    azar: azar,
    hoy: hoy
  };

  if (typeof module !== "undefined" && module.exports) module.exports = SRS;
  else root.SRS = SRS;
})(typeof self !== "undefined" ? self : this);
