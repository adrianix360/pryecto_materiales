"""Correcciones de la auditoría técnica, aplicadas por construir.py después de armar el contenido.

Cada corrección cambia UN campo de UN ítem (por su id) y guarda el texto anterior: si el texto
actual ya no coincide con «antes», construir.py se detiene para no pisar un cambio posterior.
No se agregan, borran ni reordenan ítems (los ids son posicionales y el progreso depende de ellos).

Campos: frente, reverso, enunciado, explicacion, respuesta_modelo, puntos_clave, correcta,
verificar, definicion, termino, justificacion_oficial y opciones.<id> (texto de esa opción).
«antes»/«despues» = None significa que el campo no existía / se elimina.
"""

import json
import os

# Las correcciones viven en correcciones.json (con su razón y la evidencia: documento, página y cita).
_RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "correcciones.json")
with open(_RUTA, encoding="utf-8") as _f:
    CORRECCIONES = json.load(_f)["correcciones"]
