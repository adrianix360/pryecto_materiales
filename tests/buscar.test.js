// Pruebas del núcleo de Buscar (js/buscar.js). Uso: node --test tests/buscar.test.js
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const Buscar = require("../js/buscar.js");

const RAIZ = path.join(__dirname, "..");
const leer = (rel) => JSON.parse(fs.readFileSync(path.join(RAIZ, rel), "utf8"));
const IDX = leer("data/indice.json");
const TARJETAS = IDX.temas.flatMap((t) => leer(t.tarjetas).tarjetas);
const PREGUNTAS = IDX.temas.flatMap((t) => leer(t.preguntas).preguntas);
const GLOSARIO = leer("data/glosario.json").terminos;
const INDICE = Buscar.indexar(TARJETAS, PREGUNTAS, GLOSARIO);
const marcado = (segs) => segs.map((s) => (s.m ? `[${s.t}]` : s.t)).join("");

test("normaliza sin tildes ni mayúsculas y conserva el mapa de posiciones", () => {
  const r = Buscar.normalizarConMapa("Hormigón ÁRIDO");
  assert.equal(r.n, "hormigon arido");
  assert.equal(r.mapa.length, r.n.length);
  assert.equal(Buscar.normalizar("Exudación, Ñandú"), "exudacion, nandu");
});

test("encuentra sin importar tildes ni mayúsculas", () => {
  const a = Buscar.buscar(INDICE, "hormigon").map((e) => e.id);
  const b = Buscar.buscar(INDICE, "HORMIGÓN").map((e) => e.id);
  assert.ok(a.length > 0);
  assert.deepEqual(a, b);
  assert.ok(a.includes("t1-1A-01"), "la tarjeta «¿Concreto y hormigón son lo mismo?»");
});

test("con varias palabras, deben estar todas", () => {
  const una = Buscar.buscar(INDICE, "exudacion");
  const dos = Buscar.buscar(INDICE, "exudacion astm");
  assert.ok(dos.length > 0 && dos.length < una.length);
  for (const e of dos) {
    const texto = e.nt + " " + e.nc;
    assert.ok(texto.includes("exudacion") && texto.includes("astm"), e.id);
  }
  assert.deepEqual(Buscar.buscar(INDICE, "exudacion zzzqqq"), []);
});

test("menos de 2 letras no busca", () => {
  assert.deepEqual(Buscar.buscar(INDICE, "a"), []);
  assert.deepEqual(Buscar.buscar(INDICE, "   "), []);
  assert.ok(Buscar.buscar(INDICE, "pH").length > 0);
});

test("lo que coincide en el título va antes que lo del cuerpo", () => {
  const r = Buscar.buscar(INDICE, "mortero");
  const primeroCuerpo = r.findIndex((e) => !e.nt.includes("mortero"));
  const ultimoTitulo = r.map((e) => e.nt.includes("mortero")).lastIndexOf(true);
  assert.ok(primeroCuerpo === -1 || ultimoTitulo < primeroCuerpo);
  assert.equal(r[0].tipo, "glosario", "a igual puntaje, glosario primero");
  assert.equal(r[0].titulo, "Mortero");
});

test("agrupa por tipo (glosario, tarjetas, preguntas) y por tema", () => {
  const g = Buscar.agrupar(Buscar.buscar(INDICE, "agua"));
  assert.deepEqual(g.map((x) => x.tipo), ["glosario", "tarjeta", "pregunta"]);
  for (const grupo of g) {
    assert.equal(grupo.total, grupo.temas.reduce((a, t) => a + t.items.length, 0));
    const temas = grupo.temas.map((t) => t.tema);
    assert.deepEqual(temas, [...temas].sort());
    for (const t of grupo.temas) assert.ok(t.items.every((e) => e.tema === t.tema));
  }
});

