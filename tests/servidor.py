#!/usr/bin/env python3
"""Servidor local que imita GitHub Pages: sirve el sitio bajo /pryecto_materiales/.

Así se prueba que todas las rutas sean relativas: cualquier pedido fuera del prefijo
da 404. Tampoco sirve fuentes/, tests/ ni .git/ (no se publican).

Uso: python tests/servidor.py [puerto]   →  http://localhost:8000/pryecto_materiales/
"""
import functools
import http.server
import os
import sys
import threading

PREFIJO = "/pryecto_materiales/"
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRIVADO = ("fuentes/", "tests/", ".git/", "tools/")
# Las pruebas pueden reemplazar un archivo (ruta relativa → bytes) para simular una publicación.
SOBRESCRIBIR = {}


class Manejador(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".js": "text/javascript",
        ".json": "application/json",
    }

    def _ruta_valida(self):
        ruta = self.path.split("?", 1)[0].split("#", 1)[0]
        if ruta == PREFIJO.rstrip("/"):
            return "redir"
        if not ruta.startswith(PREFIJO):
            return None
        rel = ruta[len(PREFIJO):]
        if any(rel.startswith(p) for p in PRIVADO):
            return None
        return rel

    def do_GET(self):
        rel = self._ruta_valida()
        if rel == "redir":
            self.send_response(301)
            self.send_header("Location", PREFIJO)
            self.end_headers()
            return
        if rel is None:
            self.send_error(404)
            return
        if rel in SOBRESCRIBIR:
            cuerpo = SOBRESCRIBIR[rel]
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(rel))
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)
            return
        self.path = "/" + rel
        super().do_GET()

    do_HEAD = do_GET

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, *args):
        pass


def iniciar(puerto=0):
    """Inicia el servidor en un hilo. Devuelve (servidor, url_base)."""
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", puerto), functools.partial(Manejador, directory=RAIZ))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}{PREFIJO}"


if __name__ == "__main__":
    srv, url = iniciar(int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
    print("Sirviendo en", url, "(Ctrl+C para salir)")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        srv.shutdown()
