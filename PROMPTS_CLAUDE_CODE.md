# Prompts para Claude Code — Herramienta de estudio IC-0604 (I examen)

**Cómo usarlos**
- Abrí una terminal **en la carpeta del proyecto** (`Documentos\Materiales de la construcción`) y corré `claude`. Claude Code lee `CLAUDE.md` solo.
- Pegá **un prompt a la vez**, en orden. Cada uno pide un plan antes de programar: revisalo, respondé «OK» y esperá el reporte antes de pasar al siguiente.
- Los reportes de errores llegan por correo a castroramirez702@gmail.com (ya está puesto en el prompt 1).
- El contenido ya está hecho: `data/` (152 tarjetas, 190 preguntas y 60 términos de glosario), `img/`, `ALCANCE.md` e `INVENTARIO.md`. Los prompts **no deben modificar el contenido**, solo mostrarlo.

---

## Prompt 0 · Preparar el repositorio

```text
Leé CLAUDE.md, ALCANCE.md, INVENTARIO.md (secciones 6 y 7), data/indice.json, data/fuentes.json y tools/validar_json.py. Todavía no programes la app.

Hacé lo siguiente y reportá:
1. Verificá qué tengo instalado: git, gh (GitHub CLI), node/npm y python (en Windows puede llamarse "py" o "python"). Si falta algo, decime cómo instalarlo; no lo instales sin preguntarme.
2. Inicializá git (rama main). Revisá que .gitignore excluya fuentes/ (tiene material con derechos de autor y exámenes con nombres de estudiantes) y agregá node_modules/, tests/capturas/ y los archivos del sistema.
3. Corré "python tools/validar_json.py ." y confirmá que dé OK.
4. Resumime el esquema real de data/ (campos de tarjetas, preguntas, glosario, fuentes e índice) en un archivo docs/ESQUEMA.md. Hacelo leyendo los JSON, sin inventar campos.
5. Primer commit: "Contenido inicial: temas 1-3, glosario, figuras y validador".
```

---

## Prompt 1 · App base (pantallas, PWA y créditos)

```text
Presentá primero un plan de pantallas y archivos (máximo una página) y esperá mi OK. Luego construí la app base, mobile first, con HTML, CSS y JavaScript puros (sin frameworks, sin CDN) y rutas relativas, como pide CLAUDE.md.

Contenido: se lee de data/indice.json, data/tarjetas/temaN.json, data/preguntas/temaN.json, data/glosario.json y data/fuentes.json, según docs/ESQUEMA.md. No modifiques nada en data/.

Pantallas y comportamiento:
- Navegación inferior con 5 secciones: Estudiar, Practicar, Simulacro, Progreso, Buscar. Las de Simulacro, Progreso y Buscar pueden quedar como «próximamente» en este paso.
- Estudiar: tarjetas que se voltean al tocar, con tres botones al calificar (la sabía, dudosa, no la sabía). Filtro por tema y subtema. Si la tarjeta trae "figura", mostrala con su texto alternativo y su fuente.
- Practicar: preguntas de selección única, selección múltiple y verdadero/falso con retroalimentación inmediata y la explicación. En respuesta corta, el estudiante escribe, después ve la respuesta_modelo y los puntos_clave y se autocalifica. Filtro por tema, subtema y origen (examen o teoría).
- En cada ítem mostrá la fuente legible: título del documento (de fuentes.json) y página, más la impresa si existe. En preguntas de examen, mostrá también el examen y el periodo (por ejemplo «Examen I-2025, pregunta 3»). Si el ítem trae "verificar", mostrá un aviso visible «⚠ Verificar con el profe» con ese texto. Si trae "justificacion_oficial", mostrala como «Justificación de la clave».
- Modo oscuro automático (prefers-color-scheme), tipografía grande (17 px como mínimo), botones de 48 px como mínimo, uso cómodo con una mano (acciones principales abajo) y accesible (etiquetas aria, foco visible, contraste).
- store.js para guardar el progreso en localStorage, con todo envuelto en try/catch: si el navegador lo bloquea, la app sigue funcionando sin guardar y muestra un aviso discreto. Guardá las respuestas por id de ítem.
- PWA: manifest.webmanifest e íconos, y service worker para uso sin conexión que precargue index, css, js, data e img. Poné la versión del caché en una sola constante y explicame cómo subirla en cada publicación.
- Etiqueta <meta name="robots" content="noindex, nofollow"> y un robots.txt que bloquee todo.
- Créditos: un pie de página visible en todas las pantallas con «Desarrollado por Adrián Castro Ramírez». Una pantalla «Acerca de» con su nombre, «estudiante de Ingeniería Civil de la UCR», la fecha de la versión y el aviso de que el contenido se basa en el material del curso IC-0604 y que los ítems marcados «Verificar» deben confirmarse con el profesor. El mismo crédito en README.md y en <meta name="author">.
- Botón «Reportar un error», en Acerca de y dentro de cada tarjeta y pregunta. Debe abrir un correo (enlace mailto:) a castroramirez702@gmail.com con el asunto «Error en la herramienta IC-0604» y, en el cuerpo, el id del ítem, la versión de la app y un espacio para describir el error. Codificá bien el asunto y el cuerpo para que funcione en Android y iPhone.

Pruebas:
- Agregá pruebas automáticas (por ejemplo, Node con Playwright si está instalado; si no, decime qué instalar) que carguen la app, recorran las 5 secciones, volteen una tarjeta, respondan una pregunta de cada tipo y verifiquen que el progreso se guarda y que la app no se rompe con localStorage bloqueado.
- Probá con un navegador automatizado a 390×844 px, en modo claro y oscuro, recorriendo cada pantalla. Guardá las capturas en tests/capturas/ (no se suben a git) y mostrámelas.
- Corré también "python tools/validar_json.py .".

Al final: commits pequeños con mensajes claros en español, reporte de lo hecho y de las dudas, y los comandos exactos para crear el repositorio con gh y publicar en GitHub Pages (rama main, carpeta raíz). Antes de dar esos comandos, preguntame el nombre del repositorio.
```

