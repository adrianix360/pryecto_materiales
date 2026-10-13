# Utilidades compartidas para construir el contenido del tema 3.
# Cada referencia de fuente es un dict {"doc": código, "pag": página del PDF, "impresa": opcional}.

FUENTES = {
    "01": {"archivo": "fuentes/1.  (Agua en el concreto) Fuente PCA.pdf", "titulo": "PCA, Diseño y Control de Mezclas de Concreto, cap. 4: Agua de mezcla (págs. impresas 95–100)", "autor": "Kosmatka et al. (PCA, 2004)", "del_profe": False},
    "03": {"archivo": "fuentes/220301  Introducción al concreto.pdf", "titulo": "Introducción al concreto hidráulico (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "04": {"archivo": "fuentes/220301 Tipos de materiales.pdf", "titulo": "Tipos de materiales estructurales (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "05": {"archivo": "fuentes/230317  Agua para el concreto Calidad y Cantidad Parte 1.pdf", "titulo": "Agua para el concreto: calidad y cantidad, parte 1 (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "06": {"archivo": "fuentes/230324  Agua para el concreto Calidad y Cantidad Parte 2.pdf", "titulo": "Agua para el concreto: cantidad, parte 2 (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "20": {"archivo": "fuentes/Exudación y contracción del concreto (Navas, A).pdf", "titulo": "Exudación, contracción y aire incluido (apuntes, cap. 4)", "autor": "Ing. Alejandro Navas", "del_profe": False},
    "25": {"archivo": "fuentes/Tolerancias Impurezas.pdf", "titulo": "Tabla de tolerancias de impurezas en el agua", "autor": "Material del curso", "del_profe": True},
    "02": {"archivo": "fuentes/2. Grupo B (Agregados, características).pdf", "titulo": "PCA, Diseño y Control de Mezclas de Concreto, cap. 5 (págs. impresas 113–117)", "autor": "Kosmatka et al. (PCA, 2004)", "del_profe": False},
    "09": {"archivo": "fuentes/3. Grupo C (Agregados, resistencia).pdf", "titulo": "PCA, cap. 5 (págs. impresas 117–119)", "autor": "Kosmatka et al. (PCA, 2004)", "del_profe": False},
    "10": {"archivo": "fuentes/4. Grupo D (Materiales perjudiciales).pdf", "titulo": "PCA, cap. 5 (págs. impresas 119–122 y 126–128)", "autor": "Kosmatka et al. (PCA, 2004)", "del_profe": False},
    "11": {"archivo": "fuentes/5. Grupo F (Agregados) Fuente PCA.pdf", "titulo": "PCA, cap. 5 (págs. impresas 106–113)", "autor": "Kosmatka et al. (PCA, 2004)", "del_profe": False},
    "12": {"archivo": "fuentes/ACI 116R-00 Cement and Concrete Terminology.pdf", "titulo": "ACI 116R-00, Cement and Concrete Terminology", "autor": "ACI", "del_profe": False},
    "13": {"archivo": "fuentes/Agregados Vol y Masas.pdf", "titulo": "Agregados: Volúmenes y masas (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "14": {"archivo": "fuentes/Agregados clasificación.pdf", "titulo": "Agregados: Clasificación (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "15": {"archivo": "fuentes/Agregados importancia.pdf", "titulo": "Agregados: Importancia (presentación)", "autor": "Ing. Einer Rodríguez Rojas", "del_profe": True},
    "16": {"archivo": "fuentes/AnÃ¡lisis granulomÃ©trico, Navas.pdf", "titulo": "Análisis granulométrico (apuntes, cap. 2)", "autor": "Ing. Alejandro Navas", "del_profe": False},
    "17": {"archivo": "fuentes/Curso_ II - S - 2026 - RRF - Laboratorio Materiales Construcción - 051 052 053 054 055 056 _ Mediación Virtual 2.pdf", "titulo": "Manual de Laboratorio, módulo de cementos (solo las normas de mortero)", "autor": "Ing. Flor Muñoz Umaña e Ing. Einer Rodríguez Rojas", "del_profe": True},
    "19": {"archivo": "fuentes/Curso_ II - S - 2026 - RRF - Laboratorio Materiales Construcción - 051 052 053 054 055 056 _ Mediación Virtual.pdf", "titulo": "Manual de Laboratorio, módulo de agregados", "autor": "Ing. Flor Muñoz Umaña e Ing. Einer Rodríguez Rojas", "del_profe": True},
    "22": {"archivo": "fuentes/MÃ³dulo de finura.pdf", "titulo": "Tabla de clasificación por módulo de finura", "autor": "Material del curso", "del_profe": True},
    "24": {"archivo": "fuentes/Propiedadees de agregados, Navas.pdf", "titulo": "Propiedades de los agregados (apuntes, cap. 2)", "autor": "Ing. Alejandro Navas", "del_profe": False},
    "26": {"archivo": "fuentes/UCR-Conf-Ingenieria-26Ag26.pdf", "titulo": "Rocas como agregados pétreos para mezclas de concreto (conferencia)", "autor": "Geól. Fernando Alvarado Villalón", "del_profe": False},
    "08": {"archivo": "fuentes/260517 Primer Parcial - SOLUC TEORIA.docx - Documentos de Google.pdf", "titulo": "I examen parcial, I-2026 (teoría, con clave)", "autor": "Curso IC-0604", "del_profe": True},
    "X01": {"archivo": "fuentes/examenes/Teoría examen _250523_233656 1_261009_135719.pdf", "titulo": "Recopilación: cuestionario de Mediación Virtual y claves", "autor": "Curso IC-0604", "del_profe": True},
    "X02": {"archivo": "fuentes/examenes/Solución Parte Teorica .pdf", "titulo": "I examen parcial, I-2025 (teoría, con clave)", "autor": "Curso IC-0604", "del_profe": True},
    "X04": {"archivo": "fuentes/examenes/Examen semestre 2-Teoría-Desarrollo corto con respuestas IIS.2022.pdf", "titulo": "I examen parcial, II-2022 (teoría y desarrollo corto)", "autor": "Curso IC-0604", "del_profe": False},
    "X06": {"archivo": "fuentes/examenes/Examen Parcial # 1 _ Teoria (Valor total 40 _).pdf", "titulo": "I examen parcial, I-2020 (cuestionario de teoría)", "autor": "Curso IC-0604", "del_profe": False},
    "X14": {"archivo": "fuentes/examenes/I Parcial. I-2009.pdf", "titulo": "I examen parcial, I-2009 (teoría, respuesta de un estudiante sin clave)", "autor": "Curso IC-0604 (Ing. Flor Muñoz)", "del_profe": False},
    "X15": {"archivo": "fuentes/examenes/I Parcial. II-2009.pdf", "titulo": "I examen parcial, II-2009 (respuesta de un estudiante sin clave)", "autor": "Curso IC-0604 (Ing. Flor Muñoz)", "del_profe": False},
    "X07": {"archivo": "fuentes/examenes/Primer examen IC 2020 (capturas)/", "titulo": "I examen, I-2020 (capturas del cuestionario)", "autor": "Curso IC-0604", "del_profe": False},
}

# Paginación de la PCA: página impresa -> (documento, página del PDF)
_PCA = {106: ("11", 1), 107: ("11", 2), 108: ("11", 3), 109: ("11", 4), 110: ("11", 5), 111: ("11", 6),
        112: ("11", 7), 113: ("02", 1), 114: ("02", 2), 115: ("02", 3), 116: ("02", 4), 117: ("02", 5),
        118: ("09", 2), 119: ("09", 3), 120: ("10", 2), 121: ("10", 3), 122: ("10", 4), 126: ("10", 5),
        127: ("10", 6), 128: ("10", 7)}


def S(doc, pag, impresa=None):
    d = {"doc": doc, "pag": pag}
    if impresa:
        d["impresa"] = str(impresa)
    return d


def pca(impresa):
    doc, pag = _PCA[impresa]
    return S(doc, pag, impresa)


def navas24(n):  # apuntes Navas, propiedades: pág. impresa 2/3 = PDF 1
    return S("24", n - 2, f"2/{n}")


def navas16(n):  # apuntes Navas, granulometría: pág. impresa 2/17 = PDF 1
    return S("16", n - 16, f"2/{n}")


def E(doc, pag, pregunta):
    """Referencia a una pregunta de examen."""
    return {"doc": doc, "pag": pag, "pregunta": pregunta}


def pca4(impresa):  # PCA cap. 4: pág. impresa 95 = PDF 1
    return S("01", impresa - 94, impresa)


def navas20(n):  # apuntes Navas, exudación: pág. impresa 4/6 = PDF 1
    return S("20", n - 5, f"4/{n}")
