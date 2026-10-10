// Pruebas del núcleo del Simulacro (js/examen.js): puntaje, deduplicación, estructura
// y temporizador con reloj simulado. Uso: node --test tests/examen.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const Examen = require("../js/examen.js");

const RAIZ = path.join(__dirname, "..");
const leer = (rel) => JSON.parse(fs.readFileSync(path.join(RAIZ, rel), "utf8"));
const PREGUNTAS = leer("data/indice.json").temas.flatMap((t) => leer(t.preguntas).preguntas);
const POR_ID = Object.fromEntries(PREGUNTAS.map((p) => [p.id, p]));
const MIN = 60000;

const vf = (correcta, extra = {}) => ({
  id: "vf", tipo: "verdadero_falso", correcta,
  opciones: [{ id: "a", texto: "Verdadero" }, { id: "b", texto: "Falso" }], ...extra,
});
const su = { id: "su", tipo: "seleccion_unica", correcta: "c", opciones: [] };
const rc = (n) => ({ id: "rc", tipo: "respuesta_corta", puntos_clave: Array.from({ length: n }, (_, i) => "p" + i) });

// ---------- Puntaje ----------
test("selección única: 1 punto si acierta", () => {
  assert.deepEqual(Examen.puntaje(su, { op: "c" }), { obtenido: 1, maximo: 1, completo: true });
  assert.equal(Examen.puntaje(su, { op: "a" }).obtenido, 0);
  assert.equal(Examen.puntaje(su, undefined).obtenido, 0, "sin responder");
});

test("F/V verdadero: 2 puntos si lo marca V, 0 si lo marca F", () => {
  const p = vf("a");
  assert.equal(Examen.puntaje(p, { op: "a" }).obtenido, 2);
  assert.equal(Examen.puntaje(p, { op: "b", justif: "porque sí" }, { justifOk: true }).obtenido, 0);
  assert.equal(Examen.necesitaAutoeval(p, { op: "a" }), false);
});

test("F/V falso: 1 por marcar F y 1 por la justificación", () => {
  const p = vf("b", { justificacion_oficial: "Es al revés" });
  assert.equal(Examen.puntaje(p, { op: "b", justif: "x" }, { justifOk: true }).obtenido, 2);
  assert.equal(Examen.puntaje(p, { op: "b", justif: "x" }, { justifOk: false }).obtenido, 1);
  assert.equal(Examen.puntaje(p, { op: "b", justif: "  " }, { justifOk: true }).obtenido, 1, "justificación vacía no suma");
  assert.equal(Examen.puntaje(p, { op: "a" }).obtenido, 0, "marcarlo V da 0");
  assert.equal(Examen.necesitaAutoeval(p, { op: "b", justif: "x" }), true);
  assert.equal(Examen.necesitaAutoeval(p, { op: "b", justif: "" }), false);
  assert.equal(Examen.claveJustificacion(p), "Es al revés");
  assert.equal(Examen.claveJustificacion(vf("b", { explicacion: "Expl." })), "Expl.", "sin justificación oficial usa la explicación");
});

test("respuesta corta: 2 × puntos clave cubiertos / total, redondeado a 0,5", () => {
  const t = { texto: "algo" };
  assert.equal(Examen.puntaje(rc(2), t, { marcados: [0, 1] }).obtenido, 2);
  assert.equal(Examen.puntaje(rc(2), t, { marcados: [1] }).obtenido, 1);
  assert.equal(Examen.puntaje(rc(3), t, { marcados: [0] }).obtenido, 0.5);   // 0,67 → 0,5
  assert.equal(Examen.puntaje(rc(3), t, { marcados: [0, 2] }).obtenido, 1.5); // 1,33 → 1,5
  assert.equal(Examen.puntaje(rc(4), t, { marcados: [0, 1, 2] }).obtenido, 1.5);
  assert.equal(Examen.puntaje(rc(1), t, { marcados: [0] }).obtenido, 2);
  assert.equal(Examen.puntaje(rc(2), { texto: "" }, { marcados: [0, 1] }).obtenido, 0, "en blanco no suma");
  assert.equal(Examen.necesitaAutoeval(rc(2), { texto: " " }), false);
});

test("las preguntas reales F/V se reconocen como verdaderas o falsas", () => {
  const vfs = PREGUNTAS.filter((p) => p.tipo === "verdadero_falso");
  const falsas = vfs.filter((p) => !Examen.esVerdadero(p));
  assert.equal(vfs.length, 46);
  assert.equal(falsas.length, 35); // p3-3C-x17 pasó a Verdadero en la auditoría
  assert.ok(falsas.every((p) => Examen.claveJustificacion(p)), "toda falsa tiene contra qué autoevaluar");
});

