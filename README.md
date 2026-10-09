# Materiales IC-0604 · I examen

Herramienta de estudio para la teoría del I examen de **IC-0604 Materiales de Construcción** (UCR, II ciclo 2026, sábado 17 de octubre de 2026). Cubre los temas 1, 2 y 3: introducción, agua para concreto y agregados.

**Desarrollado por Adrián Castro Ramírez**, estudiante de Ingeniería Civil de la UCR.

> El contenido se basa en el material del curso IC-0604. Los ítems marcados «⚠ Verificar» deben confirmarse con el profesor. Para reportar un error, usá el botón «Reportar un error» de cada tarjeta o pregunta.

## Qué tiene

- **Estudiar:** tarjetas que se voltean al tocarlas y se califican (la sabía, dudosa, no la sabía).
- **Practicar:** preguntas de selección única, selección múltiple, falso o verdadero y respuesta corta, con la explicación y la fuente de cada una.
- Funciona sin conexión (PWA) y guarda el progreso en el navegador.
- Simulacro, Progreso y Buscar: próximamente.

## Estructura

```
index.html            página única
css/app.css           estilos (mobile first, modo oscuro automático)
js/version.js         versión de la app y del caché (cambiar en cada publicación)
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
python tests/test_app.py
python tests/capturas.py
```

`capturas.py` guarda capturas a 390×844 en modo claro y oscuro en `tests/capturas/` (esa carpeta no se sube).

## Publicar una versión nueva

1. Cambiá `APP_VERSION` (y `APP_FECHA`) en `js/version.js`, por ejemplo `"2026-10-10.1"`.
2. Corré el validador y las pruebas.
3. Hacé commit y push a `main`. GitHub Pages publica la carpeta raíz.

Al abrir la app, el navegador detecta el `version.js` nuevo, descarga todo en un caché nuevo y muestra «Hay una versión nueva · Actualizar». Al tocar «Actualizar», se borra el caché viejo.

## Privacidad

La carpeta `fuentes/` (material con derechos de autor y exámenes con nombres de estudiantes) nunca se sube al repositorio. El sitio lleva `noindex, nofollow` para que los buscadores no lo indexen.
