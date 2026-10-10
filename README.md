# Materiales IC-0604 · I examen

Herramienta de estudio para la teoría del I examen de **IC-0604 Materiales de Construcción** (UCR, II ciclo 2026, sábado 17 de octubre de 2026). Cubre los temas 1, 2 y 3: introducción, agua para concreto y agregados.

**Desarrollado por Adrián Castro Ramírez**, estudiante de Ingeniería Civil de la UCR.

> El contenido se basa en el material del curso IC-0604. Los ítems marcados «⚠ Verificar» deben confirmarse con el profesor. Para reportar un error, usá el botón «Reportar un error» de cada tarjeta o pregunta.

## Qué tiene

- **Estudiar:** tarjetas que se voltean al tocarlas y se califican (la sabía, dudosa, no la sabía).
- **Practicar:** preguntas de selección única, selección múltiple, falso o verdadero y respuesta corta, con la explicación y la fuente de cada una.
- **Opciones en orden aleatorio:** en selección única y múltiple, las opciones cambian de lugar cada vez que sale la pregunta, así que la respuesta no cae siempre en la misma letra.
  - Las letras se siguen viendo A, B, C… en orden.
  - Las explicaciones se ajustan para citar la letra que ves: si la correcta quedó en la C, dice «Correcta la C».
  - Falso o verdadero queda fijo (Verdadero, Falso), y «Ninguna de las anteriores» no se mueve de su lugar.
  - En el Simulacro, el orden se sortea al empezar y se mantiene si recargás.
  - En Buscar, las opciones aparecen en el orden original.
- Funciona sin conexión (PWA) y guarda el progreso en el navegador.
- **Simulacro:** examen cronometrado con la estructura del I examen del curso.
- **Progreso:** cuenta regresiva, lo pendiente, racha, tiempo por día, dominio por tema y subtema, y tus datos (exportar, importar y borrar).
- **Buscar:** búsqueda sin conexión, glosario alfabético, galería de figuras y lista de ítems «⚠ Verificar» para consultar con el profe.

## Repetición espaciada: cuándo vuelve a salir un ítem

Estudiar y Practicar arrancan en **«Repaso de hoy»**. La otra opción, **«Por tema»**, usa los filtros y también cuenta para el repaso. El algoritmo está en `js/srs.js` y es un **Leitner de 5 cajas**:

| Caja | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Vuelve en | hoy mismo | 1 día | 2 días | 4 días | 7 días |

**Cómo se mueve un ítem entre cajas**

- **La sabía / Bien:** sube una caja. Si es la primera vez que sale, entra directo a la caja 2, porque ya lo dominabas.
- **Dudosa / Parcial:** baja una caja, pero nunca a menos de la caja 1.
- **No la sabía / Mal:** va a la caja 0, queda como **fallado** y vuelve en la misma sesión, 4 lugares después.
- **Ítems marcados «⚠ Verificar»:** nunca pasan de la caja 2, así que vuelven cada 2 días o antes. Siempre muestran su aviso y el resumen del día dice cuántos hay.

**Compresión antes del examen**

La fecha del examen (17 de octubre de 2026) se lee de `data/indice.json`.

- **Día de repaso final.** A cada ítem le toca uno de los 3 días antes del examen: el 14, el 15 o el 16 de octubre. Se reparten en tercios según el id del ítem, y siempre es el mismo día para el mismo ítem.
- **Ningún intervalo se salta ese día.** Si el intervalo normal cae después, se acorta para que el ítem salga a más tardar en su día final.
- **Después del repaso final** vuelven los intervalos normales. Antes del examen, el ítem solo sale otra vez si lo fallás (vuelve hoy mismo) o si queda dudoso (vuelve al día siguiente, si todavía no es la víspera).
- **Nuevos por día.** Los ítems que nunca has visto se reparten entre los días que quedan **hasta el 13 de octubre**. Así los 3 días finales quedan solo para repasar. Si ya estás en esos días, se reparten hasta la víspera.

**Orden del «Repaso de hoy»:** primero lo fallado, luego lo vencido (lo más atrasado primero) y al final los nuevos del día. Al terminar podés «Seguir con nuevas» o «Adelantar repaso».

**Ejemplo:** una tarjeta cuyo día final es el 15 de octubre.

| Fecha | Calificación | Caja | Vuelve el | Por qué |
|---|---|---|---|---|
| vie 9 | La sabía (primera vez) | 2 | dom 11 | 2 días |
| dom 11 | La sabía | 3 | jue 15 | 4 días, que coinciden con su día final |
| jue 15 | Dudosa | 2 | vie 16 | en la recta final, lo dudoso vuelve mañana |
| vie 16 | La sabía | 3 | mar 20 | ya tuvo su repaso final: intervalo normal |

**Cuánto trabajo da.** Las pruebas simulan estudiar del 9 al 16 de octubre con los datos reales, acertando más o menos el 70 %. Con esa simulación salen entre 34 y 98 tarjetas y entre 42 y 139 preguntas por día; la carga sube en los últimos días. Todo se ve antes del 13 y todo se repasa al menos una vez entre el 14 y el 16.

