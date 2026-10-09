#!/usr/bin/env python3
"""Pruebas de la app con Playwright (Python) y Chromium, a 390×844.

Uso: python tests/test_app.py
Requiere: pip install playwright && python -m playwright install chromium
Sale con código 1 si alguna prueba falla.
"""
import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import expect, sync_playwright  # noqa: E402

import servidor  # noqa: E402

VIEWPORT = {"width": 390, "height": 844}
CLAVE = "pryecto_materiales:progreso:v1"
SECCIONES = [("estudiar", "Estudiar"), ("practicar", "Practicar"), ("simulacro", "Simulacro"),
             ("progreso", "Progreso"), ("buscar", "Buscar")]

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
    bajos = pag.evaluate("""() => [...document.querySelectorAll('button, a.btn, select, .nav__item, .barra__acerca, summary')]
      .filter(e => e.getClientRects().length)
      .map(e => [e.getBoundingClientRect().height, e.textContent.trim().slice(0, 25)])
      .filter(([h]) => h < 47.5)""")
    assert not bajos, f"{nombre}: controles de menos de 48 px: {bajos[:5]}"
    pie = pag.locator("footer.pie")
    assert pie.inner_text().strip() == "Desarrollado por Adrián Castro Ramírez", f"{nombre}: pie distinto"


@prueba
def recorre_las_cinco_secciones_y_acerca(nav, url):
    ctx, pag, errores = nueva_pagina(nav, url)
    assert pag.locator('meta[name="robots"]').get_attribute("content") == "noindex, nofollow"
    assert pag.locator('meta[name="author"]').get_attribute("content") == "Adrián Castro Ramírez"
    for ruta, nombre in SECCIONES:
        pag.locator(f'.nav__item[data-ruta="{ruta}"]').click()
        expect(pag.locator("#titulo")).to_have_text(nombre)
        expect(pag.locator(f'.nav__item[data-ruta="{ruta}"]')).to_have_attribute("aria-current", "page")
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
    assert "0 falladas" in resumen and "0 vencidas" in resumen and "30 nuevas" in resumen, resumen
    expect(pag.locator(".contador")).to_have_text("Tarjeta 1 de 30")
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 90 min · 0 ítems")
    revisar_pantalla(pag, "repaso estudiar")
    primera = pag.evaluate("document.querySelector('.tarjeta').getAttribute('aria-controls').replace('reverso-','')")
    pag.locator(".tarjeta").click()
    pag.get_by_role("button", name="No la sabía", exact=True).click()
    reg = progreso(pag)["tarjetas"][primera]
    assert reg["caja"] == 0 and reg["vence"] == FECHA and reg["visto"] == FECHA, reg
    assert "1 falladas" in pag.locator(".repaso").inner_text()
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 90 min · 1 ítem")
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
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 90 min · 0 ítems")
    pag.locator('details[data-panel="meta"] summary').click()
    pag.select_option("#meta-unidad", "items")
    expect(pag.locator(".meta__texto")).to_have_text("Hoy: 0 / 120 ítems · 0 min")
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
    assert "1 vencidas" in resumen and "37 nuevas" in resumen, resumen
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
