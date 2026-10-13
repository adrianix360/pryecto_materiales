// Pruebas de la lógica de «Normas» (js/normas-logica.js) y de los datos de data/normas.json.
// Uso: node --test tests/*.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const SRS = require("../js/srs.js");
const NL = require("../js/normas-logica.js");
const Progreso = require("../js/progreso.js");

const RAIZ = path.join(__dirname, "..");
const { familias, normas } = JSON.parse(fs.readFileSync(path.join(RAIZ, "data/normas.json"), "utf8"));
const porId = Object.fromEntries(normas.map((n) => [n.id, n]));
const EXAMEN = "2026-10-17";
const azar = (semilla) => { let s = semilla >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };

test("datos: normas de la lista de Adrián, con las correcciones acordadas", () => {
  const esperadas = ["C1602", "C1603", "C114", "C109", "C305", "C1437", "C191", "C33", "C136", "C131", "C994", "C227",
    "C1260", "C289", "C586", "D4791", "D5821", "C29", "C127", "C128", "C566", "D75", "C702", "C117", "C40", "C418"];
  for (const id of esperadas) assert.ok(porId[id], "falta " + id);
  assert.equal(normas.length, esperadas.length);
  assert.equal(porId.C386, undefined, "C386 no existe en las fuentes: era C586");
  assert.match(porId.D5821.mide, /fracturadas/);
  assert.match(porId.D4791.mide, /planas/);
});

test("datos: cada norma tiene fuente, pareja existente y su «mide» no regala la respuesta", () => {
  for (const n of normas) {
    assert.ok(n.fuente.length >= 1, n.id);
    assert.ok(n.confunde_con.length >= 1, n.id);
    for (const o of n.confunde_con) assert.ok(porId[o] && o !== n.id, n.id + " → " + o);
    assert.ok(familias.some((f) => f.id === n.familia), n.id);
    const palabras = n.mide.replace(/-/g, " ").split(/\s+/);
    for (const o of normas) assert.ok(!palabras.includes(o.id), n.id + " nombra " + o.id);
  }
});

test("datos: la pareja es recíproca para las parejas clave", () => {
  for (const [a, b] of [["C127", "C128"], ["C117", "C136"], ["C305", "C1437"], ["C227", "C1260"], ["C1602", "C1603"], ["D4791", "D5821"]]) {
    assert.ok(porId[a].confunde_con.includes(b) && porId[b].confunde_con.includes(a), a + "/" + b);
  }
});

test("items: dos por norma, agrupados por familia y con los «escribir» antes que las «inversa»", () => {
  const it = NL.items(normas, familias);
  assert.equal(it.length, normas.length * 2);
  assert.equal(new Set(it.map((x) => x.id)).size, it.length);
  for (const f of familias) {
    const de = it.filter((x) => porId[x.norma].familia === f.id);
    const ultimaE = Math.max(...de.map((x, i) => (x.tipo === "e" ? i : -1)));
    const primeraI = de.findIndex((x) => x.tipo === "i");
    assert.ok(ultimaE < primeraI, f.id);
  }
  assert.equal(it.find((x) => x.id === "n-C994-e").verificar, true);
});

test("parsear: letra elegida, «C128», «ASTM C 128», «d-75»", () => {
  assert.equal(NL.parsear("C", "128"), "C128");
  assert.equal(NL.parsear("D", "75"), "D75");
  assert.equal(NL.parsear("C", "c128"), "C128");
  assert.equal(NL.parsear("C", "ASTM C 128"), "C128");
  assert.equal(NL.parsear("C", "astm d-75"), "D75");
  assert.equal(NL.parsear("C", "  1602 "), "C1602");
  assert.equal(NL.parsear("C", ""), null);
  assert.equal(NL.parsear("C", "abc"), null);
  assert.equal(NL.parsear("X", "5"), "C5");
});

