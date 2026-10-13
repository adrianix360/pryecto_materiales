#!/usr/bin/env python3
"""Valida los JSON de contenido (data/). Uso: python3 tools/validar_json.py [raíz del sitio]

Revisa: JSON bien formado, ids únicos, campos obligatorios, una sola respuesta correcta
en selección única y falso/verdadero, fuentes existentes con página válida, figuras existentes
y que las preguntas nuevas no usen "todas las anteriores". Sale con código 1 si hay errores.
"""
import glob
import json
import os
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
TIPOS_P = {"seleccion_unica", "seleccion_multiple", "verdadero_falso", "respuesta_corta"}
TIPOS_T = {"concepto", "dato", "clasificacion", "formula", "norma", "proceso", "equipo", "parametros", "criterio"}
CLAVES = {"oficial", "documental", "pendiente"}
errores, avisos = [], []


def err(i, m):
    errores.append(f"{i}: {m}")


def cargar(rel):
    try:
        with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001
        errores.append(f"{rel}: JSON inválido ({e})")
        return None


fu = cargar("data/fuentes.json") or {"fuentes": {}}
FUENTES = fu["fuentes"]
ids = {}


def ref_ok(i, r, campo="fuente"):
    if r.get("doc") not in FUENTES:
        err(i, f"{campo}: documento desconocido {r.get('doc')!r}")
        return
    pag = r.get("pag")
    if not isinstance(pag, int) or pag < 1 or pag > FUENTES[r["doc"]]["paginas"]:
        err(i, f"{campo}: página {pag!r} fuera de rango para {r['doc']}")


def unico(i):
    if i in ids:
        err(i, "id repetido")
    ids[i] = True


def figura_ok(i, fig):
    if not fig:
        return
    if not os.path.exists(os.path.join(RAIZ, fig["src"])):
        err(i, f"figura inexistente {fig['src']}")
    if not fig.get("alt"):
        err(i, "figura sin texto alternativo")
    if not fig.get("fuente"):
        err(i, "figura sin fuente")
    for r in fig.get("fuente", []):
        ref_ok(i, r, "figura.fuente")


n_t = n_p = 0
for ruta in sorted(glob.glob(os.path.join(RAIZ, "data/tarjetas/*.json"))):
    d = cargar(os.path.relpath(ruta, RAIZ))
    for t in (d or {}).get("tarjetas", []):
        n_t += 1
        i = t.get("id", "?")
        unico(i)
        for c in ("tema", "subtema", "tipo", "frente", "reverso", "fuente"):
            if not t.get(c):
                err(i, f"falta {c}")
        if t.get("tipo") not in TIPOS_T:
            err(i, f"tipo de tarjeta inválido {t.get('tipo')!r}")
        for r in t.get("fuente", []):
            ref_ok(i, r)
        figura_ok(i, t.get("figura"))

