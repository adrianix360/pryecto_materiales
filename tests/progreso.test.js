// Pruebas del núcleo de Progreso (js/progreso.js). Uso: node --test tests/progreso.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const Progreso = require("../js/progreso.js");

const T = [
  { id: "t1", tema: 1, subtema: "1A" },
  { id: "t2", tema: 1, subtema: "1A" },
  { id: "t3", tema: 2, subtema: "2A" },
  { id: "t4", tema: 2, subtema: "2B" },
];
const P = [
  { id: "p1", tema: 1, subtema: "1A" },
  { id: "p2", tema: 2, subtema: "2A" },
  { id: "p3", tema: 2, subtema: "2A" },
  { id: "p4", tema: 3, subtema: "3C" },
];
const reg = (r, n, t, extra = {}) => ({ r, n, t, caja: 1, vence: "2026-10-10", visto: "2026-10-09", ...extra });

test("dominio: % de ítems cuya última calificación fue «la sabía» o «bien»", () => {
  const rt = { t1: reg("sabia", 1, 1), t2: reg("dudosa", 2, 2), t3: reg("no", 1, 3) };
  const rp = { p1: reg("bien", 3, 4, { bien: 2 }), p2: reg("mal", 2, 5, { bien: 1 }), p3: reg("parcial", 1, 6, { bien: 0 }) };
  const d = Progreso.dominio(T, P, (id) => rt[id] || null, (id) => rp[id] || null);
  assert.deepEqual(d.global, { total: 8, vistos: 6, sabidos: 2, intentos: 6, bien: 3, dominio: 25, aciertos: 50 });
  const s = Object.fromEntries(d.subtemas.map((x) => [x.subtema, x]));
  assert.equal(s["1A"].dominio, 67); // t1 y p1 de 3
  assert.equal(s["1A"].aciertos, 67); // 2 de 3 intentos
  assert.equal(s["2A"].dominio, 0);
  assert.equal(s["2A"].aciertos, 33);
  assert.equal(s["2B"].vistos, 0);
  assert.equal(s["3C"].aciertos, null, "sin intentos no hay porcentaje de aciertos");
  assert.deepEqual(d.temas.map((t) => [t.tema, t.total, t.subtemas.length]), [[1, 3, 1], [2, 4, 2], [3, 1, 1]]);
});

test("débiles: menor dominio primero; empate, menos aciertos; lo no visto va aparte", () => {
  const subs = [
    { subtema: "1A", vistos: 3, dominio: 60, aciertos: 80 },
    { subtema: "2A", vistos: 2, dominio: 20, aciertos: 50 },
    { subtema: "2B", vistos: 0, dominio: 0, aciertos: null },
    { subtema: "3A", vistos: 4, dominio: 20, aciertos: 30 },
    { subtema: "3B", vistos: 1, dominio: 20, aciertos: null },
    { subtema: "3C", vistos: 5, dominio: 100, aciertos: 100 },
  ];
  assert.deepEqual(Progreso.debiles(subs).map((s) => s.subtema), ["3A", "2A", "3B"]);
  assert.deepEqual(Progreso.debiles(subs, 10).map((s) => s.subtema), ["3A", "2A", "3B", "1A"], "lo dominado al 100 % no sale");
  assert.deepEqual(Progreso.sinVer(subs).map((s) => s.subtema), ["2B"]);
});

test("racha: días seguidos con actividad; si hoy no hay, cuenta hasta ayer", () => {
  const d = {
    "2026-10-05": { seg: 60, items: 2 },
    "2026-10-07": { seg: 600, items: 10 },
    "2026-10-08": { seg: 900, items: 20 },
    "2026-10-09": { seg: 30, items: 1 },
  };
  assert.deepEqual(Progreso.racha(d, "2026-10-09"), { dias: 3, incluyeHoy: true });
  assert.deepEqual(Progreso.racha(d, "2026-10-10"), { dias: 3, incluyeHoy: false }, "hoy sin actividad: sigue la de ayer");
  assert.deepEqual(Progreso.racha(d, "2026-10-11"), { dias: 0, incluyeHoy: false }, "se cortó ayer");
  assert.deepEqual(Progreso.racha({ "2026-10-09": { seg: 10, items: 0 } }, "2026-10-09"), { dias: 0, incluyeHoy: false });
  assert.deepEqual(Progreso.racha({}, "2026-10-09"), { dias: 0, incluyeHoy: false });
});

