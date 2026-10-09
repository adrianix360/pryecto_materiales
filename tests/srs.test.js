// Pruebas del algoritmo de repetición espaciada (js/srs.js) con fechas simuladas.
// Uso: node --test tests/
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const SRS = require("../js/srs.js");

const RAIZ = path.join(__dirname, "..");
const EXAMEN = JSON.parse(fs.readFileSync(path.join(RAIZ, "data/indice.json"), "utf8")).examen;
const VISPERA = "2026-10-16";
const leerJSON = (rel) => JSON.parse(fs.readFileSync(path.join(RAIZ, rel), "utf8"));

function itemsReales() {
  const idx = leerJSON("data/indice.json");
  const tarjetas = [], preguntas = [];
  for (const t of idx.temas) {
    tarjetas.push(...leerJSON(t.tarjetas).tarjetas);
    preguntas.push(...leerJSON(t.preguntas).preguntas);
  }
  return { tarjetas, preguntas };
}

// Generador pseudoaleatorio fijo (las pruebas siempre dan lo mismo).
function azar(semilla) {
  let s = semilla >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

test("la fecha del examen sale de data/indice.json", () => {
  assert.equal(EXAMEN, "2026-10-17");
  assert.equal(SRS.vispera(EXAMEN), VISPERA);
});

test("aritmética de fechas", () => {
  assert.equal(SRS.sumar("2026-10-30", 3), "2026-11-02");
  assert.equal(SRS.sumar("2026-01-01", -1), "2025-12-31");
  assert.equal(SRS.diferencia("2026-10-09", "2026-10-17"), 8);
  assert.equal(SRS.diaDe(new Date(2026, 9, 9, 23, 59)), "2026-10-09");
});

test("intervalos base sin examen", () => {
  assert.deepEqual([0, 1, 2, 3, 4].map((c) => SRS.intervalo(c, "2026-10-09", null, "x")), [0, 1, 2, 4, 7]);
});

test("día de repaso final: uno de los 3 días antes del examen, repartidos en tercios", () => {
  const { tarjetas, preguntas } = itemsReales();
  const todos = [...tarjetas, ...preguntas];
  const conteo = {};
  for (const it of todos) {
    const d = SRS.diaFinal(it.id, EXAMEN);
    conteo[d] = (conteo[d] || 0) + 1;
    assert.equal(d, SRS.diaFinal(it.id, EXAMEN), "siempre el mismo día para el mismo id");
  }
  assert.deepEqual(Object.keys(conteo).sort(), ["2026-10-14", "2026-10-15", "2026-10-16"]);
  for (const n of Object.values(conteo)) assert.ok(n > todos.length * 0.25, JSON.stringify(conteo));
  assert.equal(SRS.diaFinal("x", null), null);
});

test("compresión: antes de su día final, ningún intervalo lo salta", () => {
  for (const id of ["t1-1A-01", "p3-3C-x05", "g-x", "abc"]) {
    const tope = SRS.diaFinal(id, EXAMEN);
    for (let d = 0; SRS.sumar("2026-10-09", d) < tope; d++) {
      const hoy = SRS.sumar("2026-10-09", d);
      for (let c = 1; c <= 4; c++) {
        const vence = SRS.sumar(hoy, SRS.intervalo(c, hoy, EXAMEN, id));
        assert.ok(vence <= tope, `${id} ${hoy} caja ${c} vence ${vence} > ${tope}`);
        assert.ok(vence > hoy);
      }
    }
    // el 9/10 la caja 4 (7 días) vence justo en su día final
    assert.equal(SRS.sumar("2026-10-09", SRS.intervalo(4, "2026-10-09", EXAMEN, id)), tope);
  }
});

test("compresión: desde su día final vuelven los intervalos normales", () => {
  const id = "t1-1A-01";
  const tope = SRS.diaFinal(id, EXAMEN);
  assert.deepEqual([0, 1, 2, 3, 4].map((c) => SRS.intervalo(c, tope, EXAMEN, id)), [0, 1, 2, 4, 7]);
  assert.deepEqual([1, 2, 3, 4].map((c) => SRS.intervalo(c, "2026-10-18", EXAMEN, id)), [1, 2, 4, 7]);
});

test("calificaciones: sube, baja y falla", () => {
  const o = { id: "x", hoy: "2026-10-09", examen: null, ahora: 1 };
  let r = SRS.aplicar(null, "sabia", o);
  assert.equal(r.caja, 2, "nueva y la sabía: entra a la caja 2");
  assert.equal(r.vence, "2026-10-11");
  assert.equal(r.visto, "2026-10-09");
  assert.equal(r.n, 1);
  for (let i = 0; i < 6; i++) r = SRS.aplicar(r, "bien", o);
  assert.equal(r.caja, SRS.CAJA_MAX, "no pasa de la caja máxima");
  r = SRS.aplicar(r, "dudosa", o);
  assert.equal(r.caja, 3);
  r = SRS.aplicar({ ...r, caja: 1 }, "parcial", o);
  assert.equal(r.caja, 1, "dudosa no baja de la caja 1");
  r = SRS.aplicar(r, "no", o);
  assert.equal(r.caja, 0);
  assert.equal(r.vence, "2026-10-09", "lo fallado vuelve hoy");
  assert.equal(r.visto, "2026-10-09", "conserva la fecha en que se vio por primera vez");
  assert.equal(SRS.aplicar(null, "dudosa", o).caja, 1);
  assert.equal(SRS.aplicar(null, "mal", o).caja, 0);
});

test("en la recta final, lo dudoso vuelve al día siguiente", () => {
  const id = ["a", "b", "c", "d", "e", "f"].find((x) => SRS.diaFinal(x, EXAMEN) < VISPERA);
  const tope = SRS.diaFinal(id, EXAMEN);
  const prev = { r: "sabia", n: 3, t: 1, caja: 3, vence: tope, visto: "2026-10-09" };
  const dudosa = SRS.aplicar(prev, "dudosa", { id, hoy: tope, examen: EXAMEN, ahora: 2 });
  assert.equal(dudosa.caja, 2);
  assert.equal(dudosa.vence, SRS.sumar(tope, 1));
  const sabia = SRS.aplicar(prev, "sabia", { id, hoy: tope, examen: EXAMEN, ahora: 2 });
  assert.ok(sabia.vence > EXAMEN, "lo que sabía ya no vuelve antes del examen");
  const enVispera = SRS.aplicar(prev, "dudosa", { id, hoy: VISPERA, examen: EXAMEN, ahora: 3 });
  assert.equal(enVispera.vence, SRS.sumar(VISPERA, 2), "en la víspera ya no hay mañana antes del examen");
});

test("ítems con «verificar» no pasan de la caja 2", () => {
  let r = null;
  for (let i = 0; i < 6; i++) r = SRS.aplicar(r, "sabia", { hoy: "2026-10-01", examen: null, ahora: i, verificar: true });
  assert.equal(r.caja, SRS.CAJA_MAX_VERIFICAR);
  assert.equal(r.vence, "2026-10-03");
  r = SRS.aplicar(null, "sabia", { hoy: "2026-10-01", examen: null, ahora: 0, verificar: true });
  assert.equal(r.caja, 2);
});

test("convierte el progreso viejo sin perderlo", () => {
  const t = new Date(2026, 9, 8, 10, 0).getTime();
  const sabia = SRS.normalizar({ r: "sabia", n: 2, t });
  assert.deepEqual([sabia.caja, sabia.vence, sabia.visto, sabia.n], [1, "2026-10-09", "2026-10-08", 2]);
  const no = SRS.normalizar({ r: "no", n: 1, t });
  assert.deepEqual([no.caja, no.vence], [0, "2026-10-08"]);
  const mal = SRS.normalizar({ r: "mal", n: 1, bien: 0, resp: "a", t });
  assert.equal(mal.caja, 0);
  assert.equal(mal.resp, "a", "conserva los demás campos");
  assert.equal(SRS.normalizar(null), null);
});

test("cuota de nuevos: se reparte hasta antes de la ventana final (13/10)", () => {
  assert.equal(SRS.cuotaNuevos(147, 0, "2026-10-09", EXAMEN), 30); // 147 / 5 días (9 al 13)
  assert.equal(SRS.cuotaNuevos(183, 0, "2026-10-09", EXAMEN), 37);
  assert.equal(SRS.cuotaNuevos(117, 30, "2026-10-09", EXAMEN), 0, "si ya vio la cuota de hoy, no da más");
  assert.equal(SRS.cuotaNuevos(20, 0, "2026-10-13", EXAMEN), 20, "el 13 da todos los que faltan");
  assert.equal(SRS.cuotaNuevos(30, 0, "2026-10-14", EXAMEN), 10, "ya en la ventana, se reparten hasta la víspera");
  assert.equal(SRS.cuotaNuevos(50, 0, VISPERA, EXAMEN), 50, "en la víspera da todos los que faltan");
  assert.equal(SRS.cuotaNuevos(50, 0, "2026-10-17", EXAMEN), 20, "después de la víspera, 20 por día");
  assert.equal(SRS.cuotaNuevos(0, 0, "2026-10-09", EXAMEN), 0);
});

test("cola del día: fallados, luego vencidos (más atrasados primero), luego nuevos", () => {
  const items = ["a", "b", "c", "d", "e", "f"].map((id) => ({ id }));
  const regs = {
    a: { r: "sabia", n: 1, t: 5, caja: 2, vence: "2026-10-09", visto: "2026-10-05" },
    b: { r: "no", n: 1, t: 9, caja: 0, vence: "2026-10-08", visto: "2026-10-08" },
    c: { r: "sabia", n: 1, t: 3, caja: 1, vence: "2026-10-07", visto: "2026-10-06" },
    d: { r: "sabia", n: 1, t: 3, caja: 3, vence: "2026-10-12", visto: "2026-10-06" },
  };
  const cola = SRS.colaRepaso(items, (id) => regs[id] || null, "2026-10-09", EXAMEN);
  // 2 nuevos entre 5 días (9 al 13) → 1 hoy
  assert.deepEqual(cola.ids, ["b", "c", "a", "e"]);
  assert.deepEqual([cola.fallados, cola.vencidos, cola.nuevos, cola.nuevosRestantes], [1, 2, 1, 2]);
  assert.deepEqual(SRS.adelantar(items, (id) => regs[id] || null, "2026-10-09"), ["d"]);
  assert.deepEqual(SRS.masNuevos(items, (id) => regs[id] || null, 1, ["e"]), ["f"]);
});

// Simula estudiar con la cola del día. dias: lista de fechas en que se estudia.
function simular(items, dias, semilla) {
  const regs = {};
  const repasos = {}; // id -> fechas en que salió
  const verif = new Set(items.filter((x) => x.verificar).map((x) => x.id));
  const rnd = azar(semilla);
  const carga = {};
  let reloj = 0;
  for (const hoy of dias) {
    const cola = SRS.colaRepaso(items, (id) => regs[id] || null, hoy, EXAMEN).ids.slice();
    carga[hoy] = 0;
    while (cola.length) {
      const id = cola.shift();
      carga[hoy]++;
      (repasos[id] = repasos[id] || []).push(hoy);
      const x = rnd();
      const reintento = regs[id] && regs[id].caja === 0 && regs[id].vence === hoy;
      const res = reintento ? "sabia" : x < 0.12 ? "no" : x < 0.32 ? "dudosa" : "sabia";
      regs[id] = SRS.aplicar(regs[id], res, { id, hoy, examen: EXAMEN, verificar: verif.has(id), ahora: ++reloj });
      if (res === "no") cola.push(id); // en la sesión, lo fallado vuelve a salir
      assert.ok(regs[id].caja <= (verif.has(id) ? 2 : 4));
    }
    for (const [id, r] of Object.entries(regs)) {
      assert.ok(r.caja > 0, `${hoy}: ${id} quedó fallado al cerrar el día`);
      const tope = SRS.diaFinal(id, EXAMEN);
      if (hoy < tope) assert.ok(r.vence <= tope, `${hoy}: ${id} vence ${r.vence}, después de su día final ${tope}`);
    }
  }
  return { regs, repasos, carga };
}

const DIAS = Array.from({ length: 8 }, (_, i) => SRS.sumar("2026-10-09", i)); // 9 al 16

for (const tipo of ["tarjetas", "preguntas"]) {
  test(`simulación 9–16 oct (${tipo}): todo se repasa en los últimos 3 días`, () => {
    const items = itemsReales()[tipo];
    const { regs, repasos, carga } = simular(items, DIAS, 604);
    for (const it of items) {
      assert.ok(regs[it.id], `${it.id} nunca salió`);
      const finales = repasos[it.id].filter((d) => d >= "2026-10-14" && d <= VISPERA);
      assert.ok(finales.length >= 1, `${it.id} no se repasó del 14 al 16 (${repasos[it.id]})`);
    }
    // carga diaria: nunca más del 80 % del total en un día (incluye reintentos de lo fallado)
    for (const [dia, n] of Object.entries(carga)) {
      assert.ok(n <= items.length * 0.8, `${dia}: ${n} repasos de ${items.length}`);
    }
    console.log(`  carga diaria ${tipo}:`, JSON.stringify(carga));
  });

  test(`simulación con días saltados (${tipo}): igual se ve todo`, () => {
    const items = itemsReales()[tipo];
    const dias = DIAS.filter((d) => d !== "2026-10-11" && d !== "2026-10-12" && d !== "2026-10-14");
    const { regs, repasos } = simular(items, dias, 17);
    for (const it of items) {
      assert.ok(regs[it.id], `${it.id} nunca salió`);
      assert.ok(repasos[it.id].some((d) => d >= "2026-10-15"), `${it.id} no tuvo repaso final`);
    }
  });

  test(`ítems con «verificar» siguen saliendo (${tipo})`, () => {
    const items = itemsReales()[tipo];
    const conVerificar = items.filter((x) => x.verificar);
    assert.ok(conVerificar.length > 0);
    const { regs, repasos } = simular(items, DIAS, 99);
    for (const it of conVerificar) {
      assert.ok(regs[it.id].caja <= 2);
      const r = repasos[it.id];
      for (let i = 1; i < r.length; i++) {
        assert.ok(SRS.diferencia(r[i - 1], r[i]) <= 2, `${it.id}: ${r[i - 1]} → ${r[i]}`);
      }
    }
  });
}