// ---------- Deduplicación ----------
test("normaliza tildes, mayúsculas, puntuación y «(N puntos)»", () => {
  assert.equal(Examen.normalizar("¿Qué es el ÁRIDO? (2 puntos)"), "que es el arido");
});

test("deduplica por enunciado y deja la de clave oficial más reciente", () => {
  const unicas = Examen.deduplicar(PREGUNTAS);
  const claves = unicas.map(Examen.claveDedup);
  assert.equal(new Set(claves).size, claves.length, "no quedan claves repetidas");
  assert.equal(PREGUNTAS.length - unicas.length, 4, "hay 4 pares repetidos en el banco");
  // las 5 de «Normativa» (misma frase, distinta foto) se conservan
  assert.equal(unicas.filter((p) => /^p3-3E-x0[1-5]$/.test(p.id)).length, 5);
  const a = { id: "a", enunciado: "Igual", clave: "documental", origen: "teoria" };
  const b = { id: "b", enunciado: "igual.", clave: "oficial", origen: "examen", examen: { periodo: "I-2020" } };
  const c = { id: "c", enunciado: "IGUAL", clave: "oficial", origen: "examen", examen: { periodo: "I-2025" } };
  assert.deepEqual(Examen.deduplicar([a, b, c]).map((p) => p.id), ["c"]);
});

// ---------- Estructura ----------
for (const [dur, est] of Object.entries(Examen.ESTRUCTURA)) {
  test(`examen de ${dur} min con los 3 temas: estructura completa y sin repetidos`, () => {
    const { ids, faltan } = Examen.armar(PREGUNTAS, { duracion: +dur, temas: [1, 2, 3] }, 42);
    assert.deepEqual(faltan, {});
    const tipos = ids.map((id) => POR_ID[id].tipo);
    const esperado = Examen.SECCIONES.flatMap((t) => Array(est[t]).fill(t));
    assert.deepEqual(tipos, esperado, "en orden: selección única, F/V, respuesta corta");
    assert.equal(new Set(ids).size, ids.length);
    const claves = ids.map((id) => Examen.claveDedup(POR_ID[id]));
    assert.equal(new Set(claves).size, claves.length, "sin enunciados repetidos");
    assert.ok(ids.some((id) => POR_ID[id].origen === "examen") && ids.some((id) => POR_ID[id].origen === "teoria"),
      "mezcla preguntas de examen y de teoría");
  });
}

test("los 25 min valen 40 puntos, como el I examen de I-2025", () => {
  const e = Examen.nuevo(PREGUNTAS, { duracion: 25, temas: [1, 2, 3] }, 0, 7);
  assert.equal(Examen.resultado(POR_ID, e).maximo, 40);
});

test("la misma semilla da el mismo examen; otra semilla, otro", () => {
  const o = { duracion: 25, temas: [1, 2, 3] };
  assert.deepEqual(Examen.armar(PREGUNTAS, o, 5).ids, Examen.armar(PREGUNTAS, o, 5).ids);
  assert.notDeepEqual(Examen.armar(PREGUNTAS, o, 5).ids, Examen.armar(PREGUNTAS, o, 6).ids);
});

test("filtra por temas y avisa cuántas faltan", () => {
  const { ids, faltan } = Examen.armar(PREGUNTAS, { duracion: 25, temas: [1] }, 1);
  assert.ok(ids.every((id) => POR_ID[id].tema === 1));
  assert.deepEqual(faltan, { seleccion_unica: 1, verdadero_falso: 5, respuesta_corta: 10 }); // tema 1: 5 SU, 0 F/V, 2 RC
  assert.ok(!ids.some((id) => POR_ID[id].tipo === "seleccion_multiple"), "sin selección múltiple");
});

// ---------- Temporizador con reloj simulado ----------
test("temporizador: cuenta desde la hora de inicio guardada", () => {
  const t0 = Date.UTC(2026, 9, 10, 14, 0, 0);
  const e = Examen.nuevo(PREGUNTAS, { duracion: 25, temas: [1, 2, 3] }, t0, 3);
  assert.equal(Examen.restante(e, t0), 25 * MIN);
  assert.equal(Examen.restante(e, t0 + 10 * MIN + 500), 15 * MIN - 500);
  assert.equal(Examen.formatoTiempo(Examen.restante(e, t0 + 10 * MIN + 500)), "15:00");
  assert.equal(Examen.formatoTiempo(Examen.restante(e, t0 + 24 * MIN + 59500)), "0:01");
  assert.equal(Examen.restante(e, t0 + 40 * MIN), 0);
  assert.equal(Examen.vencido(e, t0 + 25 * MIN - 1), false);
  assert.equal(Examen.vencido(e, t0 + 25 * MIN), true);
  assert.equal(Examen.formatoTiempo(60 * MIN), "1:00:00");
});