for ruta in sorted(glob.glob(os.path.join(RAIZ, "data/preguntas/*.json"))):
    d = cargar(os.path.relpath(ruta, RAIZ))
    for p in (d or {}).get("preguntas", []):
        n_p += 1
        i = p.get("id", "?")
        unico(i)
        tipo = p.get("tipo")
        if tipo not in TIPOS_P:
            err(i, f"tipo inválido {tipo!r}")
        for c in ("enunciado", "explicacion", "origen", "clave"):
            if not p.get(c):
                err(i, f"falta {c}")
        if p.get("clave") not in CLAVES:
            err(i, f"clave inválida {p.get('clave')!r}")
        if p.get("origen") == "examen":
            ex = p.get("examen") or {}
            ref_ok(i, ex, "examen")
            if not ex.get("pregunta") or not ex.get("periodo"):
                err(i, "examen sin número de pregunta o periodo")
        elif p.get("origen") == "teoria":
            if not p.get("fuente"):
                err(i, "pregunta de teoría sin fuente")
        else:
            err(i, f"origen inválido {p.get('origen')!r}")
        for r in p.get("fuente", []):
            ref_ok(i, r)
        if p.get("clave") != "oficial" and not p.get("fuente") and p.get("clave") != "pendiente":
            err(i, "respuesta derivada sin fuente documental")
        if tipo in ("seleccion_unica", "seleccion_multiple", "verdadero_falso"):
            ops = p.get("opciones") or []
            idsop = [o.get("id") for o in ops]
            if len(ops) < 2 or len(set(idsop)) != len(idsop) or any(not o.get("texto") for o in ops):
                err(i, "opciones inválidas")
            cor = p.get("correcta")
            if tipo == "seleccion_multiple":
                if not isinstance(cor, list) or not cor or any(c not in idsop for c in cor):
                    err(i, "correctas inválidas en selección múltiple")
            else:
                if not isinstance(cor, str) or cor not in idsop:
                    err(i, "selección única o F/V necesita exactamente una correcta válida")
            if p.get("origen") == "teoria":
                for o in ops:
                    if "todas las anteriores" in o["texto"].lower():
                        err(i, "opción «todas las anteriores» no permitida")
        if tipo == "respuesta_corta":
            if not p.get("respuesta_modelo"):
                err(i, "falta respuesta_modelo")
            pk = p.get("puntos_clave") or []
            if not (1 <= len(pk) <= 5):
                err(i, "puntos_clave debe tener de 1 a 5 elementos")
            if p.get("origen") == "teoria" and not (2 <= len(pk) <= 5):
                err(i, "pregunta de teoría: puntos_clave debe tener de 2 a 5")
        figura_ok(i, p.get("figura"))
        if p.get("clave") == "pendiente":
            avisos.append(f"{i}: clave pendiente")

g = cargar("data/glosario.json") or {"terminos": []}
vistos = set()
for t in g["terminos"]:
    i = t.get("id", "?")
    unico(i)
    if t["termino"].lower() in vistos:
        err(i, "término repetido")
    vistos.add(t["termino"].lower())
    if not t.get("definicion") or not t.get("fuente"):
        err(i, "término sin definición o sin fuente")
    for r in t.get("fuente", []):
        ref_ok(i, r)

# ---- Normas ASTM (entrenamiento «Normas») ----
nd = cargar("data/normas.json") or {"familias": [], "normas": []}
fam_ids = {f.get("id") for f in nd["familias"]}
ids_norma = [n.get("id") for n in nd["normas"]]
for n in nd["normas"]:
    i = "norma " + str(n.get("id", "?"))
    if ids_norma.count(n.get("id")) > 1:
        err(i, "id repetido")
    if n.get("designacion") != "ASTM " + str(n.get("id")):
        err(i, "designacion debe ser «ASTM » + id")
    if n.get("familia") not in fam_ids:
        err(i, f"familia desconocida {n.get('familia')!r}")
    for c in ("mide", "gancho", "fuente"):
        if not n.get(c):
            err(i, f"falta {c}")
    if not n.get("confunde_con"):
        err(i, "falta confunde_con (cada norma tiene al menos una pareja)")
    for otra in n.get("confunde_con", []):
        if otra not in ids_norma or otra == n.get("id"):
            err(i, f"confunde_con apunta a una norma inexistente o a sí misma: {otra!r}")
    for r in n.get("fuente", []):
        ref_ok(i, r)
    # El texto de la pregunta no puede regalar la respuesta: «mide» no menciona ninguna designación.
    for otra in ids_norma:
        if otra and otra in n.get("mide", "").replace("-", " ").split():
            err(i, f"«mide» menciona la norma {otra}")

print(f"Tarjetas: {n_t} · Preguntas: {n_p} · Glosario: {len(g['terminos'])} · Normas: {len(nd['normas'])}")
for a in avisos:
    print("AVISO", a)
for e in errores:
    print("ERROR", e)
print("OK" if not errores else f"{len(errores)} errores")
sys.exit(1 if errores else 0)
