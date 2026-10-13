# Esquema de `data/`

Resumen del esquema **real** de los JSON, obtenido leyendo los archivos (9 de octubre de 2026). Si un campo no aparece aquí, no existe en los datos.

**Conteo actual:** 153 tarjetas, 202 preguntas, 60 términos de glosario, 30 normas y 30 fuentes. `tools/validar_json.py` da OK.

> **Los JSON se generan.** `data/` sale de `tools/contenido/construir.py` (módulos `tema1.py`, `tema2.py`, `tarjetas3.py`, `preguntas3_*.py`, `glosario3.py` y `comun.py`). Si se edita un JSON a mano y luego se corre el generador, el cambio se pierde: el contenido se corrige en los módulos y se regenera. Las correcciones de la auditoría técnica (9/10/2026) están en `tools/contenido/correcciones.json`: cada una cambia un campo de un ítem y guarda el texto anterior, la razón y la evidencia; `construir.py` las aplica al final y se detiene si el texto anterior ya no coincide.

## Archivos

| Archivo | Contenido |
|---|---|
| `data/indice.json` | Lista de temas, rutas a sus JSON y nombres de subtemas |
| `data/fuentes.json` | Catálogo de fuentes citables (código → archivo, autor, páginas) |
| `data/tarjetas/temaN.json` | Tarjetas de estudio del tema N (N = 1, 2, 3) |
| `data/preguntas/temaN.json` | Preguntas de práctica del tema N |
| `data/glosario.json` | Términos del glosario (los tres temas juntos) |
| `data/normas.json` | Familias y normas ASTM del entrenamiento «Normas» (30 normas, 9 familias) |

Formato: UTF-8, sin escapar caracteres (`ensure_ascii=False`), sangría de 1 espacio.

---

## Referencia a fuente (objeto común)

Se usa en `fuente[]` de tarjetas, preguntas y glosario, y en `figura.fuente[]`.

| Campo | Tipo | Oblig. | Descripción |
|---|---|---|---|
| `doc` | string | sí | Código de `fuentes.json` (`"03"`, `"19"`, `"X01"`…) |
| `pag` | entero | sí | Página **del PDF**, de 1 a `paginas` de esa fuente |
| `impresa` | string | no | Página impresa del original, como texto: `"97"` (PCA) o `"2/6"` (Navas) |
| `pregunta` | string | no | Pregunta concreta dentro de un examen citado como fuente: `"F/V 6"`, `"respuesta corta 10"` |

---

## `indice.json`

```json
{ "version": 1, "examen": "2026-10-17", "temas": [ … ] }
```

| Campo | Tipo | Descripción |
|---|---|---|
| `version` | entero | Versión del índice (hoy 1) |
| `examen` | string (AAAA-MM-DD) | Fecha del I examen |
| `temas[]` | lista | Un objeto por tema |
| `temas[].tema` | entero | 1, 2 o 3 |
| `temas[].titulo` | string | Nombre del tema |
| `temas[].tarjetas` | string | Ruta relativa: `data/tarjetas/temaN.json` |
| `temas[].preguntas` | string | Ruta relativa: `data/preguntas/temaN.json` |
| `temas[].subtemas` | objeto | Código → título. Códigos actuales: `1A`, `2A`, `2B`, `3A`, `3B`, `3C`, `3D`, `3E` |

---

## `fuentes.json`

```json
{ "version": 1, "fuentes": { "03": { … }, "X01": { … } } }
```

Diccionario indexado por código. Hay 30: `01`–`06`, `08`–`17`, `19`, `20`, `22`, `24`–`26` y los exámenes `X01`, `X02`, `X04`, `X06`, `X07`, `X14`, `X15`, `X17`.

| Campo | Tipo | Descripción |
|---|---|---|
| `archivo` | string | Ruta del original dentro de `fuentes/` (no se publica; es solo para trazabilidad) |
| `titulo` | string | Título legible |
| `autor` | string | Autor o procedencia |
| `del_profe` | booleano | `true` si es fuente "del profe" (manda en contradicciones; ver ALCANCE.md §0) |
| `codigo` | string | Igual a la clave del diccionario |
| `paginas` | entero | Total de páginas del PDF; el validador lo usa para revisar `pag` |