test("temporizador: sobrevive a una recarga (estado guardado como JSON)", () => {
  const t0 = 1_000_000;
  let e = Examen.nuevo(PREGUNTAS, { duracion: 40, temas: [2, 3] }, t0, 9);
  e.resp[e.ids[0]] = { op: "a" };
  // la página se recarga 12 min después: se lee el estado guardado
  const recargado = JSON.parse(JSON.stringify(e));
  assert.equal(Examen.restante(recargado, t0 + 12 * MIN), 28 * MIN);
  assert.deepEqual(recargado.resp, e.resp);
  // la pantalla estuvo bloqueada y se volvió después de que se acabó el tiempo
  assert.equal(Examen.vencido(recargado, t0 + 55 * MIN), true);
  const fin = Examen.terminar(recargado, POR_ID, t0 + 55 * MIN);
  assert.equal(fin.porTiempo, true);
  assert.equal(Examen.tiempoUsado(fin), 40 * MIN, "el tiempo usado no pasa de la duración");
});

test("terminar antes de tiempo: tiempo usado real y fase siguiente", () => {
  const t0 = 0;
  const e = Examen.nuevo(PREGUNTAS, { duracion: 25, temas: [1, 2, 3] }, t0, 11);
  const sinAuto = Examen.terminar(e, POR_ID, t0 + 7 * MIN);
  assert.equal(sinAuto.fase, "resultado", "sin respuestas que autoevaluar");
  assert.equal(Examen.tiempoUsado(sinAuto), 7 * MIN);
  assert.equal(sinAuto.porTiempo, false);
  const rcId = e.ids.find((id) => POR_ID[id].tipo === "respuesta_corta");
  e.resp[rcId] = { texto: "mi respuesta" };
  assert.equal(Examen.terminar(e, POR_ID, t0 + MIN).fase, "autoeval");
  assert.equal(e.fase, "examen", "terminar no modifica el estado original");
});

test("el orden de las opciones se sortea al empezar y queda guardado", () => {
  const e = Examen.nuevo(PREGUNTAS, { duracion: 60, temas: [1, 2, 3] }, 0, 31);
  const recargado = JSON.parse(JSON.stringify(e));
  let distintos = 0;
  for (const id of e.ids) {
    const p = POR_ID[id];
    const orden = Examen.ordenDe(recargado, p);
    assert.deepEqual(orden, e.orden[id], "la recarga conserva el orden");
    assert.deepEqual([...orden].sort(), p.opciones ? p.opciones.map((o) => o.id).sort() : []);
    if (p.tipo === "verdadero_falso") assert.deepEqual(orden, ["a", "b"], "F/V queda fijo");
    if (p.tipo === "seleccion_unica" && orden.join("") !== p.opciones.map((o) => o.id).join("")) distintos++;
  }
  assert.ok(distintos >= 5, "la selección única sí se baraja");
  assert.deepEqual(Examen.nuevo(PREGUNTAS, { duracion: 60, temas: [1, 2, 3] }, 0, 31).orden, e.orden, "misma semilla, mismo orden");
  const viejo = { ...e, orden: undefined };
  const su = POR_ID[e.ids[0]];
  assert.deepEqual(Examen.ordenDe(viejo, su), su.opciones.map((o) => o.id), "exámenes viejos: orden original");
});

test("resultado: nota sobre 100 y desglose por parte", () => {
  const e = Examen.nuevo(PREGUNTAS, { duracion: 25, temas: [1, 2, 3] }, 0, 21);
  for (const id of e.ids) {
    const p = POR_ID[id];
    if (p.tipo === "seleccion_unica") e.resp[id] = { op: p.correcta };
    if (p.tipo === "verdadero_falso") { e.resp[id] = { op: p.correcta, justif: "j" }; e.auto[id] = { justifOk: true }; }
  }
  const r = Examen.resultado(POR_ID, e);
  assert.deepEqual(r.partes.seleccion_unica, { obtenido: 6, maximo: 6, n: 6 });
  assert.deepEqual(r.partes.verdadero_falso, { obtenido: 10, maximo: 10, n: 5 });
  assert.deepEqual(r.partes.respuesta_corta, { obtenido: 0, maximo: 24, n: 12 });
  assert.equal(r.puntos, 16);
  assert.equal(r.nota, 40);
  assert.equal(r.items.filter((x) => !x.completo).length, 12);
});
