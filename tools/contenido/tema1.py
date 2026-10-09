"""Tema 1 — Introducción y definiciones básicas."""
from comun import S

T, P, G = [], [], []


def t(sub, tipo, frente, reverso, fuente, verificar=None):
    n = len(T) + 1
    d = {"id": f"t1-{sub}-{n:02d}", "tema": 1, "subtema": sub, "tipo": tipo, "frente": frente, "reverso": reverso, "fuente": fuente, "origen": "teoria"}
    if verificar:
        d["verificar"] = verificar
    T.append(d)


def q(sub, tipo, enunciado, explicacion, fuente, opciones=None, correcta=None, respuesta_modelo=None, puntos_clave=None):
    n = len(P) + 1
    d = {"id": f"p1-{sub}-t{n:02d}", "tema": 1, "subtema": sub, "tipo": tipo, "enunciado": enunciado, "origen": "teoria",
         "clave": "documental", "explicacion": explicacion, "fuente": fuente}
    if opciones:
        d["opciones"] = [{"id": chr(97 + i), "texto": o} for i, o in enumerate(opciones)]
        d["correcta"] = correcta
    if respuesta_modelo:
        d["respuesta_modelo"] = respuesta_modelo
        d["puntos_clave"] = puntos_clave
    P.append(d)


def g(termino, definicion, fuente, slug):
    G.append({"id": "g-" + slug, "termino": termino, "definicion": definicion, "tema": 1, "subtema": "1A", "fuente": fuente})


t("1A", "concepto", "¿Concreto y hormigón son lo mismo?", "Sí: son sinónimos (en inglés, concrete).", [S("03", 2), S("03", 3)])
t("1A", "concepto", "Definición de concreto (hormigón) según el ACI 116R",
  "Material compuesto que consiste esencialmente en un medio ligante dentro del cual hay partículas o fragmentos de agregado, generalmente una combinación de agregado fino y grueso. En el concreto de cemento portland, el ligante es una mezcla de cemento portland y agua.",
  [S("03", 3), S("12", 15)])
t("1A", "concepto", "Componentes del concreto",
  "Cemento, agregado fino (arena), agregado grueso (piedra) y agua; pueden añadirse aditivos y fibras.", [S("03", 3)])
t("1A", "concepto", "Definición de mortero según el ACI 116R",
  "Mezcla de pasta cementicia y agregado fino. En el concreto fresco, es el material que ocupa los intersticios entre las partículas de agregado grueso. En mampostería puede contener cemento de albañilería o cemento hidráulico y cal para lograr más plasticidad y trabajabilidad.",
  [S("03", 4), S("12", 43)])
t("1A", "concepto", "Definición de pasta cementicia pura según el ACI 116R",
  "Mezcla plástica de cemento hidráulico y agua, tanto antes como después de su fraguado y endurecimiento.", [S("03", 5), S("12", 13)])
t("1A", "concepto", "Diferencia entre pasta, mortero y concreto",
  "Pasta: cemento + agua.\nMortero: pasta + agregado fino.\nConcreto: pasta + agregado fino + agregado grueso.", [S("03", 3), S("03", 4), S("03", 5)])
t("1A", "concepto", "Formas de producir concreto",
  "En planta (concreto premezclado, transportado en camión mezclador) o en sitio (por ejemplo, con batidora).", [S("03", 6)])
t("1A", "norma", "Normas ACI que menciona el curso",
  "ACI 211: práctica para seleccionar el proporcionamiento (diseño de mezcla) de concreto normal, pesado y masivo.\nACI 318: código de construcción para concreto estructural.\nACI 522: especificaciones para pavimentos de concreto permeable.\nACI 116R: terminología del cemento y el concreto.",
  [S("03", 8), S("12", 1)], verificar="La lista de referencias de la presentación (03, pág. 9) le pone por error al ACI 116R-00 el título del ACI 211.")
t("1A", "clasificacion", "Clasificación de los materiales estructurales",
  "Se clasifican en metales, polímeros, cerámicos y compuestos.", [S("04", 5)])
t("1A", "concepto", "¿Por qué el concreto es un material compuesto?",
  "Porque combina un medio ligante (la pasta) con partículas de agregado embebidas en él.", [S("03", 3), S("12", 15)])

