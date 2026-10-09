"""Obsoleto: usar tools/contenido/construir.py (construye los tres temas)."""
import runpy, os
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "construir.py"), run_name="__main__")