test("evaluarEscribir: acierto, confusión con una norma de la lista y número que no existe", () => {
  assert.deepEqual(NL.evaluarEscribir(porId.C128, "C128", porId), { ok: true, conf: null });
  assert.deepEqual(NL.evaluarEscribir(porId.C128, "C127", porId), { ok: false, conf: "C127" });
  assert.deepEqual(NL.evaluarEscribir(porId.C128, "C999", porId), { ok: false, conf: "otra" });
  assert.deepEqual(NL.evaluarEscribir(porId.C128, "D128", porId), { ok: false, conf: "otra" }); // letra equivocada
  assert.deepEqual(NL.evaluarEscribir(porId.C128, null, porId), { ok: false, conf: null }); // «No sé»
});

test("opcionesInversa: 4 opciones, la correcta, sin textos repetidos y con la pareja", () => {
  for (const n of normas) {
    for (let semilla = 1; semilla <= 5; semilla++) {
      const o = NL.opcionesInversa(n, normas, porId, azar(semilla));
      assert.equal(o.length, 4, n.id);
      assert.equal(o.filter((x) => x.norma === n.id).length, 1, n.id);
      assert.equal(new Set(o.map((x) => x.texto)).size, 4, n.id);
      assert.equal(new Set(o.map((x) => x.norma)).size, 4, n.id);
      assert.ok(o.some((x) => n.confunde_con.includes(x.norma)), n.id + ": ninguna pareja entre las opciones");
    }
  }
});

test("opcionesInversa: el orden cambia con el azar", () => {
  const ordenes = new Set();
  for (let s = 1; s <= 30; s++) ordenes.add(NL.opcionesInversa(porId.C127, normas, porId, azar(s)).map((x) => x.norma).join());
  assert.ok(ordenes.size > 3);
});

const base = { hoy: "2026-10-12", examen: EXAMEN, ahora: 1000 };

test("registrar: acierto sube de caja, cuenta el día y no guarda confusiones", () => {
  const r = NL.registrar(null, "e", true, { ...base, id: "n-C127-e" });
  assert.equal(r.r, "bien");
  assert.equal(r.caja, 2);
  assert.equal(r.bien, 1);
  assert.deepEqual(r.dias, ["2026-10-12"]);
  assert.equal(r.conf, undefined);
});

test("registrar: fallo vuelve hoy, anota con cuál se confundió y acumula", () => {
  let r = NL.registrar(null, "e", false, { ...base, id: "n-C127-e", conf: "C128" });
  assert.equal(r.caja, 0);
  assert.equal(r.vence, "2026-10-12");
  assert.deepEqual(r.conf, { C128: 1 });
  assert.deepEqual(r.dias, []);
  r = NL.registrar(r, "e", false, { ...base, id: "n-C127-e", conf: "C128", ahora: 2000 });
  assert.deepEqual(r.conf, { C128: 2 });
  r = NL.registrar(r, "e", true, { ...base, id: "n-C127-e", ahora: 3000 });
  assert.deepEqual(r.conf, { C128: 2 }, "acertar no borra el historial de confusiones");
  assert.equal(r.bien, 1);
});

test("registrar: «inversa» no lleva días; no modifica el registro anterior", () => {
  const prev = NL.registrar(null, "i", true, { ...base, id: "n-C127-i" });
  const copia = JSON.parse(JSON.stringify(prev));
  const r = NL.registrar(prev, "i", false, { ...base, id: "n-C127-i", conf: "C128" });
  assert.equal(r.dias, undefined);
  assert.deepEqual(prev, copia);
});

test("registrar: ítem con «verificar» no pasa de la caja 2", () => {
  let r = null;
  for (let i = 0; i < 6; i++) r = NL.registrar(r, "e", true, { ...base, id: "n-C994-e", verificar: true, hoy: SRS.sumar("2026-10-01", i) });
  assert.equal(r.caja, 2);
});

test("dominada: bien en 2 días distintos y la última vez bien", () => {
  let r = NL.registrar(null, "e", true, { ...base, id: "x" });
  assert.equal(NL.dominada(r), false);
  r = NL.registrar(r, "e", true, { ...base, id: "x" }); // mismo día: no cuenta otra vez
  assert.equal(NL.dominada(r), false);
  r = NL.registrar(r, "e", true, { ...base, id: "x", hoy: "2026-10-13" });
  assert.equal(NL.dominada(r), true);
  r = NL.registrar(r, "e", false, { ...base, id: "x", hoy: "2026-10-14" });
  assert.equal(NL.dominada(r), false, "si falla deja de estar dominada");
  assert.equal(NL.dominada(null), false);
});

