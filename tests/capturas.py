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

    for ruta in ("simulacro", "progreso", "buscar"):
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
        nav.close()
    srv.shutdown()
    print(f"{len(os.listdir(SALIDA))} capturas en {SALIDA}")


if __name__ == "__main__":
    main()