---

## Tarjetas (`data/tarjetas/temaN.json`)

```json
{ "tema": 1, "titulo": "…", "tarjetas": [ … ] }
```

| Campo | Tipo | Oblig. | Descripción |
|---|---|---|---|
| `id` | string | sí | `t{tema}-{subtema}-{NN}`, p. ej. `t1-1A-01`. Único en todo `data/` |
| `tema` | entero | sí | 1, 2 o 3 |
| `subtema` | string | sí | Código de `indice.json` |
| `tipo` | string | sí | `concepto`, `dato`, `clasificacion`, `formula`, `norma`, `proceso`, `equipo`, `parametros` o `criterio` |
| `frente` | string | sí | Pregunta o pista |
| `reverso` | string | sí | Respuesta |
| `fuente` | lista de referencias | sí | Al menos una |
| `origen` | string | — | Hoy siempre `"teoria"` (el validador no lo revisa) |
| `verificar` | string | no | Nota de contradicción o duda (16 tarjetas). Si existe, la app debe mostrar la marca VERIFICAR |
| `figura` | objeto | no | Ver **Figura** (18 tarjetas, todas del tema 3E) |

---

## Preguntas (`data/preguntas/temaN.json`)

```json
{ "tema": 1, "titulo": "…", "preguntas": [ … ] }
```

### Campos comunes

| Campo | Tipo | Oblig. | Descripción |
|---|---|---|---|
| `id` | string | sí | `p{tema}-{subtema}-x{NN}` (de examen) o `p{tema}-{subtema}-t{NN}` (de teoría) |
| `tema`, `subtema` | entero, string | sí | Igual que en tarjetas |
| `tipo` | string | sí | `seleccion_unica`, `seleccion_multiple`, `verdadero_falso` o `respuesta_corta` |
| `enunciado` | string | sí | Puede traer `\n`. En las de examen se copia textual (incluye el puntaje si el original lo trae) |
| `origen` | string | sí | `examen` o `teoria` |
| `clave` | string | sí | `oficial` (clave del examen), `documental` (armada con las fuentes) o `pendiente` (hoy ninguna) |
| `explicacion` | string | sí | Por qué es correcta la respuesta y por qué fallan las demás |
| `fuente` | lista de referencias | sí en `teoria` | Respaldo documental. La traen 195 de 202; las 7 que no, son de examen con clave oficial |
| `examen` | objeto | sí en `examen` | `{doc, pag, pregunta, periodo}`. `doc` y `pag` se validan como una referencia; `pregunta` es el número en el original (`"1.1, caso 2"`) y `periodo` el ciclo (`"I-2026"`, `"Sin fecha (cuestionario de Mediación Virtual)"`) |
| `verificar` | string | no | Nota de contradicción o duda (28 preguntas) |
| `figura` | objeto | no | Ver **Figura** (6 preguntas: 5 del examen 08 y el ábaco de X01) |

Combinaciones actuales de `origen` + `clave`: examen + oficial (130), teoría + documental (68), examen + documental (4).

### Según el tipo

| Tipo | Campos extra | Notas |
|---|---|---|
| `seleccion_unica` (76) | `opciones[]`, `correcta` (string) | 2 a 5 opciones (67 tienen 4) |
| `seleccion_multiple` (6) | `opciones[]`, `correcta` (lista de ids) | 4 o 5 opciones |
| `verdadero_falso` (49) | `opciones[]`, `correcta` (string), `justificacion_oficial` (string, opcional) | Opciones siempre `a` = "Verdadero", `b` = "Falso". `justificacion_oficial` está en 43: es la justificación textual de la clave |
| `respuesta_corta` (71) | `respuesta_modelo` (string), `puntos_clave` (lista de strings) | 1 a 5 puntos clave; las de teoría necesitan de 2 a 5 |

`opciones[]` = `[{ "id": "a", "texto": "…" }, …]`. Ids en minúscula (`a`–`e`). Las preguntas de teoría no pueden usar "todas las anteriores".

---

## Figura (objeto común)

