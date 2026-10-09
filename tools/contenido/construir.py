"""Construye data/ a partir de los módulos de contenido. Uso: python3 tools/contenido/construir.py [raíz]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import FUENTES
import tarjetas3, preguntas3_examen, preguntas3_teoria, glosario3, tema2, tema1

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PAGINAS = {"01": 6, "02": 5, "03": 9, "04": 5, "05": 12, "06": 11, "08": 5, "09": 3, "10": 7, "11": 8, "12": 73, "13": 11,
           "14": 16, "15": 23, "16": 6, "19": 120, "20": 3, "22": 1, "24": 12, "25": 2, "26": 87,
           "X01": 8, "X02": 3, "X04": 8, "X06": 4, "X07": 14, "X14": 10, "X15": 7}
TEMAS = {
    1: ("Introducción y definiciones básicas", tema1.T, tema1.P),
    2: ("Agua para concreto", tema2.T, tema2.P),
    3: ("Agregados", tarjetas3.T, preguntas3_examen.P + preguntas3_teoria.P),
}
SUBTEMAS = {"1A": "Concreto, mortero, pasta y tipos de materiales", "2A": "Calidad del agua", "2B": "Cantidad de agua y concreto fresco",
            "3A": "Importancia, clasificación y características", "3B": "Rocas y reactividad", "3C": "Volúmenes, masas y humedad",
            "3D": "Granulometría", "3E": "Ensayos de laboratorio"}


def dump(rel, obj):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


dump("data/fuentes.json", {"version": 1, "fuentes": {k: dict(v, codigo=k, paginas=PAGINAS[k]) for k, v in FUENTES.items()}})
indice = []
for n, (titulo, T, P) in TEMAS.items():
    dump(f"data/tarjetas/tema{n}.json", {"tema": n, "titulo": titulo, "tarjetas": T})
    dump(f"data/preguntas/tema{n}.json", {"tema": n, "titulo": titulo, "preguntas": P})
    indice.append({"tema": n, "titulo": titulo, "tarjetas": f"data/tarjetas/tema{n}.json", "preguntas": f"data/preguntas/tema{n}.json",
                   "subtemas": {k: v for k, v in SUBTEMAS.items() if k.startswith(str(n))}})
    print(f"Tema {n}: {len(T)} tarjetas, {len(P)} preguntas")
dump("data/indice.json", {"version": 1, "examen": "2026-10-17", "temas": indice})
G = tema1.G + tema2.G + glosario3.G
dump("data/glosario.json", {"terminos": sorted(G, key=lambda x: x["termino"].lower())})
print(f"Glosario: {len(G)} términos")