test("resalta sobre el texto original, con sus tildes", () => {
  assert.equal(marcado(Buscar.resaltar("¿Concreto y hormigón son lo mismo?", "HORMIGON")), "¿Concreto y [hormigón] son lo mismo?");
  assert.equal(marcado(Buscar.resaltar("Agua de mezcla: agua potable", "agua")), "[Agua] de mezcla: [agua] potable");
  assert.equal(marcado(Buscar.resaltar("granulometría", "granulo metria")), "[granulometría]", "marcas que se tocan se unen");
  assert.equal(marcado(Buscar.resaltar("sin nada", "xyz")), "sin nada");
});

test("fragmento alrededor de la coincidencia", () => {
  const largo = "a ".repeat(200) + "exudación del concreto " + "b ".repeat(200);
  const f = Buscar.fragmento(largo, "exudacion", 80);
  assert.ok(f.startsWith("…") && f.endsWith("…"));
  assert.ok(f.includes("exudación"));
  assert.ok(f.length <= 82);
  assert.equal(Buscar.fragmento("corto", "x"), "corto");
});

test("glosario alfabético en español: «Á» va con la A", () => {
  const grupos = Buscar.glosarioPorLetra(GLOSARIO);
  const letras = grupos.map((g) => g.letra);
  assert.equal(new Set(letras).size, letras.length, "cada letra una sola vez");
  assert.ok(!letras.includes("Á"));
  assert.deepEqual(letras, [...letras].sort((a, b) => a.localeCompare(b, "es")));
  assert.equal(grupos.reduce((a, g) => a + g.terminos.length, 0), 60);
  const a = grupos.find((g) => g.letra === "A").terminos.map((t) => t.termino);
  assert.ok(a.some((t) => t.startsWith("Á")), "los términos con Á están en la A");
  assert.deepEqual(a, [...a].sort((x, y) => x.localeCompare(y, "es", { sensitivity: "base" })));
  assert.equal(Buscar.letraDe("ñandú"), "Ñ");
});

test("figuras: 15, con sus usos (9 de ensayos con 2 tarjetas, 6 de exámenes con 1 pregunta)", () => {
  const f = Buscar.figuras(TARJETAS, PREGUNTAS);
  assert.equal(f.length, 15);
  const ensayos = f.filter((x) => x.src.startsWith("img/ensayos/"));
  const examenes = f.filter((x) => x.src.startsWith("img/examenes/"));
  assert.equal(ensayos.length, 9);
  assert.ok(ensayos.every((x) => x.usos.length === 2 && x.usos.every((u) => u.tipo === "tarjeta")));
  assert.equal(examenes.length, 6);
  assert.ok(examenes.every((x) => x.usos.length === 1 && x.usos[0].tipo === "pregunta"));
  assert.ok(f.every((x) => x.alt && x.fuente.length && fs.existsSync(path.join(RAIZ, x.src))));
  // todas las imágenes de img/ensayos e img/examenes están en la galería
  const enDisco = ["ensayos", "examenes"].flatMap((d) => fs.readdirSync(path.join(RAIZ, "img", d)).map((n) => `img/${d}/${n}`));
  assert.deepEqual(f.map((x) => x.src).sort(), enDisco.sort());
});

test("verificar: 41 ítems (15 tarjetas y 26 preguntas) y texto para el profe", () => {
  const v = Buscar.aVerificar(TARJETAS, PREGUNTAS, GLOSARIO);
  assert.equal(v.length, 41);
  assert.equal(v.filter((x) => x.tipo === "tarjeta").length, 15);
  assert.equal(v.filter((x) => x.tipo === "pregunta").length, 26);
  const txt = Buscar.textoParaProfe(v.slice(0, 2), (r) => `doc ${r.doc} pág. ${r.pag}`);
  assert.match(txt, /^Consultas para el profe \(IC-0604, I examen\): 2 ítems/);
  assert.match(txt, new RegExp(`1\\. \\[${v[0].id}\\]`));
  assert.match(txt, /Duda: /);
  assert.match(txt, /Fuente: doc \d+ pág\. \d+/);
});
