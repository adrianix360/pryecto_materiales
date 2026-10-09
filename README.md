# Materiales IC-0604 · I examen

Herramienta de estudio para la teoría del I examen de **IC-0604 Materiales de Construcción** (UCR, II ciclo 2026, sábado 17 de octubre de 2026). Cubre los temas 1, 2 y 3: introducción, agua para concreto y agregados.

**Desarrollado por Adrián Castro Ramírez**, estudiante de Ingeniería Civil de la UCR.

> El contenido se basa en el material del curso IC-0604. Los ítems marcados «⚠ Verificar» deben confirmarse con el profesor. Para reportar un error, usá el botón «Reportar un error» de cada tarjeta o pregunta.

## Qué tiene

- **Estudiar:** tarjetas que se voltean al tocarlas y se califican (la sabía, dudosa, no la sabía).
- **Practicar:** preguntas de selección única, selección múltiple, falso o verdadero y respuesta corta, con la explicación y la fuente de cada una.
- Funciona sin conexión (PWA) y guarda el progreso en el navegador.
- Simulacro, Progreso y Buscar: próximamente.

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

## Meta diaria

Arriba de Estudiar y Practicar hay un contador: «Hoy: 23 / 90 min · 31 ítems». Al tocarlo se cambia la meta.

- Se puede medir en minutos (90 por defecto) o en ítems (120 ítems ≈ 90 min, a unos 45 s por ítem).
- El tiempo cuenta desde que aparece un ítem hasta que lo calificás, con un tope de 3 minutos por ítem para no contar ratos en que dejaste la app abierta.

## Estructura

```
index.html            página única
css/app.css           estilos (mobile first, modo oscuro automático)
js/version.js         versión de la app y del caché (cambiar en cada publicación)
js/srs.js             repetición espaciada (Leitner) y compresión antes del examen
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
node --test tests/srs.test.js
python tests/test_app.py
python tests/capturas.py
```

`srs.test.js` prueba el algoritmo con fechas simuladas y no necesita dependencias, solo Node. Las pruebas de la app fijan la fecha en el 9 de octubre de 2026 con `window.__fechaPrueba`.

`capturas.py` guarda capturas a 390×844 en modo claro y oscuro en `tests/capturas/` (esa carpeta no se sube).

## Publicar una versión nueva

1. Cambiá `APP_VERSION` (y `APP_FECHA`) en `js/version.js`, por ejemplo `"2026-10-10.1"`.
2. Corré el validador y las pruebas.
3. Hacé commit y push a `main`. GitHub Pages publica la carpeta raíz.

Al abrir la app, el navegador detecta el `version.js` nuevo, descarga todo en un caché nuevo y muestra «Hay una versión nueva · Actualizar». Al tocar «Actualizar», se borra el caché viejo.

## Privacidad

La carpeta `fuentes/` (material con derechos de autor y exámenes con nombres de estudiantes) nunca se sube al repositorio. El sitio lleva `noindex, nofollow` para que los buscadores no lo indexen.