test("tiempo por día: los últimos 7 días, en minutos, terminando hoy", () => {
  const d = { "2026-10-09": { seg: 2430, items: 40 }, "2026-10-04": { seg: 89, items: 3 } };
  const r = Progreso.porDia(d, "2026-10-09");
  assert.equal(r.length, 7);
  assert.deepEqual(r[0], { dia: "2026-10-03", min: 0, items: 0 });
  assert.deepEqual(r[1], { dia: "2026-10-04", min: 1, items: 3 });
  assert.deepEqual(r[6], { dia: "2026-10-09", min: 41, items: 40 });
});

test("exportar y validar: ida y vuelta", () => {
  const estado = { ...Progreso.vacio(), tarjetas: { t1: reg("sabia", 1, 1) }, diario: { "2026-10-09": { seg: 1, items: 1 } } };
  const archivo = JSON.parse(JSON.stringify(Progreso.exportar(estado, "2026-10-09.4", Date.UTC(2026, 9, 9, 12))));
  assert.equal(archivo.app, "pryecto_materiales");
  assert.equal(archivo.exportado, "2026-10-09T12:00:00.000Z");
  const v = Progreso.validar(archivo);
  assert.equal(v.ok, true);
  assert.deepEqual(v.progreso, estado);
  assert.deepEqual(v.resumen, { tarjetas: 1, preguntas: 0, normas: 0, dias: 1, simulacros: 0, exportado: "2026-10-09T12:00:00.000Z" });
});

test("validar rechaza archivos ajenos o dañados", () => {
  assert.equal(Progreso.validar(null).ok, false);
  assert.match(Progreso.validar({ app: "otra" }).error, /no es un progreso de esta app/);
  assert.match(Progreso.validar({ app: "pryecto_materiales", formato: 99, progreso: {} }).error, /formato/);
  assert.match(Progreso.validar({ app: "pryecto_materiales", formato: 1 }).error, /falta el progreso/);
  assert.match(Progreso.validar({ app: "pryecto_materiales", formato: 1, progreso: { tarjetas: { x: { n: 1 } } } }).error, /dañados/);
  assert.match(Progreso.validar({ app: "pryecto_materiales", formato: 1, progreso: { historial: {} } }).error, /historial/);
});

test("combinar: por ítem el registro más reciente; por día, el mayor; nada se pierde", () => {
  const actual = {
    ...Progreso.vacio(),
    tarjetas: { a: reg("sabia", 3, 100), b: reg("no", 1, 50) },
    preguntas: { p: reg("bien", 1, 10, { bien: 1 }) },
    diario: { "2026-10-08": { seg: 600, items: 10 }, "2026-10-09": { seg: 100, items: 5 } },
    prefs: { meta: { unidad: "minutos", valor: 40 } },
    historial: [{ fecha: "2026-10-09", duracion: 25, nota: 70, usado: 1 }],
  };
  const nuevo = {
    ...Progreso.vacio(),
    tarjetas: { a: reg("no", 1, 90), b: reg("sabia", 2, 80), c: reg("dudosa", 1, 70) },
    diario: { "2026-10-09": { seg: 900, items: 3 }, "2026-10-07": { seg: 60, items: 1 } },
    prefs: { meta: { unidad: "items", valor: 80 }, modoEstudiar: "tema" },
    historial: [{ fecha: "2026-10-09", duracion: 25, nota: 70, usado: 1 }, { fecha: "2026-10-08", duracion: 40, nota: 55, usado: 2 }],
  };
  const r = Progreso.combinar(actual, nuevo);
  assert.equal(r.tarjetas.a.r, "sabia", "a: el actual es más reciente");
  assert.equal(r.tarjetas.b.r, "sabia", "b: el importado es más reciente");
  assert.equal(r.tarjetas.c.r, "dudosa", "c: solo estaba en el importado");
  assert.equal(r.preguntas.p.r, "bien");
  assert.deepEqual(r.diario["2026-10-09"], { seg: 900, items: 5 });
  assert.deepEqual(Object.keys(r.diario).sort(), ["2026-10-07", "2026-10-08", "2026-10-09"]);
  assert.deepEqual(r.prefs.meta, { unidad: "minutos", valor: 40 }, "los ajustes de este teléfono mandan");
  assert.equal(r.prefs.modoEstudiar, "tema");
  assert.equal(r.historial.length, 2, "el simulacro repetido no se duplica");
  assert.equal(r.historial[0].fecha, "2026-10-09");
});