---

## Prompt 2 · Repetición espaciada

```text
Presentá primero un plan breve y esperá mi OK.

Agregá repetición espaciada a Estudiar y Practicar usando las calificaciones que ya se guardan (la sabía / dudosa / no la sabía, y acierto o error en preguntas):
- Un algoritmo simple y documentado (tipo Leitner o SM-2 simplificado). Explicame en el README cómo decide cuándo vuelve a salir un ítem.
- Un modo «Repaso de hoy» que muestre primero lo vencido y lo fallado. Calculá las fechas pensando que el examen es el sábado 17 de octubre de 2026 (está en data/indice.json): en los últimos días, comprimí los intervalos para que todo se repase al menos una vez.
- Una meta diaria configurable, que empiece en 90 minutos o en un número de ítems equivalente, con un contador visible.
- Que los ítems marcados "verificar" no se pierdan en el repaso, pero que conserven su aviso.
Pruebas automáticas del algoritmo (con fechas simuladas), validación de JSON, capturas a 390×844 y commits pequeños.
```

---

## Prompt 3 · Simulacro cronometrado

```text
Presentá primero un plan breve y esperá mi OK.

Construí la sección Simulacro:
- Un examen cronometrado que imite la estructura de los exámenes reales del curso (INVENTARIO.md, secciones 3 y 7): una parte de selección única, una de falso/verdadero con justificación de los falsos y una de respuesta corta. Que se pueda elegir la duración (25, 40 o 60 min) y los temas.
- Puntaje como en los exámenes: en falso/verdadero, 2 puntos si acierta un verdadero; si el caso es falso, 1 punto por marcarlo y 1 por la justificación (autoevaluada contra la justificacion_oficial). En respuesta corta, autoevaluación con los puntos_clave.
- No mostrar retroalimentación hasta terminar. Al final: nota, tiempo usado, revisión pregunta por pregunta con la explicación y la fuente, y la opción de mandar los fallos a «Repaso de hoy».
- Mezclá preguntas de examen y de teoría, sin repetir el mismo enunciado (hay preguntas de examen repetidas entre años: deduplicá por texto del enunciado).
- Que el temporizador sobreviva si el teléfono bloquea la pantalla o se recarga la página.
Pruebas (puntaje, deduplicación y temporizador con reloj simulado), capturas a 390×844 y commits.
```

---

## Prompt 4 · Progreso

```text
Presentá primero un plan breve y esperá mi OK.

Construí la sección Progreso:
- Dominio por tema y subtema (porcentaje de ítems «sabidos» y de aciertos), los subtemas más débiles primero, racha de días y tiempo de estudio por día.
- Cuenta regresiva al examen (17 de octubre de 2026) y lo pendiente de repasar.
- Gráficos hechos con SVG o CSS propios (sin librerías externas), legibles en modo oscuro y accesibles (con el valor también en texto).
- Exportar e importar el progreso como un archivo JSON, para pasarlo de un teléfono a otro, y un botón «Borrar mi progreso» con confirmación.
Pruebas, capturas a 390×844 y commits.
```

---

## Prompt 5 · Buscar, glosario e imágenes

```text
Presentá primero un plan breve y esperá mi OK.

Construí la sección Buscar:
- Búsqueda sin conexión en tarjetas, preguntas y glosario, sin distinguir tildes ni mayúsculas, con resultados agrupados por tipo y por tema.
- Glosario alfabético con definición y fuente.
- Galería de figuras (img/ensayos e img/examenes) con su texto alternativo y fuente; al tocar una, que abra las tarjetas o preguntas que la usan.
- Filtro rápido «Ítems a verificar con el profe», que liste todo lo marcado "verificar" para que yo lo consulte.
Pruebas, capturas a 390×844 y commits.
```

---

## Prompt 6 · Revisión final y publicación

```text
Hacé una revisión final antes de publicar y reportame:
1. "python tools/validar_json.py ." y todas las pruebas automáticas en verde.
2. Una auditoría a 390×844 en claro y oscuro: tamaños de letra y de botones, contraste, foco con teclado, textos alternativos y que todo funcione sin conexión (cargar, activar el modo avión en el navegador automatizado y navegar).
3. Que no se suba nada de fuentes/ y que ninguna página muestre nombres de estudiantes.
4. Que el noindex, el robots.txt, los créditos (pie de página, Acerca de, README y meta author) y el botón «Reportar un error» estén bien.
5. Que la versión del caché del service worker y la fecha de la versión en Acerca de estén actualizadas.
Corregí lo que falle con commits pequeños, mostrame las capturas finales y dame los comandos para publicar o actualizar GitHub Pages. Después de publicar, verificá que la URL pública cargue con rutas relativas (el sitio se sirve desde /nombre-del-repo/).
```

---

## Prompt 7 · Cuando corrija contenido (usar cuando haga falta)

```text
Corregí el contenido así: [describí la corrección, por ejemplo «en la pregunta p2-2B-x23 la respuesta es contracción autógena, lo confirmó el profe»].
Reglas: el contenido se edita en tools/contenido/*.py (no a mano en data/), y después se regenera con "python tools/contenido/construir.py ." y se valida con "python tools/validar_json.py .". Si la corrección resuelve un ítem marcado "verificar", quitá esa marca y anotá la decisión en ALCANCE.md (sección 7). Subí la versión del caché del service worker, hacé commit y dame el comando para publicar.
```