## Simulacro

**Estructura.** Imita el I examen de I-2025 (25 min, 40 puntos), que es el modelo más completo del banco:

| Duración | Selección única (1 pt) | Falso o verdadero (2 pts) | Respuesta corta (2 pts) | Total |
|---|---|---|---|---|
| 25 min | 6 | 5 | 12 | 40 pts |
| 40 min | 10 | 8 | 18 | 62 pts |
| 60 min | 14 | 12 | 26 | 90 pts |

- Se pueden elegir los temas. Si con los temas elegidos no alcanzan las preguntas, se usan las que haya y se avisa.
- Las preguntas se sacan al azar entre las de examen y las de teoría. La selección múltiple queda fuera, porque los exámenes no la usan.
- **Sin repetidos:** se deduplica por enunciado (sin tildes, mayúsculas, puntuación ni «(N puntos)») más la figura. Así, las 5 preguntas de «Normativa» del I-2026, que tienen el mismo texto pero distinta foto, cuentan como distintas. Entre duplicadas queda la de clave oficial más reciente.

**Puntaje**

- **Selección única:** 1 punto.
- **Falso o verdadero, caso verdadero:** 2 puntos si lo marcás V.
- **Falso o verdadero, caso falso:** 1 punto por marcarlo F y 1 por la justificación. La justificación la autoevaluás contra la justificación de la clave, o contra la explicación si la clave no la trae.
- **Respuesta corta:** marcás qué puntos clave cubriste. Puntos = 2 × cubiertos / total, redondeado a 0,5.
- **Nota:** porcentaje sobre 100, con el desglose por parte.

**Durante el examen no hay retroalimentación.** Al terminar:
1. Autoevaluás las justificaciones y las respuestas cortas.
2. Ves la nota, el tiempo usado y la revisión pregunta por pregunta, con la explicación y la fuente.
3. Podés tocar «Mandar N fallos a Repaso de hoy»: las preguntas sin el puntaje completo quedan como falladas en Practicar.

**Temporizador.** Se guarda la hora de fin y lo que queda se calcula como `fin − ahora`. Por eso sigue corriendo aunque el teléfono bloquee la pantalla o se recargue la página: el examen en curso y las respuestas quedan en el navegador. Si al volver ya se acabó el tiempo, el examen se cierra solo con lo que alcanzaste a responder. Si el navegador no permite guardar datos, aguanta el bloqueo de pantalla pero no una recarga.

## Progreso

- **Cuenta regresiva** al I examen (sábado 17 de octubre, 8:00 a. m.) y **pendientes de hoy** (lo que trae el «Repaso de hoy» de tarjetas y preguntas), más lo que todavía no has visto.
- **Racha:** días seguidos con al menos un ítem calificado. Si hoy todavía no estudiaste, cuenta hasta ayer.
- **Tiempo de estudio:** barras de los últimos 7 días con la línea de la meta.
- **Dominio** por tema y subtema: porcentaje de ítems cuya última calificación fue «la sabía» o «bien». Lo que nunca viste cuenta como no sabido. En las preguntas también se muestra el **porcentaje de aciertos** (respuestas «bien» entre todos los intentos).
- **Para reforzar:** los 3 subtemas con menor dominio. Cada uno trae un botón que abre Practicar con ese subtema ya filtrado.
- **Gráficos accesibles:** son SVG y CSS propios, sin librerías. Cada valor también está escrito en texto, y el tiempo por día tiene una lista para lectores de pantalla.

**Tus datos.** El progreso vive solo en el navegador donde estudiás.

- **Exportar** descarga `progreso-materiales-AAAA-MM-DD.json`.
- **Importar** valida el archivo, muestra qué trae y te deja elegir entre dos opciones:
  - **Combinar** (recomendado): de cada ítem queda el registro más reciente; de cada día, el mayor tiempo. Los ajustes de este teléfono se conservan.
  - **Reemplazar:** borra lo de este teléfono y deja solo lo del archivo.
- **Borrar mi progreso** pide confirmación y borra tarjetas, preguntas, tiempo, racha y simulacros. La meta y los filtros se conservan.

## Buscar

Tiene cuatro pestañas; la app recuerda la última que usaste.

- **Buscar:**
  - Busca en tarjetas (frente y reverso), preguntas (enunciado, opciones, respuesta modelo, puntos clave y explicación) y glosario.
  - No distingue tildes ni mayúsculas: «hormigon» encuentra «hormigón».
  - Con varias palabras, el ítem tiene que contenerlas todas. Busca desde 2 letras.
  - Primero salen las coincidencias en el título. Los resultados se agrupan por tipo (glosario, tarjetas, preguntas) y por tema, y lo encontrado se resalta.
  - Al tocar un resultado se despliega la respuesta con su fuente, y se puede abrir en Estudiar o en Practicar.
