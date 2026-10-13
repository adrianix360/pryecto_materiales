#!/usr/bin/env python3
"""Pruebas de la app con Playwright (Python) y Chromium, a 390×844.

Uso: python tests/test_app.py
Requiere: pip install playwright && python -m playwright install chromium
Sale con código 1 si alguna prueba falla.
"""
import json
import os
import re
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import expect, sync_playwright  # noqa: E402

import servidor  # noqa: E402

VIEWPORT = {"width": 390, "height": 844}
CLAVE = "pryecto_materiales:progreso:v1"
SECCIONES = [("estudiar", "Estudiar"), ("practicar", "Practicar"), ("normas", "Normas"), ("simulacro", "Simulacro"),
             ("progreso", "Progreso"), ("buscar", "Buscar")]  # Buscar está en la barra superior; el resto, abajo

BLOQUEAR_LS = """
(() => {
  const falla = () => { throw new DOMException('bloqueado', 'SecurityError'); };
  Object.defineProperty(window, 'localStorage', { configurable: true, get: falla });
})();
"""

FECHA = "2026-10-09"  # todas las pruebas corren con esta fecha simulada

resultados = []


def prueba(fn):
    resultados.append(fn)
    return fn


def nueva_pagina(nav, url, bloquear=False, sw=False, fecha=FECHA, sembrar=None):
    """Abre la app con la fecha simulada. sembrar: progreso guardado antes de cargar."""
    ctx = nav.new_context(viewport=VIEWPORT, service_workers="allow" if sw else "block")
    ctx.add_init_script(f"window.__fechaPrueba = {json.dumps(fecha)};")
    if sembrar is not None:
        ctx.add_init_script(
            "try { if (!sessionStorage.getItem('sembrado')) {"
            f" localStorage.setItem({json.dumps(CLAVE)}, {json.dumps(json.dumps(sembrar))});"
            " sessionStorage.setItem('sembrado', '1'); } } catch (e) {}")
    if bloquear:
        ctx.add_init_script(BLOQUEAR_LS)
    pag = ctx.new_page()
    errores = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.goto(url)
    pag.wait_for_selector("body[data-listo='1']")
    return ctx, pag, errores


def por_tema(pag):
    """Pasa la sección actual al modo «Por tema» y abre los filtros."""
    pag.locator('[data-modo="tema"]').click()
    expect(pag.locator('[data-modo="tema"]')).to_have_attribute("aria-pressed", "true")
    pag.locator("details.filtros:not([data-panel]) summary").click()


def progreso(pag):
    crudo = pag.evaluate(f"localStorage.getItem({json.dumps(CLAVE)})")
    return json.loads(crudo) if crudo else {"tarjetas": {}, "preguntas": {}}


def revisar_pantalla(pag, nombre):
    """Reglas comunes: sin scroll horizontal, texto ≥ 17 px, controles ≥ 48 px, pie visible."""
    ancho = pag.evaluate("document.documentElement.scrollWidth")
    assert ancho <= VIEWPORT["width"], f"{nombre}: scroll horizontal ({ancho}px)"
    chicos = pag.evaluate("""() => {
      const malos = [];
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) {
        const n = w.currentNode, el = n.parentElement;
        if (!n.textContent.trim() || !el || el.closest('.solo-lector, .saltar, [hidden]')) continue;
        if (!el.getClientRects().length) continue;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs < 17) malos.push(fs.toFixed(1) + 'px: ' + n.textContent.trim().slice(0, 30));
      }
      return malos;
    }""")
    assert not chicos, f"{nombre}: texto menor a 17 px: {chicos[:5]}"
    bajos = pag.evaluate("""() => [...document.querySelectorAll('button, a.btn, select, .nav__item, .barra__acerca, .barra__buscar, summary')]
      .filter(e => e.getClientRects().length)
      .map(e => [e.getBoundingClientRect().height, e.textContent.trim().slice(0, 25)])
      .filter(([h]) => h < 47.5)""")
    assert not bajos, f"{nombre}: controles de menos de 48 px: {bajos[:5]}"
    alto_barra = pag.evaluate("document.querySelector('header.barra').getBoundingClientRect().height")
    assert alto_barra < 70, f"{nombre}: el encabezado se deformó ({alto_barra}px)"
    pie = pag.locator("footer.pie")
    assert pie.inner_text().strip() == "Desarrollado por Adrián Castro Ramírez", f"{nombre}: pie distinto"


@prueba
def recorre_las_seis_secciones_y_acerca(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url)
    assert pag.locator('meta[name="robots"]').get_attribute("content") == "noindex, nofollow"
    assert pag.locator('meta[name="author"]').get_attribute("content") == "Adrián Castro Ramírez"
    for ruta, nombre in SECCIONES:
        pag.locator(f'[data-ruta="{ruta}"]').click()
        expect(pag.locator("#titulo")).to_have_text(nombre)
        expect(pag.locator(f'[data-ruta="{ruta}"]')).to_have_attribute("aria-current", "page")
        assert pag.locator("#vista").inner_text().strip(), f"{ruta} vacía"
        revisar_pantalla(pag, ruta)
    pag.locator(".barra__acerca").click()
    expect(pag.locator("#titulo")).to_have_text("Acerca de")
    texto = pag.locator("#vista").inner_text()
    for esperado in ("Adrián Castro Ramírez", "Estudiante de Ingeniería Civil de la UCR",
                     pag.evaluate("self.APP_VERSION"), pag.evaluate("self.APP_FECHA"),
                     "IC-0604", "deben confirmarse con el profesor"):
        assert esperado in texto, f"Acerca de no dice «{esperado}»"
    href = pag.locator("#vista .reportar a").get_attribute("href")
    assert href.startswith("mailto:castroramirez702@gmail.com?"), href
    revisar_pantalla(pag, "acerca")
    assert not errores, errores
    ctx.close()


