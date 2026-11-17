"""Construye data/ a partir de los módulos de contenido. Uso: python3 tools/contenido/construir.py [raíz]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import FUENTES
import tarjetas3, preguntas3_examen, preguntas3_teoria, glosario3, tema2, tema1, normas

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PAGINAS = {"01": 6, "02": 5, "03": 9, "04": 5, "05": 12, "06": 11, "08": 5, "09": 3, "10": 7, "11": 8, "12": 73, "13": 11,
           "14": 16, "15": 23, "16": 6, "17": 84, "19": 120, "20": 3, "22": 1, "24": 12, "25": 2, "26": 87,
           "X01": 8, "X02": 3, "X04": 8, "X06": 4, "X07": 14, "X14": 10, "X15": 7, "X17": 3}
TEMAS = {
    1: ("Introducción y definiciones básicas", tema1.T, tema1.P),
    2: ("Agua para concreto", tema2.T, tema2.P),
    3: ("Agregados", tarjetas3.T, preguntas3_examen.P + preguntas3_teoria.P),
}
SUBTEMAS = {"1A": "Concreto, mortero, pasta y tipos de materiales", "2A": "Calidad del agua", "2B": "Cantidad de agua y concreto fresco",
            "3A": "Importancia, clasificación y características", "3B": "Rocas y reactividad", "3C": "Volúmenes, masas y humedad",
            "3D": "Granulometría", "3E": "Ensayos de laboratorio"}


def aplicar_correcciones():
    """Aplica tools/contenido/correcciones.py sobre los ítems ya armados (ver ese archivo)."""
    from correcciones import CORRECCIONES
    todos = {}
    for lista in (tema1.T, tema1.P, tema1.G, tema2.T, tema2.P, tema2.G, tarjetas3.T,
                  preguntas3_examen.P, preguntas3_teoria.P, glosario3.G):
        for it in lista:
            todos[it["id"]] = it
    for c in CORRECCIONES:
        it = todos.get(c["id"])
        if it is None:
            raise SystemExit(f"Corrección: no existe el ítem {c['id']}")
        campo = c["campo"]
        if campo.startswith("opciones."):
            oid = campo.split(".", 1)[1]
            dueno, clave = next(o for o in it["opciones"] if o["id"] == oid), "texto"
        else:
            dueno, clave = it, campo
        if dueno.get(clave) != c["antes"]:
            raise SystemExit(f"Corrección {c['id']}.{campo}: el texto actual no coincide con «antes»")
        if c["despues"] is None:
            dueno.pop(clave, None)
        else:
            dueno[clave] = c["despues"]
    print(f"Correcciones de auditoría aplicadas: {len(CORRECCIONES)}")


aplicar_correcciones()


def dump(rel, obj):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


# ---- II examen (temas 4 y 8): contenido en tools/contenido/examen2/*.json (ver README) ----
EX2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examen2")
TEMAS_EX2 = {4: "Cemento hidráulico", 8: "Concreto hidráulico"}
SUBTEMAS_EX2 = {
    "4A": "Historia y definición del cemento", "4B": "Producción del cemento y del clínker",
    "4C": "Compuestos químicos, hidratación y sulfato de calcio", "4D": "Tipos y clasificación de cementos",
    "4E": "Propiedades físicas y mecánicas del cemento y sus ensayos", "4F": "Puzolanas y adiciones minerales",
    "8A": "Concreto fresco", "8B": "Diseño de mezclas", "8C": "Concreto endurecido y factores que afectan la resistencia",
    "8D": "Durabilidad", "8E": "Ensayos de laboratorio del concreto", "8F": "Aditivos"}
FUENTES_EX2 = {  # código: (título legible, autor, del_profe)
    "E01": ("Manual de Laboratorio: cementos", "Ing. Einer Rodríguez", True),
    "E02": ("Manual de Laboratorio: concreto", "Ing. Einer Rodríguez", True),
    "E03": ("Clases de cemento (presentación)", "Ing. Einer Rodríguez", True),
    "E04": ("Factores que afectan la resistencia del concreto (presentación)", "Ing. Einer Rodríguez", True),
    "E05": ("Carbonatación (presentación)", "Ing. Einer Rodríguez", True),
    "E06": ("Historia del cemento", "Ing. Einer Rodríguez", True),
    "E07": ("Producción del cemento", "Ing. Einer Rodríguez", True),
    "E08": ("Producción del clínker", "Ing. Einer Rodríguez", True),
    "E09": ("Diseño de mezclas: pasos detallados", "Ing. Einer Rodríguez", True),
    "E10": ("INTE 06-11-15:2005 (norma INTECO)", "INTECO", False),
    "E11": ("Producción del cemento y tipos de cemento Portland (lectura del grupo H)", "Lectura de grupo (PCA)", False),
    "E12": ("Propiedades físicas del cemento (lectura del grupo I)", "Lectura de grupo (PCA)", False),
    "E13": ("Puzolanas y efectos en el concreto endurecido (lectura del grupo J)", "Lectura de grupo (PCA)", False),
    "E14": ("Puzolana y concreto endurecido (lectura del grupo K)", "Lectura de grupo (PCA)", False),
    "E15": ("Compuestos químicos del cemento (lectura del grupo L)", "Lectura de grupo (PCA)", False),
    "E16": ("Concreto endurecido, Navas págs. 119–126 (lectura del grupo M)", "Navas (lectura de grupo)", False),
    "E17": ("Concreto fresco, Navas págs. 97–107 (lectura del grupo N)", "Navas (lectura de grupo)", False),
    "E18": ("Tarea 16", "Tarea del curso", False),
    "E19": ("Tarea 17", "Tarea del curso", False)}
EXAMENES = [
    {"id": 1, "titulo": "I examen", "fecha": "2026-10-17", "temas": [1, 2, 3], "simulacro": [1, 2, 3]},
    {"id": 2, "titulo": "II examen", "fecha": "2026-12-02", "temas": [4, 8], "simulacro": [1, 2, 3, 4, 8]}]


def leer_ex2(nombre):
    ruta = os.path.join(EX2, nombre)
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


fuentes_json = {k: dict(v, codigo=k, paginas=PAGINAS[k]) for k, v in FUENTES.items()}
_codigos = os.path.join(SITE, "fuentes", "examen2", "codigos.json")
_pag_ex2 = {}
if os.path.exists(_codigos):
    with open(_codigos, encoding="utf-8") as f:
        _pag_ex2 = {k: v["paginas"] for k, v in json.load(f).items()}
for k, (tit, aut, prof) in FUENTES_EX2.items():
    if k in _pag_ex2:
        _arch = json.load(open(_codigos, encoding="utf-8"))[k]["archivo"]
        fuentes_json[k] = {"archivo": "examen2/pdf/" + _arch, "titulo": tit, "autor": aut, "del_profe": prof,
                           "codigo": k, "paginas": _pag_ex2[k]}
if not _pag_ex2 and os.path.exists(os.path.join(SITE, "data", "fuentes.json")):
    # Sin fuentes/ (p. ej. en otra máquina): se conservan las E01–E19 ya generadas.
    with open(os.path.join(SITE, "data", "fuentes.json"), encoding="utf-8") as f:
        for k, v in json.load(f)["fuentes"].items():
            if k.startswith("E"):
                fuentes_json[k] = v
dump("data/fuentes.json", {"version": 1, "fuentes": fuentes_json})
indice = []
for n, (titulo, T, P) in TEMAS.items():
    dump(f"data/tarjetas/tema{n}.json", {"tema": n, "titulo": titulo, "tarjetas": T})
    dump(f"data/preguntas/tema{n}.json", {"tema": n, "titulo": titulo, "preguntas": P})
    indice.append({"tema": n, "titulo": titulo, "examen": 1, "tarjetas": f"data/tarjetas/tema{n}.json", "preguntas": f"data/preguntas/tema{n}.json",
                   "subtemas": {k: v for k, v in SUBTEMAS.items() if k.startswith(str(n))}})
    print(f"Tema {n}: {len(T)} tarjetas, {len(P)} preguntas")
G_EX2 = []
for n, titulo in TEMAS_EX2.items():
    d = leer_ex2(f"tema{n}.json") or {}
    T, P = d.get("tarjetas", []), d.get("preguntas", [])
    subs = dict(SUBTEMAS_EX2)
    subs.update(d.get("subtemas", {}))
    titulo = d.get("titulo", titulo)
    dump(f"data/tarjetas/tema{n}.json", {"tema": n, "titulo": titulo, "tarjetas": T})
    dump(f"data/preguntas/tema{n}.json", {"tema": n, "titulo": titulo, "preguntas": P})
    indice.append({"tema": n, "titulo": titulo, "examen": 2, "tarjetas": f"data/tarjetas/tema{n}.json",
                   "preguntas": f"data/preguntas/tema{n}.json", "subtemas": {k: v for k, v in subs.items() if k.startswith(str(n))}})
    print(f"Tema {n} (II examen): {len(T)} tarjetas, {len(P)} preguntas" + ("" if d else "  [sin archivo en examen2/]"))
G_EX2 = (leer_ex2("glosario.json") or {}).get("terminos", [])
dump("data/normas.json", {"version": 1, "familias": normas.FAMILIAS, "normas": normas.NORMAS})
print(f"Normas: {len(normas.NORMAS)}")
dump("data/indice.json", {"version": 1, "examen": "2026-10-17", "examenes": EXAMENES, "temas": indice})
G = tema1.G + tema2.G + glosario3.G + G_EX2
dump("data/glosario.json", {"terminos": sorted(G, key=lambda x: x["termino"].lower())})
print(f"Glosario: {len(G)} términos")
