#!/usr/bin/env python3
"""Capturas de cada pantalla a 390×844, en modo claro y oscuro → tests/capturas/.

Uso: python tests/capturas.py      (la carpeta tests/capturas/ no se sube a git)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import expect, sync_playwright  # noqa: E402

import servidor  # noqa: E402

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capturas")
FECHA = "2026-10-09"
CLAVE = "pryecto_materiales:progreso:v1"
BLOQUEAR_LS = "Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('x','SecurityError')}})"


def listo(pag):
    pag.wait_for_selector("body[data-listo='1']")


def ir_a_pregunta(pag, condicion):
    """Salta preguntas en Practicar hasta una que cumpla condicion(tipo, id)."""
    for _ in range(250):
        sec = pag.locator(".pregunta")
        if condicion(sec.get_attribute("data-tipo"), sec.get_attribute("data-id")):
            return
        pag.get_by_role("button", name="Saltar").click()
    raise RuntimeError("no se encontró la pregunta")


def contexto(nav, esquema):
    ctx = nav.new_context(viewport={"width": 390, "height": 844}, color_scheme=esquema,
                          device_scale_factor=2, service_workers="block")
    ctx.add_init_script(f"window.__fechaPrueba = {json.dumps(FECHA)};")
    return ctx


def todo_al_dia():
    """Progreso con todas las tarjetas vistas y al día (para la pantalla final del repaso)."""
    raiz = servidor.RAIZ
    regs = {}
    for n in (1, 2, 3):
        for t in json.load(open(os.path.join(raiz, f"data/tarjetas/tema{n}.json"), encoding="utf-8"))["tarjetas"]:
            regs[t["id"]] = {"r": "sabia", "n": 2, "t": 0, "caja": 2, "vence": "2026-10-11", "visto": "2026-10-08"}
    return {"tarjetas": regs, "preguntas": {}, "diario": {FECHA: {"seg": 5520, "items": 131}}, "prefs": {}}


def capturar(nav, url, esquema):
    ctx = contexto(nav, esquema)
    pag = ctx.new_page()
    n = [0]

    def foto(nombre):
        n[0] += 1
        pag.wait_for_timeout(350)
        pag.screenshot(path=os.path.join(SALIDA, f"{esquema}-{n[0]:02d}-{nombre}.png"))

    pag.goto(url + "#/estudiar")
    listo(pag)
    foto("estudiar-repaso")
    pag.locator(".tarjeta").click()
    foto("estudiar-volteada")
    pag.get_by_role("button", name="No la sabía", exact=True).click()
    for _ in range(2):
        pag.locator(".tarjeta").click()
        pag.get_by_role("button", name="La sabía", exact=True).click()
    foto("estudiar-repaso-avance")
    pag.locator('details[data-panel="meta"] summary').click()
    foto("meta-diaria")
    pag.locator('details[data-panel="meta"] summary').click()
    pag.locator('[data-modo="tema"]').click()
    pag.locator("details.filtros:not([data-panel]) summary").click()
    pag.select_option("#est-tema", "3")
    pag.select_option("#est-subtema", "3E")
    foto("estudiar-por-tema")
    pag.locator("details.filtros:not([data-panel]) summary").click()
    pag.locator(".tarjeta").click()
    pag.locator(".figura").scroll_into_view_if_needed()
    foto("estudiar-figura")

    pag.locator('.nav__item[data-ruta="practicar"]').click()
    expect(pag.locator(".pregunta")).to_be_visible()
    foto("practicar-repaso")
    pag.locator('[data-modo="tema"]').click()
    expect(pag.locator(".pregunta")).to_be_visible()
    ir_a_pregunta(pag, lambda t, i: t == "seleccion_unica")
    foto("practicar-unica")
    pag.locator("[data-opcion]").nth(1).click()
    foto("practicar-unica-retro")
    pag.get_by_role("button", name="Siguiente →").click()
    ir_a_pregunta(pag, lambda t, i: t == "seleccion_multiple")
    pag.locator("[data-opcion]").first.click()
    foto("practicar-multiple")
    pag.get_by_role("button", name="Revisar").click()
    foto("practicar-multiple-retro")
    pag.get_by_role("button", name="Siguiente →").click()
    ir_a_pregunta(pag, lambda t, i: t == "verdadero_falso" and i.startswith("p2-"))
    pag.locator("[data-opcion]").first.click()
    foto("practicar-vf-retro")
    pag.get_by_role("button", name="Siguiente →").click()
    ir_a_pregunta(pag, lambda t, i: t == "respuesta_corta")
    pag.fill("#respuesta", "Pasta, mortero y concreto se diferencian por los agregados.")
    foto("practicar-corta")
    pag.get_by_role("button", name="Ver respuesta").click()
    foto("practicar-corta-vista")

    for ruta in ("buscar",):
        pag.locator(f'.nav__item[data-ruta="{ruta}"]').click()
        foto(ruta)
    pag.locator(".barra__acerca").click()
    expect(pag.locator("#titulo")).to_have_text("Acerca de")
    foto("acerca")
    ctx.close()

    ctx = contexto(nav, esquema)
    ctx.add_init_script(
        f"try {{ localStorage.setItem({json.dumps(CLAVE)}, {json.dumps(json.dumps(todo_al_dia()))}); }} catch (e) {{}}")
    pag = ctx.new_page()
    pag.goto(url + "#/estudiar")
    listo(pag)
    foto("estudiar-repaso-terminado")
    ctx.close()

    ctx = contexto(nav, esquema)
    ctx.add_init_script(BLOQUEAR_LS)
    pag = ctx.new_page()
    pag.goto(url + "#/estudiar")
    listo(pag)
    foto("sin-localstorage")
    ctx.close()


def capturar_simulacro(nav, url, esquema):
    ctx = contexto(nav, esquema)
    ctx.clock.install(time=1_791_640_800)
    pag = ctx.new_page()

    def foto(nombre):
        pag.wait_for_timeout(300)
        pag.screenshot(path=os.path.join(SALIDA, f"{esquema}-s{nombre}.png"))

    def actual():
        return pag.evaluate("""(() => { const id = document.querySelector('.pregunta').dataset.id;
            return Datos.preguntas.find(p => p.id === id); })()""")

    pag.goto(url + "#/simulacro")
    listo(pag)
    foto("1-configurar")
    pag.get_by_role("button", name="Empezar simulacro").click()
    foto("2-seleccion-unica")
    vf_falso = None
    for i in range(23):
        p = actual()
        if p["tipo"] == "respuesta_corta":
            pag.fill("#resp-texto", "Se mide con el ensayo indicado por la norma.")
        else:
            op = p["correcta"] if i % 3 else p["opciones"][0]["id"]
            pag.locator(f'[data-opcion="{op}"]').click()
            if pag.locator("#resp-justif").count():
                pag.fill("#resp-justif", "Es falso porque el valor correcto es otro.")
                if vf_falso is None:
                    vf_falso = i
                    pag.clock.fast_forward(21 * 60 * 1000)
                    foto("3-falso-con-justificacion")
        if i < 22:
            pag.get_by_role("button", name="Siguiente →").click()
    pag.locator("details.mapa summary").click()
    pag.locator("details.mapa").scroll_into_view_if_needed()
    foto("4-mapa-de-preguntas")
    pag.locator("details.mapa summary").click()
    pag.locator(".acciones").get_by_role("button", name="Terminar").click()
    foto("5-confirmar")
    pag.get_by_role("button", name="Sí, terminar").click()
    foto("6-autoevaluacion")
    for b in pag.locator('[data-justif="si"]').all():
        b.click()
    for c in pag.locator("[data-punto]").all()[::2]:
        c.check()
    pag.locator("[data-punto]").first.scroll_into_view_if_needed()
    foto("7-autoevaluacion-puntos")
    pag.get_by_role("button", name="Ver resultado").click()
    foto("8-resultado")
    pag.locator("details.revision--mal summary").first.click()
    pag.locator("details.revision--mal").first.scroll_into_view_if_needed()
    foto("9-revision")
    ctx.close()


def capturar_progreso(nav, url, esquema):
    import test_app
    ctx = contexto(nav, esquema)
    ctx.add_init_script(
        "try { if (!sessionStorage.getItem('sembrado')) {"
        f" localStorage.setItem({json.dumps(CLAVE)}, {json.dumps(json.dumps(test_app.progreso_de_ejemplo()))});"
        " sessionStorage.setItem('sembrado', '1'); } } catch (e) {}")
    pag = ctx.new_page()

    def foto(nombre):
        pag.wait_for_timeout(300)
        pag.screenshot(path=os.path.join(SALIDA, f"{esquema}-p{nombre}.png"))

    pag.goto(url + "#/progreso")
    listo(pag)
    foto("1-resumen")
    pag.evaluate("document.querySelector('#h-tiempo').scrollIntoView(); window.scrollBy(0, -70)")
    foto("2-tiempo-y-dominio")
    pag.locator('details.dominio[data-tema="2"] summary').click()
    pag.locator('details.dominio[data-tema="2"]').scroll_into_view_if_needed()
    foto("3-subtemas")
    pag.evaluate("document.querySelector('#h-reforzar').scrollIntoView(); window.scrollBy(0, -70)")
    foto("4-reforzar")
    pag.locator("#archivo-progreso").set_input_files(files=[{"name": "p.json", "mimeType": "application/json",
        "buffer": json.dumps({"app": "pryecto_materiales", "formato": 1, "exportado": "2026-10-08T20:00:00.000Z",
                              "progreso": test_app.progreso_de_ejemplo()}).encode()}])
    pag.locator(".confirmar").scroll_into_view_if_needed()
    foto("5-importar")
    pag.get_by_role("button", name="Cancelar").click()
    pag.get_by_role("button", name="Borrar mi progreso").click()
    foto("6-borrar")
    ctx.close()


def main():
    os.makedirs(SALIDA, exist_ok=True)
    for f in os.listdir(SALIDA):
        if f.endswith(".png"):
            os.remove(os.path.join(SALIDA, f))
    srv, url = servidor.iniciar()
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for esquema in ("light", "dark"):
            capturar(nav, url, esquema)
            capturar_simulacro(nav, url, esquema)
            capturar_progreso(nav, url, esquema)
        nav.close()
    srv.shutdown()
    print(f"{len(os.listdir(SALIDA))} capturas en {SALIDA}")


if __name__ == "__main__":
    main()