- **Glosario:** los 60 términos en orden alfabético español («Á» va con la A), con un índice de letras, su definición, su subtema y su fuente.
- **Figuras:** las 15 imágenes de `img/ensayos` e `img/examenes`, con su texto alternativo y su fuente. Al tocar una, se abren en Estudiar o en Practicar los ítems que la usan.
- **Verificar:** los 33 ítems marcados «⚠ Verificar» (10 tarjetas y 23 preguntas), agrupados por tipo y tema, con la duda y la fuente.
  - «Copiar lista para el profe» copia un texto listo para pegar en un correo o mensaje. Si el navegador no deja copiar, lo muestra para copiarlo a mano.
  - También se pueden repasar esas tarjetas o practicar esas preguntas.

## Meta diaria

Arriba de Estudiar y Practicar hay un contador: «Hoy: 23 / 40 min · 31 ítems». Al tocarlo se cambia la meta.

- Se puede medir en minutos (40 por defecto) o en ítems (53 ítems ≈ 40 min, a unos 45 s por ítem).
- Si el repaso del día trae más de lo que cabe en la meta, el orden prioriza lo fallado y lo vencido; lo que quede pasa al día siguiente.
- El tiempo cuenta desde que aparece un ítem hasta que lo calificás, con un tope de 3 minutos por ítem para no contar ratos en que dejaste la app abierta.

## Estructura

```
index.html            página única
css/app.css           estilos (mobile first, modo oscuro automático)
js/version.js         versión de la app y del caché (cambiar en cada publicación)
js/opciones.js        orden aleatorio de opciones y ajuste de letras en las explicaciones
js/srs.js             repetición espaciada (Leitner) y compresión antes del examen
js/examen.js          simulacro: armar, deduplicar, puntuar y temporizador
js/simulacro.js       pantallas del simulacro
js/progreso.js        progreso: dominio, débiles, racha, tiempo y exportar/importar
js/pantalla-progreso.js  pantalla de progreso
js/buscar.js          búsqueda sin tildes, resaltado, glosario, figuras y verificar
js/pantalla-buscar.js pantalla de búsqueda
js/                   store, datos, ui, estudiar, practicar, app
sw.js                 service worker (precarga para uso sin conexión)
data/                 contenido en JSON (esquema en docs/ESQUEMA.md)
img/                  figuras de ensayos y de exámenes
tools/                validador de JSON, generador de contenido e íconos
tests/                servidor local y pruebas con Playwright
```

## Probar en la computadora

```bash
python tests/servidor.py
```

Luego abrí <http://localhost:8000/pryecto_materiales/>. El servidor imita GitHub Pages: sirve el sitio bajo `/pryecto_materiales/`, así que si una ruta no es relativa, falla.

## Pruebas

Requiere Python 3 y Playwright (`pip install playwright` y `python -m playwright install chromium`).

```bash
python tools/validar_json.py .
node --test tests/srs.test.js tests/examen.test.js tests/progreso.test.js tests/buscar.test.js tests/opciones.test.js
python tests/test_app.py
python tests/capturas.py
```

`srs.test.js` prueba el repaso con fechas simuladas, `examen.test.js` prueba el simulacro (puntaje, deduplicación y temporizador con reloj simulado) , `progreso.test.js` prueba el dominio, la racha y el exportar/importar, , `buscar.test.js` prueba la búsqueda, el resaltado, el glosario y los índices, y `opciones.test.js` prueba el orden aleatorio y el ajuste de letras con las 72 preguntas reales. Ninguno necesita dependencias, solo Node. Las pruebas de la app fijan la fecha en el 9 de octubre de 2026 con `window.__fechaPrueba`.

`capturas.py` guarda capturas a 390×844 en modo claro y oscuro en `tests/capturas/` (esa carpeta no se sube).

## Publicar una versión nueva

1. Cambiá `APP_VERSION` (y `APP_FECHA`) en `js/version.js`, por ejemplo `"2026-10-10.1"`.
2. Corré el validador y las pruebas.
3. Hacé commit y push a `main`. GitHub Pages publica la carpeta raíz.

Al abrir la app, el navegador detecta el `version.js` nuevo, descarga todo en un caché nuevo y muestra «Hay una versión nueva · Actualizar». Al tocar «Actualizar», se borra el caché viejo.

## Auditoría del contenido

El 9 de octubre de 2026 se auditaron todas las tarjetas, preguntas y términos contra las fuentes del curso. El informe está en [`docs/AUDITORIA-2026-10-09.md`](docs/AUDITORIA-2026-10-09.md). Las correcciones están en `tools/contenido/correcciones.json`, y cada una guarda el texto anterior, la razón y la evidencia.

## Privacidad

La carpeta `fuentes/` (material con derechos de autor y exámenes con nombres de estudiantes) nunca se sube al repositorio. El sitio lleva `noindex, nofollow` para que los buscadores no lo indexen.