@prueba
def voltea_y_califica_una_tarjeta(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/estudiar")
    tarjeta = pag.locator(".tarjeta")
    assert tarjeta.get_attribute("aria-expanded") == "false"
    assert pag.locator(".tarjeta__reverso").count() == 0
    tarjeta.click()
    assert pag.locator(".tarjeta").get_attribute("aria-expanded") == "true"
    assert pag.locator(".tarjeta__reverso").is_visible()
    assert pag.locator(".fuentes").is_visible(), "la tarjeta volteada no muestra la fuente"
    id_ = pag.evaluate("document.querySelector('.tarjeta').getAttribute('aria-controls').replace('reverso-','')")
    href = pag.locator(".reportar a").get_attribute("href")
    assert id_ in href and pag.evaluate("encodeURIComponent(self.APP_VERSION)") in href, "reporte sin id o versión"
    revisar_pantalla(pag, "estudiar volteada")
    pag.get_by_role("button", name="La sabía", exact=True).click()
    assert progreso(pag)["tarjetas"][id_]["r"] == "sabia"
    pag.reload()
    pag.wait_for_selector("body[data-listo='1']")
    assert progreso(pag)["tarjetas"][id_]["r"] == "sabia", "el progreso no sobrevive a la recarga"
    assert not errores, errores
    ctx.close()


@prueba
def tarjeta_con_figura_y_verificar(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/estudiar")
    por_tema(pag)
    pag.select_option("#est-tema", "3")
    pag.select_option("#est-subtema", "3E")
    pag.locator(".tarjeta").click()
    fig = pag.locator(".figura img")
    assert fig.count() == 1, "la primera tarjeta de 3E debería traer figura"
    assert fig.get_attribute("alt"), "figura sin alt"
    assert pag.evaluate("document.querySelector('.figura img').complete && document.querySelector('.figura img').naturalWidth > 0")
    assert "Fuente" in pag.locator(".figura figcaption").inner_text()
    # una tarjeta con «verificar»
    objetivo = pag.evaluate("Datos.tarjetas.find(t => t.verificar && t.subtema === '3E').id")
    for _ in range(60):
        if pag.locator(".tarjeta").get_attribute("aria-controls") == "reverso-" + objetivo:
            break
        if pag.locator(".tarjeta").get_attribute("aria-expanded") == "false":
            pag.locator(".tarjeta").click()
        pag.get_by_role("button", name="La sabía", exact=True).click()
    else:
        raise AssertionError("no apareció la tarjeta con verificar")
    assert pag.locator(".chip--verificar").is_visible()
    pag.locator(".tarjeta").click()
    assert "⚠ Verificar con el profe" in pag.locator(".verificar").inner_text()
    assert not errores, errores
    ctx.close()


def responder(pag, tipo):
    if tipo in ("seleccion_unica", "verdadero_falso"):
        pag.locator("[data-opcion]").first.click()
    elif tipo == "seleccion_multiple":
        assert pag.get_by_role("button", name="Revisar").is_disabled()
        pag.locator("[data-opcion]").first.click()
        assert pag.locator("[data-opcion]").first.get_attribute("aria-checked") == "true"
        pag.get_by_role("button", name="Revisar").click()
    else:
        pag.fill("#respuesta", "Mi respuesta de prueba")
        pag.get_by_role("button", name="Ver respuesta").click()
        assert "Respuesta modelo" in pag.locator("#retro").inner_text()
        assert "Puntos clave" in pag.locator("#retro").inner_text()
        revisar_pantalla(pag, "respuesta corta vista")
        pag.get_by_role("button", name="Parcial").click()


@prueba
def responde_una_pregunta_de_cada_tipo(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/practicar")
    por_tema(pag)
    pendientes = {"seleccion_unica", "seleccion_multiple", "verdadero_falso", "respuesta_corta"}
    respondidas = {}
    for _ in range(250):
        if not pendientes:
            break
        sec = pag.locator(".pregunta")
        tipo, id_ = sec.get_attribute("data-tipo"), sec.get_attribute("data-id")
        if tipo in pendientes:
            responder(pag, tipo)
            retro = pag.locator("#retro")
            assert retro.is_visible(), f"{tipo}: sin retroalimentación"
            assert "Fuente" in retro.inner_text(), f"{tipo}: sin fuente"
            if tipo != "respuesta_corta":
                assert "Explicación" in retro.inner_text(), f"{tipo}: sin explicación"
                assert pag.locator(".opcion.es-correcta").count() >= 1
            revisar_pantalla(pag, f"practicar {tipo}")
            pendientes.discard(tipo)
            respondidas[id_] = tipo
            pag.get_by_role("button", name="Siguiente →").click()
        else:
            pag.get_by_role("button", name="Saltar").click()
    assert not pendientes, f"no se encontraron preguntas de tipo {pendientes}"
    guardado = progreso(pag)["preguntas"]
    for id_, tipo in respondidas.items():
        assert id_ in guardado, f"no se guardó {id_} ({tipo})"
        assert guardado[id_]["r"] in ("bien", "parcial", "mal")
    rc = [i for i, t in respondidas.items() if t == "respuesta_corta"][0]
    assert guardado[rc]["r"] == "parcial" and guardado[rc]["resp"] == "Mi respuesta de prueba"
    assert not errores, errores
    ctx.close()


@prueba
def pregunta_de_examen_muestra_examen_justificacion_y_verificar(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/practicar")
    objetivo = pag.evaluate("""Datos.preguntas.find(p => p.origen === 'examen' && p.justificacion_oficial
                                && p.verificar && p.tipo === 'verdadero_falso')""")
    assert objetivo, "no hay pregunta F/V de examen con justificación y verificar"
    por_tema(pag)
    pag.select_option("#pra-tema", str(objetivo["tema"]))
    pag.select_option("#pra-subtema", objetivo["subtema"])
    pag.select_option("#pra-origen", "examen")
    for _ in range(80):
        if pag.locator(".pregunta").get_attribute("data-id") == objetivo["id"]:
            break
        pag.get_by_role("button", name="Saltar").click()
    else:
        raise AssertionError("no apareció la pregunta objetivo")
    chip = pag.locator(".chip--examen").inner_text()
    assert chip.lower().startswith(("Examen " + objetivo["examen"]["periodo"].split(" ")[0]).lower()), chip
    pag.locator("[data-opcion]").first.click()
    retro = pag.locator("#retro").inner_text()
    assert "Justificación de la clave" in retro
    assert "⚠ Verificar con el profe" in retro
    assert "Examen" in pag.locator("#retro .fuentes").inner_text()
    assert not errores, errores
    ctx.close()


@prueba
def funciona_con_localstorage_bloqueado(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/estudiar", bloquear=True)
    aviso = pag.locator("#aviso-almacen")
    assert aviso.is_visible() and "no permite guardar" in aviso.inner_text()
    pag.locator(".tarjeta").click()
    pag.get_by_role("button", name="No la sabía", exact=True).click()
    assert pag.locator(".tarjeta").is_visible()
    pag.locator('.nav__item[data-ruta="practicar"]').click()
    expect(pag.locator(".pregunta")).to_be_visible()
    tipo = pag.locator(".pregunta").get_attribute("data-tipo")
    responder(pag, tipo)
    assert pag.locator("#retro").is_visible()
    pag.locator(".barra__acerca").click()
    expect(pag.locator("#titulo")).to_have_text("Acerca de")
    assert "no permite guardarlo" in pag.locator("#vista").inner_text()
    assert not errores, errores
    ctx.close()


@prueba
def funciona_sin_conexion(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url, sw=True)
    pag.evaluate("navigator.serviceWorker.ready.then(() => true)")
    pag.reload()
    pag.wait_for_selector("body[data-listo='1']")
    assert pag.evaluate("!!navigator.serviceWorker.controller"), "el SW no controla la página"
    caches = pag.evaluate("caches.keys()")
    assert caches == ["pryecto_materiales-" + pag.evaluate("self.APP_VERSION")], caches
    ctx.set_offline(True)
    pag.reload()
    pag.wait_for_selector("body[data-listo='1']")
    pag.locator('.nav__item[data-ruta="practicar"]').click()
    expect(pag.locator(".pregunta")).to_be_visible()
    figs = pag.evaluate("""Promise.all([...new Set([...Datos.tarjetas, ...Datos.preguntas]
        .filter(x => x.figura).map(x => x.figura.src))].map(s => fetch(s).then(r => r.ok)))""")
    assert figs and all(figs), "hay figuras que no quedaron en el caché"
    fotos = pag.evaluate("Promise.all(Datos.normas.filter(n => n.figura).map(n => fetch(n.figura.src).then(r => r.ok)))")
    assert len(fotos) == 16 and all(fotos), "las fotos de Normas no quedaron en el caché"
    assert not [e for e in errores if "ERR_INTERNET_DISCONNECTED" not in e], errores
    ctx.close()


def tarjeta_vieja(r, dias_atras):
    """Registro con el formato anterior (sin caja), de hace unos días a mediodía."""
    return {"r": r, "n": 1, "t": pag_ms(FECHA, -dias_atras)}


def pag_ms(dia, delta):
    import datetime
    d = datetime.datetime.strptime(dia, "%Y-%m-%d") + datetime.timedelta(days=delta, hours=12)
    return int(d.timestamp() * 1000)


@prueba
def repaso_de_hoy_en_estudiar(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/estudiar")
    expect(pag.locator('[data-modo="repaso"]')).to_have_attribute("aria-pressed", "true")
    resumen = pag.locator(".repaso").inner_text()
    assert "Viernes 9 de octubre" in resumen and "faltan 8 días" in resumen, resumen
    assert "0 falladas" in resumen and "0 vencidas" in resumen and "31 nuevas" in resumen, resumen
    expect(pag.locator(".contador")).to_have_text("Tarjeta 1 de 31")
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 40 min · 0 ítems")
    revisar_pantalla(pag, "repaso estudiar")
    primera = pag.evaluate("document.querySelector('.tarjeta').getAttribute('aria-controls').replace('reverso-','')")
    pag.locator(".tarjeta").click()
    pag.get_by_role("button", name="No la sabía", exact=True).click()
    reg = progreso(pag)["tarjetas"][primera]
    assert reg["caja"] == 0 and reg["vence"] == FECHA and reg["visto"] == FECHA, reg
    assert "1 falladas" in pag.locator(".repaso").inner_text()
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 40 min · 1 ítem")
    assert progreso(pag)["diario"][FECHA]["items"] == 1
    # la fallada vuelve 4 lugares después
    for _ in range(4):
        pag.locator(".tarjeta").click()
        pag.get_by_role("button", name="La sabía", exact=True).click()
    assert pag.locator(".tarjeta").get_attribute("aria-controls") == "reverso-" + primera
    pag.locator(".tarjeta").click()
    pag.get_by_role("button", name="La sabía", exact=True).click()
    reg = progreso(pag)["tarjetas"][primera]
    assert reg["caja"] == 1 and reg["vence"] == "2026-10-10", reg
    assert not errores, errores
    ctx.close()


@prueba
def repaso_respeta_fechas_simuladas_y_convierte_progreso_viejo(nav, url):
    idx = json.load(open(os.path.join(servidor.RAIZ, "data/tarjetas/tema1.json"), encoding="utf-8"))["tarjetas"]
    a, b, c = idx[0]["id"], idx[1]["id"], idx[2]["id"]
    sembrado = {
        "tarjetas": {
            a: tarjeta_vieja("no", 3),                    # formato viejo, fallada
            b: {"r": "sabia", "n": 2, "t": pag_ms(FECHA, -5), "caja": 2,
                "vence": "2026-10-10", "visto": "2026-10-04"},  # vence mañana
            c: {"r": "sabia", "n": 1, "t": pag_ms(FECHA, -4), "caja": 1,
                "vence": "2026-10-07", "visto": "2026-10-05"},  # vencida hace 2 días
        },
        "preguntas": {}, "prefs": {},
    }
    # 9/10: la fallada y la vencida salen primero; la de mañana no
    ctx, pag, errores = nueva_pagina(nav, url + "#/estudiar", sembrar=sembrado)
    assert "1 falladas" in pag.locator(".repaso").inner_text()
    assert "1 vencidas" in pag.locator(".repaso").inner_text()
    assert pag.locator(".tarjeta").get_attribute("aria-controls") == "reverso-" + a
    guardado = progreso(pag)["tarjetas"][a]
    assert guardado["caja"] == 0 and guardado["vence"] == "2026-10-06", f"no se convirtió: {guardado}"
    pag.locator(".tarjeta").click()
    pag.get_by_role("button", name="La sabía", exact=True).click()
    assert pag.locator(".tarjeta").get_attribute("aria-controls") == "reverso-" + c
    ctx.close()
    # 10/10 (otro día simulado): la de mañana ya venció
    ctx, pag, errores2 = nueva_pagina(nav, url + "#/estudiar", fecha="2026-10-10", sembrar=sembrado)
    assert "Sábado 10 de octubre" in pag.locator(".repaso").inner_text()
    assert pag.locator(".tarjeta").get_attribute("aria-controls") == "reverso-" + a, "la fallada sigue primero"
    assert "2 vencidas" in pag.locator(".repaso").inner_text(), pag.locator(".repaso").inner_text()
    assert not errores and not errores2, errores + errores2
    ctx.close()


@prueba
def meta_diaria_configurable(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/practicar")
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 40 min · 0 ítems")
    pag.locator('details[data-panel="meta"] summary').click()
    pag.select_option("#meta-unidad", "items")
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 53 ítems · 0 min")
    pag.select_option("#meta-valor", "40")
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 40 ítems · 0 min")
    assert progreso(pag)["prefs"]["meta"] == {"unidad": "items", "valor": 40}
    revisar_pantalla(pag, "meta abierta")
    tipo = pag.locator(".pregunta").get_attribute("data-tipo")
    responder(pag, tipo)
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 1 / 40 ítems · 0 min")
    assert progreso(pag)["diario"][FECHA]["seg"] > 0
    pag.locator('.nav__item[data-ruta="estudiar"]').click()
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 1 / 40 ítems · 0 min")
    assert not errores, errores
    ctx.close()


@prueba
def repaso_de_practicar_reinserta_las_falladas_y_muestra_verificar(nav, url):
    preguntas = []
    for n in (1, 2, 3):
        preguntas += json.load(open(os.path.join(servidor.RAIZ, f"data/preguntas/tema{n}.json"), encoding="utf-8"))["preguntas"]
    verif = next(p for p in preguntas if p.get("verificar") and p["tipo"] == "verdadero_falso")
    sembrado = {"tarjetas": {}, "preguntas": {verif["id"]: {
        "r": "bien", "n": 3, "t": pag_ms(FECHA, -2), "caja": 2, "vence": "2026-10-08",
        "visto": "2026-10-03", "bien": 3, "resp": "a"}}, "prefs": {}}
    ctx, pag, errores = nueva_pagina(nav, url + "#/practicar", sembrar=sembrado)
    resumen = pag.locator(".repaso").inner_text()
    assert "1 vencidas" in resumen and "38 nuevas" in resumen, resumen
    assert "con ⚠ Verificar" in resumen, resumen
    assert pag.locator(".pregunta").get_attribute("data-id") == verif["id"], "la vencida va primero"
    expect(pag.locator(".chip--verificar").first).to_be_visible()
    incorrecta = next(o["id"] for o in verif["opciones"] if o["id"] != verif["correcta"])
    pag.locator(f'[data-opcion="{incorrecta}"]').click()
    assert "⚠ Verificar con el profe" in pag.locator("#retro").inner_text()
    reg = progreso(pag)["preguntas"][verif["id"]]
    assert reg["caja"] == 0 and reg["r"] == "mal" and reg["bien"] == 3, reg
    assert "1 falladas" in pag.locator(".repaso").inner_text()
    pag.get_by_role("button", name="Siguiente →").click()
    for _ in range(4):
        pag.get_by_role("button", name="Saltar").click()
    assert pag.locator(".pregunta").get_attribute("data-id") == verif["id"], "la fallada vuelve 4 lugares después"
    pag.locator(f'[data-opcion="{verif["correcta"]}"]').click()
    reg = progreso(pag)["preguntas"][verif["id"]]
    assert reg["caja"] == 1 and reg["vence"] == "2026-10-10", reg
    assert not errores, errores
    ctx.close()


def abrir_simulacro(nav, url, reloj=None, sembrar=None):
    """Abre Simulacro. reloj: hora simulada (ms) para controlar el temporizador."""
    ctx = nav.new_context(viewport=VIEWPORT, service_workers="block")
    ctx.add_init_script(f"window.__fechaPrueba = {json.dumps(FECHA)};")
    if sembrar is not None:
        ctx.add_init_script(
            "try { if (!sessionStorage.getItem('sembrado')) {"
            f" localStorage.setItem({json.dumps(CLAVE)}, {json.dumps(json.dumps(sembrar))});"
            " sessionStorage.setItem('sembrado', '1'); } } catch (e) {}")
    if reloj is not None:
        ctx.clock.install(time=reloj / 1000)
    pag = ctx.new_page()
    errores = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.goto(url + "#/simulacro")
    pag.wait_for_selector("body[data-listo='1']")
    return ctx, pag, errores


def examen_guardado(pag):
    return progreso(pag).get("simulacro")


def pregunta_actual(pag):
    return pag.evaluate("""(() => { const id = document.querySelector('.pregunta').dataset.id;
        return Datos.preguntas.find(p => p.id === id); })()""")


RELOJ_0 = 1_791_640_800_000  # hora fija para el temporizador


@prueba
def simulacro_completo_sin_retroalimentacion_hasta_terminar(nav, url):
    ctx, pag, errores = abrir_simulacro(nav, url, reloj=RELOJ_0)
    expect(pag.locator("#titulo")).to_have_text("Simulacro")
    expect(pag.locator('[data-duracion="25"]')).to_have_attribute("aria-pressed", "true")
    assert "Total: 40 puntos" in pag.locator("#vista").inner_text()
    revisar_pantalla(pag, "simulacro configurar")
    pag.get_by_role("button", name="Empezar simulacro").click()
    expect(pag.locator("#reloj-tiempo")).to_have_text("25:00")
    e = examen_guardado(pag)
    assert len(e["ids"]) == 23 and e["fase"] == "examen"
    revisar_pantalla(pag, "simulacro examen")
    for i in range(23):
        p = pregunta_actual(pag)
        if p["tipo"] == "respuesta_corta":
            pag.fill("#resp-texto", "Respuesta " + str(i))
        else:
            pag.locator(f'[data-opcion="{p["correcta"]}"]').click()
            if p["tipo"] == "verdadero_falso" and pag.locator("#resp-justif").count():
                pag.fill("#resp-justif", "Justificación " + str(i))
        # sin retroalimentación durante el examen
        assert pag.locator(".retro, .es-correcta, .es-incorrecta, .verificar").count() == 0
        if i < 22:
            pag.get_by_role("button", name="Siguiente →").click()
    revisar_pantalla(pag, "simulacro última")
    pag.clock.fast_forward(12 * 60 * 1000)
    pag.locator(".acciones").get_by_role("button", name="Terminar").click()
    assert "Respondiste todas" in pag.locator(".confirmar").inner_text()
    pag.get_by_role("button", name="Sí, terminar").click()
    expect(pag.locator("#h-auto")).to_have_text("Autoevaluación")
    revisar_pantalla(pag, "simulacro autoevaluación")
    for b in pag.locator('[data-justif="si"]').all():
        b.click()
    for c in pag.locator("[data-punto]").all():
        c.check()
    pag.get_by_role("button", name="Ver resultado").click()
    texto = pag.locator("#vista").inner_text()
    assert "100" in pag.locator(".nota-final__valor").inner_text(), texto[:300]
    assert "40 de 40 puntos" in texto
    # 12 min simulados + los segundos reales que tardó la prueba en contestar
    assert re.search(r"Tiempo usado: 12:[0-5]\d de 25:00", texto), texto[:300]
    assert pag.locator("details.revision").count() == 23
    assert pag.locator('[data-accion="mandar"]').count() == 0, "sin fallos no se ofrece mandar al repaso"
    pag.locator("details.revision").first.locator("summary").click()
    assert "Fuente" in pag.locator("details.revision").first.inner_text()
    revisar_pantalla(pag, "simulacro resultado")
    hist = progreso(pag)["historial"]
    assert hist[0]["nota"] == 100 and 12 * 60 * 1000 <= hist[0]["usado"] < 13 * 60 * 1000, hist
    assert not errores, errores
    ctx.close()


@prueba
def temporizador_sobrevive_a_la_recarga_y_cierra_solo(nav, url):
    ctx, pag, errores = abrir_simulacro(nav, url, reloj=RELOJ_0)
    pag.get_by_role("button", name="Empezar simulacro").click()
    p = pregunta_actual(pag)
    pag.locator("[data-opcion]").first.click()
    pag.clock.fast_forward(10 * 60 * 1000)
    expect(pag.locator("#reloj-tiempo")).to_have_text("15:00")
    # recarga (o el teléfono cerró la pestaña): sigue el mismo examen y el mismo tiempo
    pag.reload()
    pag.wait_for_selector("body[data-listo='1']")
    expect(pag.locator("#reloj-tiempo")).to_have_text("15:00")
    assert pregunta_actual(pag)["id"] == p["id"]
    expect(pag.locator("[data-opcion]").first).to_have_attribute("aria-pressed", "true")
    # pantalla bloqueada 11 min: al volver se recalcula con la hora real
    pag.clock.fast_forward(11 * 60 * 1000)
    pag.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
    expect(pag.locator("#reloj-tiempo")).to_have_text("4:00")
    expect(pag.locator("#reloj")).to_have_class("reloj reloj--poco")
    pag.clock.fast_forward(4 * 60 * 1000 + 1000)
    expect(pag.locator("#h-res, #h-auto")).to_be_visible()
    e = examen_guardado(pag)
    assert e["porTiempo"] is True and e["terminado"] - e["inicio"] == 25 * 60 * 1000, e
    assert "se acabó el tiempo" in pag.locator("#vista").inner_text().lower()
    assert not errores, errores
    ctx.close()


@prueba
def examen_vencido_al_volver_se_cierra(nav, url):
    preguntas = []
    for n in (1, 2, 3):
        preguntas += json.load(open(os.path.join(servidor.RAIZ, f"data/preguntas/tema{n}.json"), encoding="utf-8"))["preguntas"]
    ids = [p["id"] for p in preguntas if p["tipo"] == "seleccion_unica"][:6]
    vencido = {"tarjetas": {}, "preguntas": {}, "prefs": {}, "simulacro": {
        "v": 1, "duracion": 25, "temas": [1, 2, 3], "semilla": 1, "ids": ids, "faltan": {},
        "inicio": RELOJ_0 - 60 * 60 * 1000, "fin": RELOJ_0 - 35 * 60 * 1000, "terminado": None,
        "porTiempo": False, "fase": "examen", "pos": 2, "resp": {ids[0]: {"op": "a"}}, "auto": {}, "enviados": False}}
    ctx, pag, errores = abrir_simulacro(nav, url, reloj=RELOJ_0, sembrar=vencido)
    expect(pag.locator("#h-res")).to_be_visible()
    assert "se acabó el tiempo" in pag.locator(".nota-final").inner_text()
    assert "25:00 de 25:00" in pag.locator(".nota-final").inner_text()
    assert not errores, errores
    ctx.close()


@prueba
def simulacro_manda_los_fallos_a_repaso_de_hoy(nav, url):
    ctx, pag, errores = abrir_simulacro(nav, url, reloj=RELOJ_0)
    pag.locator('[data-tema="1"]').uncheck()
    pag.locator('[data-tema="2"]').uncheck()
    assert "faltan" not in pag.locator(".tarjeta-info").first.inner_text()
    pag.get_by_role("button", name="Empezar simulacro").click()
    e = examen_guardado(pag)
    assert e["temas"] == [3]
    assert all(pag.evaluate(f"Datos.preguntas.find(p => p.id === {json.dumps(i)}).tema") == 3 for i in e["ids"])
    # responde bien solo la primera y termina
    p = pregunta_actual(pag)
    pag.locator(f'[data-opcion="{p["correcta"]}"]').click()
    pag.locator("details.mapa summary").click()
    pag.locator("details.mapa").get_by_role("button", name="Terminar examen").click()
    assert "Te quedan 22 sin responder" in pag.locator(".confirmar").inner_text()
    pag.get_by_role("button", name="Sí, terminar").click()
    expect(pag.locator("#h-res")).to_be_visible()
    pag.get_by_role("button", name="Mandar 22 fallos a Repaso de hoy").click()
    expect(pag.locator(".enviado")).to_contain_text("22 preguntas quedaron")
    guardado = progreso(pag)["preguntas"]
    fallos = [i for i in e["ids"] if i != p["id"]]
    assert all(guardado[i]["caja"] == 0 and guardado[i]["vence"] == FECHA for i in fallos)
    assert p["id"] not in guardado, "lo acertado no se toca"
    pag.locator(".enviado a").click()
    expect(pag.locator("#titulo")).to_have_text("Practicar")
    assert "22 falladas" in pag.locator(".repaso").inner_text()
    assert pag.locator(".pregunta").get_attribute("data-id") in fallos
    # «Nuevo simulacro» vuelve a configurar y conserva el historial
    pag.locator('.nav__item[data-ruta="simulacro"]').click()
    pag.get_by_role("button", name="Nuevo simulacro").click()
    assert "Tus últimos simulacros" in pag.locator("#vista").inner_text()
    assert not errores, errores
    ctx.close()


def progreso_de_ejemplo():
    """Progreso sembrado: 3 días seguidos de estudio y algunos ítems calificados."""
    def r(res, n, dias, **extra):
        return {"r": res, "n": n, "t": pag_ms(FECHA, -dias), "caja": 1, "vence": "2026-10-10",
                "visto": "2026-10-07", **extra}
    return {
        "tarjetas": {"t1-1A-01": r("sabia", 2, 1), "t1-1A-02": r("no", 1, 1), "t2-2A-01": r("dudosa", 1, 2)},
        "preguntas": {"p1-1A-t01": r("bien", 2, 1, bien=2, resp="b"), "p2-2A-x01": r("mal", 3, 0, bien=1, resp="a")},
        "diario": {"2026-10-07": {"seg": 1800, "items": 30}, "2026-10-08": {"seg": 2700, "items": 45},
                   "2026-10-09": {"seg": 600, "items": 12}, "2026-10-05": {"seg": 300, "items": 4}},
        "prefs": {"meta": {"unidad": "minutos", "valor": 40}},
        "historial": [{"fecha": "2026-10-08", "duracion": 25, "temas": [1, 2, 3], "puntos": 28, "maximo": 40, "nota": 70, "usado": 1260000}],
        "simulacro": None,
    }


@prueba
def progreso_muestra_cuenta_regresiva_racha_tiempo_y_dominio(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/progreso", sembrar=progreso_de_ejemplo())
    expect(pag.locator("#titulo")).to_have_text("Progreso")
    assert pag.locator(".cuenta__num").inner_text() == "8"
    assert "Sábado 17 de octubre, 8:00 a. m." in pag.locator(".cuenta").inner_text()
    kpis = " ".join(pag.locator(".kpis").inner_text().split())
    assert "3 días de racha incluye hoy" in kpis, kpis
    assert "337 sin ver" in kpis, kpis  # 152 + 190 − 5 vistos
    tiempo = pag.locator("#h-tiempo").locator("..").inner_text()
    assert "Hoy: 10 / 40 min" in tiempo and "últimos 7 días: 90 min" in tiempo, tiempo
    lista = pag.locator("#h-tiempo ~ ul.solo-lector").inner_text()
    assert "viernes 9 de octubre: 10 min, 12 ítems" in lista, lista
    assert pag.locator("svg.grafico rect").count() == 7
    # 5 de 342 vistos; sabidos: t1-1A-01 y p1-1A-t01 → 1 %; aciertos 3 de 5 = 60 %
    assert "General: 1 % dominado · 60 % de aciertos" in pag.locator(".dominio__global").inner_text()
    t1 = pag.locator('details.dominio[data-tema="1"]')
    t1.locator("summary").click()
    sub = t1.locator('li[data-subtema="1A"]').inner_text()
    assert "3 de 18 vistos" in sub and "100 % de aciertos" in sub, sub
    reforzar = pag.locator(".reforzar").inner_text()
    assert "2A" in reforzar and "1A" in reforzar, reforzar
    revisar_pantalla(pag, "progreso")
    pag.locator('[data-reforzar="2A"]').click()
    expect(pag.locator("#titulo")).to_have_text("Practicar")
    expect(pag.locator('[data-modo="tema"]')).to_have_attribute("aria-pressed", "true")
    assert pag.locator(".filtros__resumen").last.inner_text().startswith("Tema 2 · 2A")
    assert pag.locator(".pregunta").get_attribute("data-id").startswith("p2-2A-")
    assert not errores, errores
    ctx.close()


@prueba
def exportar_borrar_e_importar_el_progreso(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/progreso", sembrar=progreso_de_ejemplo())
    with pag.expect_download() as info:
        pag.get_by_role("button", name="Exportar progreso (.json)").click()
    descarga = info.value
    assert descarga.suggested_filename == f"progreso-materiales-{FECHA}.json"
    import tempfile
    ruta = os.path.join(tempfile.mkdtemp(), descarga.suggested_filename)
    descarga.save_as(ruta)  # se copia: la descarga se borra al cerrar el contexto
    archivo = json.loads(open(ruta, encoding="utf-8").read())
    assert archivo["app"] == "pryecto_materiales" and archivo["formato"] == 1
    assert set(archivo["progreso"]["tarjetas"]) == {"t1-1A-01", "t1-1A-02", "t2-2A-01"}
    # borrar con confirmación
    pag.get_by_role("button", name="Borrar mi progreso").click()
    assert "No se puede deshacer" in pag.locator(".confirmar").inner_text()
    pag.get_by_role("button", name="Cancelar").click()
    assert progreso(pag)["tarjetas"], "cancelar no borra"
    pag.get_by_role("button", name="Borrar mi progreso").click()
    with pag.expect_navigation():
        pag.get_by_role("button", name="Sí, borrar todo").click()
    pag.wait_for_selector("body[data-listo='1']")
    expect(pag.locator(".enviado")).to_have_text("✓ Se borró tu progreso.")
    guardado = progreso(pag)
    assert guardado["tarjetas"] == {} and guardado["preguntas"] == {} and guardado["diario"] == {} and guardado["historial"] == []
    assert guardado["prefs"]["meta"] == {"unidad": "minutos", "valor": 40}, "los ajustes se conservan"
    assert pag.locator(".kpi__valor").nth(1).inner_text() == "342"
    # archivo inválido
    pag.locator("#archivo-progreso").set_input_files(
        files=[{"name": "otro.json", "mimeType": "application/json", "buffer": b'{"app": "otra"}'}])
    expect(pag.locator(".error")).to_contain_text("no es un progreso de esta app")
    pag.locator("#archivo-progreso").set_input_files(
        files=[{"name": "roto.json", "mimeType": "application/json", "buffer": b"esto no es json"}])
    expect(pag.locator(".error")).to_contain_text("no es un JSON de progreso")
    # importar y combinar
    pag.locator("#archivo-progreso").set_input_files(ruta)
    resumen = pag.locator(".confirmar").inner_text()
    assert "3 tarjetas, 2 preguntas, 4 días de estudio y 1 simulacro" in resumen, resumen
    revisar_pantalla(pag, "progreso importar")
    with pag.expect_navigation():
        pag.get_by_role("button", name="Combinar (recomendado)").click()
    pag.wait_for_selector("body[data-listo='1']")
    expect(pag.locator(".enviado")).to_have_text("✓ Progreso combinado con el archivo.")
    guardado = progreso(pag)
    assert set(guardado["tarjetas"]) == {"t1-1A-01", "t1-1A-02", "t2-2A-01"}
    assert guardado["diario"]["2026-10-08"]["items"] == 45 and len(guardado["historial"]) == 1
    assert pag.locator(".kpi__valor").nth(2).inner_text() == "3", "vuelve la racha"
    ctx.close()
    # reemplazar en otro «teléfono» con otro progreso
    otro = {"tarjetas": {"t3-3A-01": {"r": "sabia", "n": 1, "t": pag_ms(FECHA, 0), "caja": 2, "vence": "2026-10-11", "visto": FECHA}},
            "preguntas": {}, "diario": {}, "prefs": {}, "historial": []}
    ctx, pag, errores2 = nueva_pagina(nav, url + "#/progreso", sembrar=otro)
    pag.locator("#archivo-progreso").set_input_files(ruta)
    with pag.expect_navigation():
        pag.get_by_role("button", name="Reemplazar").click()
    pag.wait_for_selector("body[data-listo='1']")
    guardado = progreso(pag)
    assert "t3-3A-01" not in guardado["tarjetas"] and "t1-1A-01" in guardado["tarjetas"]
    assert not errores and not errores2, errores + errores2
    ctx.close()


@prueba
def buscar_sin_tildes_con_resaltado_y_agrupado(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/buscar")
    expect(pag.locator('[data-pestana="buscar"]')).to_have_attribute("aria-pressed", "true")
    assert "al menos 2 letras" in pag.locator("#conteo").inner_text()
    revisar_pantalla(pag, "buscar vacío")
    pag.fill("#q", "HORMIGON")
    expect(pag.locator("#conteo")).to_contain_text("resultado")
    tarjeta = pag.locator('details.resultado[data-id="t1-1A-01"]')
    expect(tarjeta).to_be_visible()
    assert tarjeta.locator("mark").first.inner_text() == "hormigón", "resalta el texto original con tilde"
    grupos = pag.locator(".grupo-res h3").all_inner_texts()
    orden = [g.split(" (")[0] for g in grupos]
    assert orden == [x for x in ["Glosario", "Tarjetas", "Preguntas"] if x in orden], orden
    tarjeta.locator("summary").click()
    expect(tarjeta.locator(".resultado__cuerpo")).to_contain_text("Respuesta")
    expect(tarjeta.locator(".resultado__cuerpo")).to_contain_text("Fuente")
    revisar_pantalla(pag, "buscar resultados")
    # varias palabras: deben estar todas
    pag.fill("#q", "exudacion astm")
    expect(pag.locator("#conteo")).to_contain_text("resultado")
    n = pag.locator("details.resultado").count()
    pag.fill("#q", "exudacion")
    expect(pag.locator("#conteo")).not_to_contain_text(f"{n} resultado")
    pag.fill("#q", "zzzqqq")
    expect(pag.locator("#conteo")).to_contain_text("No hay resultados para «zzzqqq»")
    # abrir una pregunta en Practicar desde el resultado
    pag.fill("#q", "mortero")
    expect(pag.locator('details.resultado[data-id="p1-1A-t01"]')).to_be_visible()
    pag.locator('details.resultado[data-id="p1-1A-t01"] summary').click()
    expect(pag.locator('details.resultado[data-id="p1-1A-t01"]')).to_contain_text("✓ correcta")
    pag.locator('details.resultado[data-id="p1-1A-t01"]').get_by_role("button", name="Abrir en Practicar").click()
    expect(pag.locator("#titulo")).to_have_text("Practicar")
    assert pag.locator(".pregunta").get_attribute("data-id") == "p1-1A-t01"
    assert "De Buscar:" in pag.locator(".extra").inner_text()
    assert not errores, errores
    ctx.close()


@prueba
def glosario_alfabetico_con_definicion_y_fuente(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/buscar")
    pag.locator('[data-pestana="glosario"]').click()
    letras = pag.locator(".letras__btn").all_inner_texts()
    assert letras[0] == "A" and "Á" not in letras, letras
    assert pag.locator(".glosario__termino").count() == 60
    terminos = pag.locator(".glosario dt").all_inner_texts()
    nombres = [t.rsplit(" ", 1)[0] for t in terminos]
    ordenado = pag.evaluate("(xs) => [...xs].sort((a, b) => a.localeCompare(b, 'es', { sensitivity: 'base' }))", nombres)
    assert nombres == ordenado, "orden alfabético en español"
    mortero = pag.locator('.glosario__termino[data-id="g-mortero"]').inner_text()
    assert "pasta cementicia y agregado fino" in mortero and "Fuente" in mortero
    pag.locator('.letras__btn:text-is("P")').click()
    expect(pag.locator("#letra-P")).to_be_focused()
    revisar_pantalla(pag, "glosario")
    assert progreso(pag)["prefs"]["pestanaBuscar"] == "glosario", "recuerda la pestaña"
    assert not errores, errores
    ctx.close()


@prueba
def galeria_de_figuras_abre_los_items_que_las_usan(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/buscar")
    pag.locator('[data-pestana="figuras"]').click()
    figs = pag.locator(".figura-btn")
    assert figs.count() == 15
    for i in range(15):
        img = figs.nth(i).locator("img")
        assert img.get_attribute("alt"), f"figura {i} sin alt"
        assert "Fuente:" in figs.nth(i).inner_text()
    revisar_pantalla(pag, "figuras")
    c117 = pag.locator('.figura-btn:has(img[src="img/ensayos/c117.jpg"])')
    assert "ASTM C117" in c117.inner_text() and "Abre 2 tarjetas" in c117.inner_text()
    c117.click()
    expect(pag.locator("#titulo")).to_have_text("Estudiar")
    expect(pag.locator(".contador")).to_have_text("Tarjeta 1 de 2")
    assert "figura ASTM C117" in pag.locator(".extra").inner_text()
    pag.locator(".tarjeta").click()
    assert pag.locator(".figura img").get_attribute("src") == "img/ensayos/c117.jpg"
    pag.locator('.barra__buscar').click()
    abaco = pag.locator('.figura-btn:has(img[src="img/examenes/X01-p5-abaco.jpg"])')
    assert "Abre 1 pregunta" in abaco.inner_text()
    abaco.click()
    expect(pag.locator("#titulo")).to_have_text("Practicar")
    assert pag.locator(".pregunta .figura img").get_attribute("src") == "img/examenes/X01-p5-abaco.jpg"
    assert not errores, errores
    ctx.close()


@prueba
def lista_de_items_a_verificar_con_el_profe(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/buscar")
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    pag.locator('[data-pestana="verificar"]').click()
    assert "44 ítems marcados «⚠ Verificar»: 16 tarjetas y 28 preguntas" in pag.locator(".pestana").inner_text()
    assert pag.locator(".verif-item").count() == 44
    assert pag.locator(".verif-item .verificar").count() == 44
    revisar_pantalla(pag, "verificar")
    pag.get_by_role("button", name="Copiar lista para el profe").click()
    expect(pag.locator("#copiado")).to_contain_text("Lista copiada (44 ítems)")
    copiado = pag.evaluate("navigator.clipboard.readText()")
    assert copiado.startswith("Consultas para el profe (IC-0604, I examen): 44 ítems"), copiado[:80]
    assert copiado.count("Duda: ") == 44
    pag.get_by_role("button", name="Practicar las 28 preguntas").click()
    expect(pag.locator("#titulo")).to_have_text("Practicar")
    expect(pag.locator(".contador")).to_have_text("Pregunta 1 de 28")
    expect(pag.locator(".chip--verificar").first).to_be_visible()
    assert not errores, errores
    ctx.close()


@prueba
def practicar_baraja_las_opciones_y_ajusta_las_letras(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/practicar")
    por_tema(pag)
    pag.select_option("#pra-tema", "1")
    barajadas = 0
    revisadas = 0
    for _ in range(12):
        p = pregunta_actual(pag)
        if p["tipo"] != "seleccion_unica":
            pag.get_by_role("button", name="Saltar").click()
            continue
        letras = pag.locator(".opcion__letra").all_inner_texts()
        assert letras == list("ABCDE"[:len(letras)]), f"letras en orden: {letras}"
        ids = [b.get_attribute("data-opcion") for b in pag.locator("[data-opcion]").all()]
        assert sorted(ids) == sorted(o["id"] for o in p["opciones"])
        if ids != sorted(ids):
            barajadas += 1
        letra_ok = "ABCDE"[ids.index(p["correcta"])]
        incorrecta = next(i for i in ids if i != p["correcta"])
        pag.locator(f'[data-opcion="{incorrecta}"]').click()
        retro = pag.locator("#retro").inner_text()
        assert f"La correcta es la {letra_ok}." in retro, (p["id"], letra_ok, retro[:120])
        if p["explicacion"].startswith("Correcta la "):
            assert f"Correcta la {letra_ok}" in retro, (p["id"], letra_ok, retro[:160])
        revisadas += 1
        pag.get_by_role("button", name="Siguiente →").click()
    assert revisadas >= 5, revisadas
    assert barajadas >= 2, f"solo {barajadas} de {revisadas} salieron barajadas"
    assert not errores, errores
    ctx.close()


@prueba
def simulacro_conserva_el_orden_de_opciones_al_recargar(nav, url):
    ctx, pag, errores = abrir_simulacro(nav, url, reloj=RELOJ_0)
    pag.get_by_role("button", name="Empezar simulacro").click()
    e = examen_guardado(pag)
    ordenes = []
    for i in range(6):  # las 6 de selección única van primero
        ordenes.append([b.get_attribute("data-opcion") for b in pag.locator("[data-opcion]").all()])
        assert ordenes[-1] == e["orden"][e["ids"][i]]
        pag.get_by_role("button", name="Siguiente →").click()
    assert any(o != sorted(o) for o in ordenes), "alguna sale barajada"
    pag.locator("details.mapa summary").click()
    pag.locator('[data-ir="0"]').click()
    pag.reload()
    pag.wait_for_selector("body[data-listo='1']")
    assert [b.get_attribute("data-opcion") for b in pag.locator("[data-opcion]").all()] == ordenes[0]
    # la revisión usa las mismas letras
    p = pregunta_actual(pag)
    pag.locator(f'[data-opcion="{p["correcta"]}"]').click()
    letra = "ABCDE"[ordenes[0].index(p["correcta"])]
    pag.locator("details.mapa summary").click()
    pag.locator("details.mapa").get_by_role("button", name="Terminar examen").click()
    pag.get_by_role("button", name="Sí, terminar").click()
    expect(pag.locator("#h-res")).to_be_visible()
    primera = pag.locator("details.revision").first
    primera.locator("summary").click()
    texto = primera.inner_text()
    assert f"Tu respuesta\n{letra}. " in texto.replace("\n\n", "\n"), texto[:300]
    assert not errores, errores
    ctx.close()


@prueba
def nueva_version_reemplaza_el_cache(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url, sw=True)
    pag.evaluate("navigator.serviceWorker.ready.then(() => true)")
    pag.reload()
    pag.wait_for_selector("body[data-listo='1']")
    vieja = pag.evaluate("self.APP_VERSION")
    nueva = vieja + "-prueba"
    # simula una publicación: el servidor entrega un version.js con otra versión
    servidor.SOBRESCRIBIR["js/version.js"] = (
        f'self.APP_VERSION = "{nueva}";\nself.APP_FECHA = "prueba";\n').encode()
    try:
        pag.evaluate("navigator.serviceWorker.getRegistration().then(r => r.update()).then(() => true)")
        expect(pag.locator("#aviso-version")).to_be_visible(timeout=15000)
        with pag.expect_navigation():
            pag.get_by_role("button", name="Actualizar").click()
        pag.wait_for_selector("body[data-listo='1']")
        assert pag.evaluate("self.APP_VERSION") == nueva
        expect(pag.locator("#aviso-version")).to_be_hidden()
        assert pag.evaluate("caches.keys()") == ["pryecto_materiales-" + nueva], "quedó un caché viejo"
    finally:
        servidor.SOBRESCRIBIR.clear()
    assert not errores, errores
    ctx.close()


# ---------- Normas ----------
def guardado_normas(pag):
    return progreso(pag)["normas"]


def escribir_norma(pag, letra, numero):
    pag.locator(f'[data-letra="{letra}"]').click()
    pag.fill("#numero", numero)
    pag.get_by_role("button", name="Comprobar").click()


@prueba
def normas_escribir_confundir_no_se_e_inversa(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas")
    texto = pag.locator("#vista").inner_text()
    assert "Normas ASTM de memoria" in texto and "0 de 26 normas dominadas" in texto, texto[:300]
    assert pag.locator(".fam-item").count() == 8, "deben verse las 8 familias"
    revisar_pantalla(pag, "normas inicio")
    pag.get_by_role("button", name=re.compile(r"Entrenar hoy")).click()

    # 1.ª ficha: «escribir» de la primera norma de la primera familia (D75). Acierta con la letra D.
    assert pag.locator(".pregunta").get_attribute("data-id") == "n-D75-e"
    assert "Muestreo de agregados en campo" in pag.locator(".norma-mide").inner_text()
    revisar_pantalla(pag, "normas escribir")
    escribir_norma(pag, "D", "75")
    assert "Correcto: ASTM D75" in pag.locator("#retro").inner_text()
    assert "Ayuda de memoria" in pag.locator("#retro").inner_text()
    assert pag.locator("#retro .fuentes").is_visible()
    revisar_pantalla(pag, "normas retro")
    pag.get_by_role("button", name="Siguiente →").click()

    # 2.ª ficha (C702): la confunde con su pareja D75 → queda anotado y vuelve hoy
    assert pag.locator(".pregunta").get_attribute("data-id") == "n-C702-e"
    escribir_norma(pag, "D", "75")
    retro = pag.locator("#retro").inner_text()
    assert "Era ASTM C702" in retro and "Escribiste ASTM D75" in retro, retro
    pag.get_by_role("button", name="Siguiente →").click()

    # 3.ª ficha: «No sé» no pide número y la califica mal, sin pareja
    assert pag.locator(".pregunta").get_attribute("data-id") == "n-C117-e"
    pag.get_by_role("button", name="No sé").click()
    assert "Respondiste «No sé»" in pag.locator("#retro").inner_text()
    pag.get_by_role("button", name="Siguiente →").click()

    g = guardado_normas(pag)
    assert g["n-D75-e"]["r"] == "bien" and g["n-D75-e"]["dias"] == [FECHA] and "conf" not in g["n-D75-e"]
    assert g["n-C702-e"]["r"] == "mal" and g["n-C702-e"]["conf"] == {"D75": 1} and g["n-C702-e"]["caja"] == 0
    assert g["n-C117-e"]["r"] == "mal" and "conf" not in g["n-C117-e"]

    # sin número no califica
    pag.get_by_role("button", name="Comprobar").click()
    assert pag.locator("#retro").count() == 0

    # recorre hasta una ficha «inversa»: las opciones traen la pareja y la correcta se marca
    for _ in range(40):
        if pag.locator(".pregunta").get_attribute("data-id").endswith("-i"):
            break
        pag.get_by_role("button", name="No sé").click()
        pag.get_by_role("button", name="Siguiente →").click()
    id_i = pag.locator(".pregunta").get_attribute("data-id")
    assert id_i.endswith("-i"), "no apareció ninguna ficha inversa"
    norma = id_i.split("-")[1]
    assert pag.locator("[data-opcion]").count() == 4
    revisar_pantalla(pag, "normas inversa")
    otra = pag.evaluate("(n) => Datos.normaPorId[n].confunde_con[0]", norma)
    assert pag.locator(f'[data-opcion="{otra}"]').count() == 1, "la pareja debe estar entre las opciones"
    pag.locator(f'[data-opcion="{otra}"]').click()
    assert "Incorrecto" in pag.locator("#retro").inner_text()
    assert pag.locator(".opcion.es-correcta").count() == 1 and pag.locator(".opcion.es-incorrecta").count() == 1
    g = guardado_normas(pag)
    assert g[id_i]["r"] == "mal" and g[id_i]["conf"] == {otra: 1}
    revisar_pantalla(pag, "normas inversa respondida")

    # la confusión aparece en el inicio como pareja
    pag.get_by_role("button", name="← Salir").click()
    assert "ASTM C702 ↔ ASTM D75" in pag.locator("#vista").inner_text()
    assert pag.locator('[data-accion="parejas"]').is_visible()
    assert not errores, errores
    ctx.close()


@prueba
def normas_dominada_con_dos_dias_y_practica_por_familia(nav, url):
    reg = {"r": "bien", "n": 1, "t": 1, "caja": 2, "vence": "2026-10-08", "visto": "2026-10-07", "bien": 1, "dias": ["2026-10-07"]}
    sembrado = {"tarjetas": {}, "preguntas": {}, "normas": {"n-D75-e": reg}, "diario": {}, "prefs": {}, "simulacro": None, "historial": []}
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas", sembrar=sembrado)
    assert "0 de 26 normas dominadas" in pag.locator("#vista").inner_text()
    pag.get_by_role("button", name=re.compile(r"Entrenar hoy")).click()
    assert pag.locator(".pregunta").get_attribute("data-id") == "n-D75-e", "la vencida sale primero"
    escribir_norma(pag, "D", "75")  # segundo día distinto → dominada
    pag.get_by_role("button", name="← Salir").click()
    assert "1 de 26 normas dominadas" in pag.locator("#vista").inner_text()
    # práctica por familia: las 2 normas de muestreo → 6 fichas (escribir, inversa y foto)
    pag.locator('[data-familia="muestreo"]').click()
    assert "Ficha 1 de 6" in pag.locator(".contador").inner_text()
    ids = []
    for _ in range(6):
        ids.append(pag.locator(".pregunta").get_attribute("data-id"))
        if ids[-1].endswith("-e"):
            pag.get_by_role("button", name="No sé").click()
        else:
            pag.locator("[data-opcion]").first.click()
        pag.get_by_role("button", name="Siguiente →").click()
    assert ids[:5] == ["n-D75-e", "n-C702-e", "n-D75-i", "n-C702-i", "n-D75-f"], ids  # la 6.ª puede ser una «No sé» que volvió
    assert not errores, errores
    ctx.close()


@prueba
def normas_parejas_lado_a_lado_con_diferencias_y_practica_de_la_pareja(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas")
    assert "Aprender por parejas · 0 de 23 vistas" in pag.locator("#vista").inner_text()
    pag.get_by_role("button", name=re.compile(r"Aprender por parejas")).click()
    assert "Pareja 1 de 23" in pag.locator(".contador").inner_text()
    assert pag.get_by_role("button", name="← Anterior").is_disabled()
    cols = pag.locator(".par-col")
    assert cols.count() == 2
    assert "ASTM D75" in cols.nth(0).inner_text() and "ASTM C702" in cols.nth(1).inner_text()
    assert pag.locator("mark.difiere").count() >= 1
    revisar_pantalla(pag, "normas parejas")
    # avanza hasta C127 / C128: lo que las distingue es grueso / fino
    for _ in range(23):
        if "ASTM C127" in pag.locator(".par-col").nth(0).inner_text():
            break
        pag.get_by_role("button", name="Siguiente →").click()
    assert pag.locator(".par-col").nth(1).locator("p.norma-codigo").inner_text() == "ASTM C128"
    assert pag.locator(".par-col").nth(0).locator("mark.difiere").all_inner_texts() == ["grueso"]
    assert pag.locator(".par-col").nth(1).locator("mark.difiere").all_inner_texts() == ["fino"]
    assert "Ayuda de memoria" in pag.locator(".par-col").nth(0).inner_text()
    # practicar la pareja: 4 fichas, primero las «escribir» y mezcladas entre las dos
    pag.get_by_role("button", name="Probarme con esta pareja").click()
    assert "Ficha 1 de 6" in pag.locator(".contador").inner_text()
    ids = []
    for _ in range(6):  # todas bien: ninguna ficha vuelve a la cola
        ids.append(pag.locator(".pregunta").get_attribute("data-id"))
        norma = ids[-1].split("-")[1]
        if ids[-1].endswith("-e"):
            escribir_norma(pag, "C", norma[1:])
        else:
            pag.locator(f'[data-opcion="{norma}"]').click()
        pag.get_by_role("button", name="Siguiente →").click()
    assert ids == ["n-C127-e", "n-C128-e", "n-C127-i", "n-C128-i", "n-C127-f", "n-C128-f"], ids
    assert "Volver a las parejas" in pag.locator("#vista").inner_text()
    pag.get_by_role("button", name="Volver a las parejas").click()
    assert "Parejas que se parecen" in pag.locator("#vista").inner_text()
    vistas = progreso(pag)["prefs"]["parejasVistas"]
    assert "C127|C128" in vistas and "C702|D75" in vistas, vistas
    pag.get_by_role("button", name="← Volver a Normas").click()
    assert "vistas" in pag.locator('[data-accion="ver-parejas"]').inner_text()
    assert not errores, errores
    ctx.close()


@prueba
def normas_parejas_confundidas_salen_primero_y_se_abren_desde_el_inicio(nav, url):
    reg = {"r": "mal", "n": 1, "t": 1, "caja": 0, "vence": "2026-10-09", "visto": "2026-10-09", "bien": 0, "conf": {"C1603": 2}}
    sembrado = {"tarjetas": {}, "preguntas": {}, "normas": {"n-C1602-e": reg}, "diario": {}, "prefs": {}, "simulacro": None, "historial": []}
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas", sembrar=sembrado)
    pag.get_by_role("button", name="Ver la pareja").first.click()
    assert "Pareja 1 de 23" in pag.locator(".contador").inner_text()
    assert "La confundiste 2 veces" in pag.locator(".chips").inner_text()
    textos = pag.locator(".par-col").all_inner_texts()
    assert "ASTM C1602" in textos[0] and "ASTM C1603" in textos[1]
    revisar_pantalla(pag, "normas pareja confundida")
    assert not errores, errores
    ctx.close()


@prueba
def normas_foto_sin_pista_en_el_alt_y_confusion_al_elegir_mal(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas")
    pag.locator('[data-familia="muestreo"]').click()
    for _ in range(4):  # salta las 4 primeras (escribir e inversa)
        if pag.locator('[data-accion="nose"]').count():
            pag.get_by_role("button", name="No sé").click()
        else:
            pag.locator("[data-opcion]").first.click()
        pag.get_by_role("button", name="Siguiente →").click()
    assert pag.locator(".pregunta").get_attribute("data-id") == "n-D75-f"
    img = pag.locator(".norma-foto img")
    assert img.get_attribute("alt") == "Foto de un equipo de laboratorio", "el alt no debe dar la respuesta"
    assert img.evaluate("i => i.complete && i.naturalWidth > 0"), "la foto no cargó"
    assert pag.locator(".norma-foto figcaption").count() == 0
    assert pag.locator(".chip-norma").count() == 26
    letras = pag.locator(".chip-norma").all_inner_texts()
    assert letras[:3] == ["C29", "C33", "C40"] and letras[-3:] == ["D75", "D4791", "D5821"], letras
    revisar_pantalla(pag, "normas foto")
    pag.locator('.chip-norma[data-opcion="C702"]').click()
    retro = pag.locator("#retro").inner_text()
    assert "Era ASTM D75" in retro and "Elegiste ASTM C702" in retro, retro
    assert "Cargador frontal" in pag.locator(".norma-foto figcaption").inner_text()
    assert pag.locator(".chip-norma.es-correcta").inner_text() == "D75"
    assert pag.locator(".chip-norma.es-incorrecta").inner_text() == "C702"
    g = guardado_normas(pag)["n-D75-f"]
    assert g["r"] == "mal" and g["conf"] == {"C702": 1}
    revisar_pantalla(pag, "normas foto respondida")
    assert not errores, errores
    ctx.close()


@prueba
def normas_simulacro_de_fotos_sin_retro_hasta_el_final_y_con_nota(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas")
    pag.get_by_role("button", name=re.compile(r"Simulacro de fotos")).click()
    assert "Foto 1 de 10" in pag.locator(".contador").inner_text()
    assert pag.get_by_role("button", name="← Anterior").is_disabled()
    revisar_pantalla(pag, "normas simulacro de fotos")
    for k in range(10):
        assert pag.locator("#retro").count() == 0, "no hay retroalimentación durante el simulacro"
        assert pag.locator(".norma-foto img").get_attribute("alt") == "Foto de un equipo de laboratorio"
        if k == 0:  # se puede cambiar la respuesta
            pag.locator('.chip-norma[data-opcion="C33"]').click()
            pag.locator('.chip-norma[data-opcion="C29"]').click()
            assert pag.locator('.chip-norma[aria-pressed="true"]').count() == 1
        elif k != 3:  # la foto 4 queda sin responder
            pag.locator('.chip-norma[data-opcion="C29"]').click()
        if k < 9:
            pag.get_by_role("button", name="Siguiente →").click()
    pag.get_by_role("button", name="← Anterior").click()
    assert "Foto 9 de 10" in pag.locator(".contador").inner_text()
    pag.get_by_role("button", name="Siguiente →").click()
    pag.get_by_role("button", name="Terminar").click()
    texto = pag.locator("#vista").inner_text()
    assert "Resultado del simulacro de fotos" in texto
    assert pag.locator(".sim-fila").count() == 10
    bien = pag.locator(".sim-fila--bien").count()
    assert bien in (0, 1), "solo la C29 puede salir bien, y solo si tocó"
    assert f"{bien} de 10" in texto
    assert pag.locator(".sim-fila img").first.evaluate("i => i.complete && i.naturalWidth > 0")
    assert "No respondiste" in texto
    revisar_pantalla(pag, "normas simulacro de fotos resultado")
    g = guardado_normas(pag)
    assert len([k for k in g if k.endswith("-f")]) == 10, "cada foto queda como ficha de repaso"
    hist = progreso(pag)["prefs"]["simulacroNormas"]
    assert hist[0]["total"] == 10 and hist[0]["puntos"] == bien and hist[0]["dia"] == FECHA
    pag.get_by_role("button", name="Volver a Normas").click()
    assert f"último: {bien} de 10" in pag.locator("#vista").inner_text()
    assert not errores, errores
    ctx.close()


@prueba
def normas_lista_de_consulta_con_ganchos_fuentes_y_verificar(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url + "#/normas")
    pag.get_by_role("button", name="Ver la lista de normas").click()
    assert pag.locator(".norma-ficha").count() == 26
    texto = pag.locator("#vista").inner_text()
    for esperado in ("ASTM D5821", "fracturadas", "ASTM D4791", "Ayuda de memoria", "Se confunde con", "Manual de Laboratorio"):
        assert esperado in texto, esperado
    assert pag.locator(".norma-ficha .verificar").count() >= 2, "C994 y D4791 llevan VERIFICAR"
    revisar_pantalla(pag, "normas lista")
    pag.get_by_role("button", name="← Volver a Normas").click()
    assert "Normas ASTM de memoria" in pag.locator("#vista").inner_text()
    assert not errores, errores
    ctx.close()


def main():
    srv, url = servidor.iniciar()
    fallas = 0
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for fn in resultados:
            try:
                fn(nav, url)
                print("OK   ", fn.__name__)
            except Exception:  # noqa: BLE001
                fallas += 1
                print("FALLA", fn.__name__)
                traceback.print_exc()
        nav.close()
    srv.shutdown()
    print(f"\n{len(resultados) - fallas}/{len(resultados)} pruebas pasaron")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
