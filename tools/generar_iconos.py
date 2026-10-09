#!/usr/bin/env python3
"""Genera los íconos PNG de la PWA en icons/. Uso: python tools/generar_iconos.py

Necesita Pillow. Dibuja un corte de concreto (agregados en una pasta) con «IC» encima.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
AZUL = (11, 87, 164)
PASTA = (226, 222, 212)
PIEDRAS = [(120, 116, 108), (150, 144, 133), (95, 92, 86), (176, 170, 158)]


def fuente(tam):
    for nombre in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        for carpeta in ("C:/Windows/Fonts", "/usr/share/fonts/truetype/dejavu", ""):
            try:
                return ImageFont.truetype(os.path.join(carpeta, nombre), tam)
            except OSError:
                continue
    return ImageFont.load_default()


def icono(lado, maskable):
    esc = 4  # se dibuja grande y se reduce para suavizar bordes
    L = lado * esc
    img = Image.new("RGB", (L, L), AZUL)
    d = ImageDraw.Draw(img)
    # zona segura: 80 % para maskable, 88 % para el normal
    m = int(L * (0.18 if maskable else 0.12))
    caja = (m, m, L - m, L - m)
    d.rounded_rectangle(caja, radius=int(L * 0.08), fill=PASTA)
    rnd = random.Random(604)
    ancho = caja[2] - caja[0]
    for _ in range(26):
        r = rnd.uniform(0.05, 0.11) * ancho
        x = rnd.uniform(caja[0] + r, caja[2] - r)
        y = rnd.uniform(caja[1] + r, caja[3] - r)
        d.ellipse((x - r, y - r * 0.8, x + r, y + r * 0.8), fill=rnd.choice(PIEDRAS))
    # banda con las letras
    alto_banda = int(ancho * 0.42)
    y0 = (L - alto_banda) // 2
    d.rectangle((caja[0], y0, caja[2], y0 + alto_banda), fill=AZUL)
    f = fuente(int(alto_banda * 0.78))
    texto = "IC"
    bb = d.textbbox((0, 0), texto, font=f)
    d.text(((L - (bb[2] - bb[0])) / 2 - bb[0], y0 + (alto_banda - (bb[3] - bb[1])) / 2 - bb[1]),
           texto, font=f, fill=(255, 255, 255))
    return img.resize((lado, lado), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(RAIZ, "icons"), exist_ok=True)
    icono(192, False).save(os.path.join(RAIZ, "icons", "icon-192.png"), optimize=True)
    icono(512, False).save(os.path.join(RAIZ, "icons", "icon-512.png"), optimize=True)
    icono(512, True).save(os.path.join(RAIZ, "icons", "icon-maskable-512.png"), optimize=True)
    print("Íconos generados en icons/")


if __name__ == "__main__":
    main()
