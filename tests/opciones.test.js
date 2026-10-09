// Pruebas del orden aleatorio de opciones (js/opciones.js). Uso: node --test tests/opciones.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const Opciones = require("../js/opciones.js");

const RAIZ = path.join(__dirname, "..");
const leer = (rel) => JSON.parse(fs.readFileSync(path.join(RAIZ, rel), "utf8"));
const PREGUNTAS = leer("data/indice.json").temas.flatMap((t) => leer(t.preguntas).preguntas);
const POR_ID = Object.fromEntries(PREGUNTAS.map((p) => [p.id, p]));
const SELECCION = PREGUNTAS.filter((p) => p.tipo === "seleccion_unica" || p.tipo === "seleccion_multiple");

function azar(semilla) {
  let a = semilla >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

test("baraja selección única y múltiple; falso o verdadero queda fijo", () => {
  const rnd = azar(1);
  const vf = PREGUNTAS.find((p) => p.tipo === "verdadero_falso");
  for (let i = 0; i < 20; i++) assert.deepEqual(Opciones.ordenPara(vf, rnd), ["a", "b"]);
  const su = POR_ID["p1-1A-t01"];
  const ordenes = new Set();
  for (let i = 0; i < 50; i++) {
    const o = Opciones.ordenPara(su, rnd);
    assert.deepEqual([...o].sort(), ["a", "b", "c", "d"], "mismas opciones, sin perder ni repetir");
    ordenes.add(o.join(""));
  }
  assert.ok(ordenes.size > 5, "el orden cambia");
});

test("«Ninguna de las anteriores» no se mueve de su lugar", () => {
  const rnd = azar(5);
  const fijas = SELECCION.filter((p) => p.opciones.some((o) => /anterior/i.test(o.texto)));
  assert.equal(fijas.length, 3);
  for (const p of fijas) {
    const i = p.opciones.findIndex((o) => /anterior/i.test(o.texto));
    const vistos = new Set();
    for (let k = 0; k < 30; k++) {
      const o = Opciones.ordenPara(p, rnd);
      assert.equal(o[i], p.opciones[i].id, p.id);
      assert.deepEqual([...o].sort(), p.opciones.map((x) => x.id).sort());
      vistos.add(o.join(""));
    }
    assert.ok(vistos.size > 1, `${p.id}: las demás sí se barajan`);
  }
});

test("la correcta cae en cada posición más o menos igual de seguido", () => {
  const rnd = azar(7);
  const cuatro = SELECCION.filter((p) => p.tipo === "seleccion_unica" && p.opciones.length === 4);
  const conteo = [0, 0, 0, 0];
  let n = 0;
  for (let r = 0; r < 4000; r++) {
    const p = cuatro[r % cuatro.length];
    conteo[Opciones.ordenPara(p, rnd).indexOf(p.correcta)]++;
    n++;
  }
  for (const c of conteo) assert.ok(c / n > 0.2 && c / n < 0.3, JSON.stringify(conteo));
});

test("letra y mapa siguen el orden mostrado", () => {
  const orden = ["c", "a", "d", "b"];
  assert.equal(Opciones.letra(orden, "c"), "A");
  assert.equal(Opciones.letra(orden, "b"), "D");
  assert.deepEqual(Opciones.mapa(orden), { C: "A", A: "B", D: "C", B: "D" });
});

test("reletrar cambia las citas de opciones", () => {
  const m = Opciones.mapa(["c", "a", "d", "b"]); // C→A, A→B, D→C, B→D
  assert.equal(
    Opciones.reletrar("Correcta la B. La A es la pasta, la C es el concreto y la D no corresponde.", m),
    "Correcta la D. La B es la pasta, la A es el concreto y la C no corresponde.");
  assert.equal(Opciones.reletrar("El agregado (A, B) y el aditivo (D).", m), "El agregado (B, D) y el aditivo (C).");
  assert.equal(Opciones.reletrar("Correctas la A, la B, la C y la E.", m), "Correctas la B, la D, la A y la E.", "la E no es opción: queda igual");
  assert.equal(Opciones.reletrar("Las sales de sodio y potasio (C, D)", m), "Las sales de sodio y potasio (A, C)");
});

test("reletrar no toca variables, graduaciones ni palabras", () => {
  const m = Opciones.mapa(["d", "c", "b", "a"]); // A↔D, B↔C
  assert.equal(Opciones.reletrar("(w > D aporta; w < D absorbe)", m), "(w > D aporta; w < D absorbe)");
  assert.equal(Opciones.reletrar("Correcta la A: D = PWD / Ps × 100", m), "Correcta la D: D = PWD / Ps × 100");
  assert.equal(Opciones.reletrar("GBSS = GBS (1 + D) = 2,652", m), "GBSS = GBS (1 + D) = 2,652");
  assert.equal(Opciones.reletrar("Correcta la D: A → 12, B → 11, C → 8 y D → 6 esferas.", m),
    "Correcta la A: A → 12, B → 11, C → 8 y D → 6 esferas.");
  assert.equal(Opciones.reletrar("a 110 °C, la a/c, ASTM C117, Bien", m), "a 110 °C, la a/c, ASTM C117, Bien");
  assert.equal(Opciones.reletrar(null, m), null);
});

test("en las 72 preguntas reales, reletrar y deshacer devuelve el texto original", () => {
  const rnd = azar(3);
  let cambiadas = 0;
  for (const p of SELECCION) {
    for (let k = 0; k < 5; k++) {
      const orden = Opciones.ordenPara(p, rnd);
      const ida = Opciones.mapa(orden);
      const vuelta = Object.fromEntries(Object.entries(ida).map(([a, b]) => [b, a]));
      for (const campo of ["explicacion", "verificar"]) {
        if (!p[campo]) continue;
        const nuevo = Opciones.reletrar(p[campo], ida);
        if (nuevo !== p[campo]) cambiadas++;
        assert.equal(Opciones.reletrar(nuevo, vuelta), p[campo], `${p.id} ${campo}`);
      }
    }
    // «Correcta la X» apunta siempre a la opción correcta en la letra mostrada
    const orden = Opciones.ordenPara(p, rnd);
    const m = Opciones.mapa(orden);
    const cita = /^Correctas? la ([A-E])/.exec(p.explicacion || "");
    if (cita && p.tipo === "seleccion_unica") {
      assert.equal(Opciones.reletrar(p.explicacion, m).charAt(cita[0].length - 1), Opciones.letra(orden, p.correcta), p.id);
    }
  }
  assert.ok(cambiadas > 100);
});