test("estadoNorma: nueva, riesgo, camino y dominada", () => {
  assert.equal(NL.estadoNorma(null, null), "nueva");
  const mal = NL.registrar(null, "e", false, { ...base, id: "x" });
  assert.equal(NL.estadoNorma(mal, null), "riesgo");
  const bien = NL.registrar(null, "e", true, { ...base, id: "x" });
  assert.equal(NL.estadoNorma(bien, null), "camino");
  const dos = NL.registrar(bien, "e", true, { ...base, id: "x", hoy: "2026-10-13" });
  assert.equal(NL.estadoNorma(dos, null), "dominada");
});

test("parejas: suma las confusiones de las dos fichas y de los dos sentidos; ignora «otra»", () => {
  const regs = {
    "n-C127-e": { conf: { C128: 2, otra: 5 } },
    "n-C127-i": { conf: { C128: 1 } },
    "n-C128-e": { conf: { C127: 1 } },
    "n-C117-e": { conf: { C136: 1 } }
  };
  const p = NL.parejas(normas, (k) => regs[k] || null);
  assert.deepEqual(p, [{ a: "C127", b: "C128", n: 4 }, { a: "C117", b: "C136", n: 1 }]);
  assert.deepEqual(NL.parejas(normas, () => null), []);
});

test("itemsDe: fichas de esas normas, «escribir» primero, en el orden pedido", () => {
  const todos = NL.items(normas, familias);
  const ids = NL.itemsDe(todos, ["C128", "C127"]).map((x) => x.id);
  assert.deepEqual(ids, ["n-C128-e", "n-C127-e", "n-C128-i", "n-C127-i"]);
});

test("repaso con SRS: todas las fichas se ven antes del examen", () => {
  const todos = NL.items(normas, familias);
  const guardado = {};
  const leer = (k) => guardado[k] || null;
  const vistas = new Set();
  const azarSim = azar(7);
  for (let d = 0; d <= 4; d++) {
    const hoy = SRS.sumar("2026-10-12", d);
    const cola = SRS.colaRepaso(todos, leer, hoy, EXAMEN).ids;
    for (const id of cola) {
      vistas.add(id);
      const it = todos.find((x) => x.id === id);
      guardado[id] = NL.registrar(leer(id), it.tipo, azarSim() < 0.7, { id, hoy, examen: EXAMEN, verificar: it.verificar, ahora: d * 1e6 });
    }
  }
  assert.equal(vistas.size, todos.length, "faltaron fichas por ver");
});

test("progreso: las normas se exportan, validan y combinan; un archivo viejo sin normas vale", () => {
  const regN = (t) => ({ r: "bien", n: 1, t, caja: 2, vence: "2026-10-14", visto: "2026-10-12" });
  const estado = { ...Progreso.vacio(), normas: { "n-C127-e": regN(1) } };
  const archivo = JSON.parse(JSON.stringify(Progreso.exportar(estado, "2026-10-12.1", Date.UTC(2026, 9, 12, 12))));
  const v = Progreso.validar(archivo);
  assert.equal(v.ok, true);
  assert.deepEqual(v.progreso.normas, estado.normas);
  assert.equal(v.resumen.normas, 1);
  delete archivo.progreso.normas; // exportado antes de existir «Normas»
  assert.deepEqual(Progreso.validar(archivo).progreso.normas, {});
  archivo.progreso.normas = { x: { n: 1 } };
  assert.match(Progreso.validar(archivo).error, /normas/);
  const a = { ...Progreso.vacio(), normas: { "n-C127-e": regN(1), "n-C128-e": regN(5) } };
  const b = { ...Progreso.vacio(), normas: { "n-C127-e": regN(9) } };
  const c = Progreso.combinar(a, b);
  assert.equal(c.normas["n-C127-e"].t, 9);
  assert.equal(c.normas["n-C128-e"].t, 5);
});