q("1A", "seleccion_unica", "Según el ACI 116R, el mortero es:",
  "Correcta la B. La A es la pasta, la C es el concreto y la D no corresponde a ninguna definición del curso.",
  [S("03", 4), S("12", 43)], ["Una mezcla de cemento hidráulico y agua", "Una mezcla de pasta cementicia y agregado fino",
                              "Una mezcla de pasta, agregado fino y agregado grueso", "Una mezcla de cal y agregado grueso"], "b")
q("1A", "seleccion_unica", "La «pasta cementicia pura» es:",
  "Correcta la A, según el ACI 116R. La B es el mortero y la C el concreto. La D es falsa porque la definición dice expresamente «antes y después de su fraguado».",
  [S("03", 5), S("12", 13)], ["Mezcla plástica de cemento hidráulico y agua, antes y después de su fraguado y endurecimiento",
                              "Mezcla de cemento, agua y arena", "Mezcla de cemento, agua, arena y piedra", "Solo el cemento y el agua antes del fraguado"], "a")
q("1A", "seleccion_unica", "En el concreto de cemento portland, el medio ligante es:",
  "Correcta la C. El agregado (A, B) es lo que queda embebido en el ligante, no el ligante. El aditivo (D) es opcional.",
  [S("03", 3)], ["El agregado grueso", "El agregado fino", "Una mezcla de cemento portland y agua", "El aditivo"], "c")
q("1A", "seleccion_unica", "¿Qué documento del ACI es el código de construcción para concreto estructural?",
  "Correcta la B. El ACI 211 (A) trata el proporcionamiento de mezclas, el ACI 522 (C) los pavimentos permeables y el ACI 116R (D) la terminología.",
  [S("03", 8)], ["ACI 211", "ACI 318", "ACI 522", "ACI 116R"], "b")
q("1A", "seleccion_unica", "¿Qué documento del ACI trata la selección del proporcionamiento de concreto de peso normal, pesado y masivo?",
  "Correcta la A. El ACI 318 (B) es el código estructural, el ACI 522 (C) los pavimentos permeables y el ACI 305 (D) el concreto en clima caluroso.",
  [S("03", 8), S("06", 8)], ["ACI 211", "ACI 318", "ACI 522", "ACI 305"], "a")
q("1A", "seleccion_multiple", "Marque los grupos en que se clasifican los materiales estructurales según la presentación del curso:",
  "Correctas la A, la B, la C y la E. La madera (D) no aparece como grupo en esa clasificación.",
  [S("04", 5)], ["Metales", "Polímeros", "Cerámicos", "Maderas", "Compuestos"], ["a", "b", "c", "e"])
q("1A", "respuesta_corta", "Explique la diferencia entre pasta, mortero y concreto.",
  "Se basa en las definiciones del ACI 116R de la presentación.", [S("03", 3), S("03", 4), S("03", 5)],
  respuesta_modelo="La pasta es cemento hidráulico con agua. El mortero es pasta con agregado fino. El concreto es un material compuesto de un ligante (pasta de cemento y agua) con agregado fino y grueso embebidos.",
  puntos_clave=["pasta = cemento + agua", "mortero = pasta + agregado fino", "concreto = pasta + agregado fino + agregado grueso"])
q("1A", "respuesta_corta", "Defina concreto según el ACI 116R.",
  "Definición textual de la presentación.", [S("03", 3), S("12", 15)],
  respuesta_modelo="Material compuesto formado por un medio ligante con partículas o fragmentos de agregado embebidos, generalmente fino y grueso; en el concreto de cemento portland el ligante es cemento portland y agua.",
  puntos_clave=["material compuesto", "medio ligante", "agregado fino y grueso embebido", "ligante: cemento portland + agua"])

g("Concreto (hormigón)", "Material compuesto de un medio ligante con partículas de agregado embebidas; en el concreto de cemento portland, el ligante es cemento y agua.", [S("03", 3), S("12", 15)], "concreto")
g("Mortero", "Mezcla de pasta cementicia y agregado fino.", [S("03", 4), S("12", 43)], "mortero")
g("Pasta cementicia pura", "Mezcla plástica de cemento hidráulico y agua, antes y después de su fraguado y endurecimiento.", [S("03", 5), S("12", 13)], "pasta-cementicia-pura")
g("ACI 318", "Código de construcción para concreto estructural.", [S("03", 8)], "aci-318")
g("ACI 211", "Práctica estándar para seleccionar el proporcionamiento de concreto de peso normal, pesado y masivo.", [S("03", 8)], "aci-211")