| Campo | Tipo | Descripción |
|---|---|---|
| `src` | string | Ruta relativa a la raíz del sitio: `img/ensayos/c117.jpg`, `img/examenes/X01-p5-abaco.jpg` |
| `alt` | string | Texto alternativo (obligatorio) |
| `fuente` | lista de referencias | De dónde salió la imagen (obligatoria) |

---

## Glosario (`data/glosario.json`)

```json
{ "terminos": [ … ] }
```

No tiene `version` ni `titulo`.

| Campo | Tipo | Oblig. | Descripción |
|---|---|---|---|
| `id` | string | sí | `g-{termino-en-minusculas}`, p. ej. `g-mortero`. Tres ids llevan letras griegas (`g-densidad-aparente-δs`, `g-densidad-bruta-seca-δbs`, `g-peso-unitario-densidad-masiva-δb`) |
| `termino` | string | sí | Único sin distinguir mayúsculas |
| `definicion` | string | sí | |
| `tema`, `subtema` | entero, string | — | Presentes en los 60 términos (el validador no los revisa) |
| `fuente` | lista de referencias | sí | |

---

## Normas (`data/normas.json`)

```json
{ "version": 1, "familias": [ … ], "normas": [ … ] }
```

`familias[]` = `{id, titulo}`, en el orden de estudio. Se generan desde `tools/contenido/normas.py`.

| Campo de `normas[]` | Tipo | Oblig. | Descripción |
|---|---|---|---|
| `id` | string | sí | `C127`, `D75`… Único |
| `designacion` | string | sí | `"ASTM " + id` |
| `familia` | string | sí | Id de una familia |
| `mide` | string | sí | Qué determina, con las palabras de la fuente. **No nombra ninguna norma**: es el enunciado de «Escribir» y la opción de «¿Qué determina?» |
| `detalle` | string | no | Dato de apoyo con su página (límites, definiciones) |
| `figura` | objeto (ver Figura) | no | Foto del equipo; la tienen 16 normas. Activa la ficha «foto» y el simulacro de fotos. `alt` describe la foto y **solo se muestra después de responder** |
| `confunde_con` | lista de ids | sí | Parejas con las que se confunde (al menos una; deben existir) |
| `gancho` | string | sí | Ayuda de memoria. **No es dato del curso**; la app lo rotula «Ayuda de memoria» |
| `fuente` | lista de referencias | sí | Al menos una; `doc` `17` es el Manual de cementos (solo C305, C1437, C109 y C191) |
| `verificar` | string | no | Duda o contradicción (C994, D4791). La app muestra la marca VERIFICAR |

**Progreso** (`localStorage`, clave `normas`): `normas["n-C127-e"]` (escribir) y `normas["n-C127-i"]` (¿qué determina?) y `normas["n-C127-f"]` (foto, solo las que tienen `figura`). Cada registro es un registro de SRS más `bien`, `conf` (`{ "C128": 3 }`: veces que la confundió con esa norma; `"otra"` si escribió un número fuera de la lista) y, solo en `-e`, `dias` (días en que la escribió bien).

---

## Qué revisa `tools/validar_json.py`

- JSON bien formado e ids únicos en tarjetas, preguntas y glosario.
- Campos obligatorios y valores permitidos de `tipo`, `clave` y `origen`.
- Cada referencia: `doc` existe en `fuentes.json` y `pag` está entre 1 y `paginas`.
- Figuras (también las de normas): el archivo existe y tiene `alt` y `fuente`.
- Selección única y F/V: exactamente una `correcta` válida; selección múltiple: lista no vacía de ids válidos.
- Respuesta corta: `respuesta_modelo` y de 1 a 5 `puntos_clave` (2 a 5 si es de teoría).
- Las preguntas de examen traen `examen.pregunta` y `examen.periodo`.
- Avisa (sin fallar) de las claves `pendiente`.
- Normas: `designacion` = «ASTM » + `id`, familia existente, `mide`, `gancho` y `fuente` presentes, fuentes con página válida, `confunde_con` apunta a normas existentes y `mide` no nombra ninguna norma.

No revisa: `origen` de tarjetas, `tema`/`subtema` del glosario, que `subtema` exista en `indice.json` ni el formato de los ids.
