"""Tema 2 — Agua para concreto: tarjetas, preguntas (examen y teoría) y glosario."""
from comun import S, E, pca4, navas20

T, P, G = [], [], []
VF = ["Verdadero", "Falso"]
I26, I25, II22, I20 = "I-2026", "I-2025", "II-2022", "I-2020"
X01P = "Sin fecha (cuestionario de Mediación Virtual)"


def t(sub, tipo, frente, reverso, fuente, verificar=None, figura=None):
    n = len([x for x in T if x["subtema"] == sub]) + 1
    d = {"id": f"t2-{sub}-{n:02d}", "tema": 2, "subtema": sub, "tipo": tipo, "frente": frente, "reverso": reverso,
         "fuente": fuente, "origen": "teoria"}
    if verificar:
        d["verificar"] = verificar
    if figura:
        d["figura"] = figura
    T.append(d)


def q(sub, tipo, enunciado, explicacion, fuente, origen="teoria", examen=None, periodo=None, opciones=None, correcta=None,
      respuesta_modelo=None, puntos_clave=None, clave=None, justificacion_oficial=None, verificar=None, figura=None):
    pref = "x" if origen == "examen" else "t"
    n = len([x for x in P if x["subtema"] == sub and x["origen"] == origen]) + 1
    d = {"id": f"p2-{sub}-{pref}{n:02d}", "tema": 2, "subtema": sub, "tipo": tipo, "enunciado": enunciado,
         "origen": origen, "clave": clave or ("oficial" if origen == "examen" else "documental"),
         "explicacion": explicacion, "fuente": fuente}
    if examen:
        d["examen"] = dict(examen, periodo=periodo)
    if opciones is not None:
        d["opciones"] = [{"id": chr(97 + i), "texto": o} for i, o in enumerate(opciones)]
        d["correcta"] = correcta
    if respuesta_modelo:
        d["respuesta_modelo"] = respuesta_modelo
        d["puntos_clave"] = puntos_clave
    for k, v in (("justificacion_oficial", justificacion_oficial), ("verificar", verificar), ("figura", figura)):
        if v:
            d[k] = v
    P.append(d)


def g(termino, definicion, fuente, sub):
    import unicodedata
    slug = unicodedata.normalize("NFKD", termino.lower()).encode("ascii", "ignore").decode()
    slug = "".join(c if c.isalnum() else "-" for c in slug).strip("-")
    G.append({"id": "g-" + slug, "termino": termino, "definicion": definicion, "tema": 2, "subtema": sub, "fuente": fuente})


# ======================== TARJETAS 2A · Calidad ========================
t("2A", "concepto", "¿Qué agua sirve, en principio, para hacer concreto?",
  "Prácticamente cualquier agua natural potable y sin sabor u olor fuerte. Algunas aguas no potables también sirven, pero hay que verificar su desempeño.",
  [pca4(95)])
t("2A", "concepto", "¿Qué parámetros del agua deben cumplir límites?",
  "El pH, los aceites, las sales, y los limos y la materia orgánica.", [S("05", 2)])
t("2A", "concepto", "Sulfatos en el agua de mezcla",
  "Son sales del ácido sulfúrico y una base (SO₄). Pueden provocar reacciones expansivas en el concreto.", [S("05", 3), pca4(97)])
t("2A", "concepto", "Carbonatos y bicarbonatos de sodio y potasio",
  "El carbonato de sodio puede causar fraguado rápido. Los bicarbonatos pueden acelerar o retardar el fraguado. Si la suma de sales disueltas supera 1000 ppm, hay que ensayar su efecto en la resistencia y el fraguado.",
  [S("05", 3), pca4(97)])
t("2A", "concepto", "Cloruros en el agua de mezcla",
  "Atacan la capa de óxido que protege al acero, que se forma por la alta alcalinidad del concreto (pH mayor que 12,5), y provocan corrosión del refuerzo. Son la sal que más preocupa en el concreto reforzado.",
  [S("05", 3), pca4(97)])
t("2A", "concepto", "Dureza del agua",
  "Es un indicador del contenido de sales; se caracteriza principalmente por el contenido de calcio y magnesio, y se expresa como CaCO₃.",
  [S("05", 3)])
t("2A", "concepto", "Problemas asociados a las sales de calcio y magnesio",
  "Con el agua producen eflorescencias y expansiones.", [S("05", 5)])
t("2A", "norma", "Normas ASTM sobre el agua de mezcla",
  "ASTM C1602: especificación del agua de mezcla para concreto (requisitos).\nASTM C1603: medición de sólidos en el agua.\nASTM C114: métodos de análisis químico (se usa para cloruros y sulfatos).",
  [S("05", 7), S("05", 8)])
t("2A", "dato", "Límites químicos del agua de mezcla (ASTM C1602), según la presentación",
  "Sulfato como SO₄: 3 000 ppm (método ASTM C114).\nÁlcalis: 600 ppm.\nSólidos totales: 5 000 ppm (ASTM C1603).\nCloruro: ver la tabla de tolerancias (ASTM C114).",
  [S("05", 8)], verificar="La PCA (Tabla 4-4, pág. 96) da 50 000 ppm de sólidos totales; la presentación dice 5 000. Se usa el valor del profe.")
t("2A", "criterio", "Criterios para aceptar un agua dudosa (no potable)",
  "Resistencia a compresión de cubos de mortero (ASTM C109): al menos 90 % de la del control a los 7 días.\nTiempo de fraguado (ASTM C191): desde 1:00 h antes hasta 1:30 h después que el control.\nEl control se hace con agua potable o destilada.",
  [S("05", 9), pca4(95), pca4(96)])
t("2A", "dato", "Tolerancias de impurezas: cloruros y sulfatos",
  "Cloruro de sodio: 20 000 ppm.\nCloruro como Cl⁻: 500 ppm en concreto preesforzado y 1000 ppm en concreto húmedo o con aluminio o metales galvanizados.\nSulfato de sodio: 10 000 ppm.\nSulfato como SO₄: 3 000 ppm.\nSulfato de magnesio: 25 000 ppm.",
  [S("25", 1)])
t("2A", "dato", "Tolerancias de impurezas: carbonatos y otras sales",
  "Carbonato de sodio y potasio: 1000 ppm.\nCarbonato de calcio y magnesio (como bicarbonato): 400 ppm.\nCloruro de magnesio: 40 000 ppm.\nSales de hierro: 40 000 ppm.\nYodato, fosfato y borato de sodio: 100 ppm.",
  [S("25", 1)])
t("2A", "dato", "Tolerancias de impurezas: pH, hidróxidos, azúcar, aceite, algas y materia orgánica",
  "pH: 6,5 a 8,5.\nHidróxido de sodio: 0,50 % del peso del cemento.\nHidróxido de potasio: 1,20 % del peso del cemento.\nAzúcar: 500 ppm.\nAceite mineral: 2 % del peso del cemento.\nAgua con algas: 0.\nMateria orgánica: 20 ppm.\nSólidos en suspensión en agua natural: 2 000 ppm.",
  [S("25", 1)], verificar="La PCA da otros valores para algas (1000 ppm, pág. 100), habla de hidróxido de calcio en vez de potasio (pág. 99) y fija el aceite mineral en 2,5 % (pág. 100). Se usa la tabla del curso.")
t("2A", "concepto", "Agua de mar",
  "Hasta 35 000 ppm de sales es adecuada para concreto SIN acero. No se recomienda para concreto reforzado ni preesforzado, por el riesgo de corrosión. También causa eflorescencias y manchas, y puede agravar la reacción álcali-agregado.",
  [S("25", 1), pca4(98), S("05", 10)])
t("2A", "concepto", "Aguas ácidas",
  "La PCA dice que las aguas con pH menor que 3,0 pueden crear problemas de manejo y se deben evitar si es posible. El pH neutro es 7; por debajo hay acidez y por encima alcalinidad.",
  [pca4(98)], verificar="El cuestionario del curso (X01, pág. 3) dice «menor a 3,5» y la tabla de tolerancias da un rango aceptable de 6,5 a 8,5 (contradicción C15).")
t("2A", "concepto", "Consecuencias del exceso de impurezas en el agua de mezcla",
  "Pueden afectar el tiempo de fraguado y la resistencia, y causar eflorescencias, manchado, corrosión del refuerzo, inestabilidad de volumen y menor durabilidad.",
  [pca4(96)])
t("2A", "concepto", "Algas en el agua",
  "Las aguas con algas no son adecuadas: reducen mucho la resistencia, por su efecto en la hidratación o porque incluyen mucho aire, y en los agregados reducen la adherencia. La tabla del curso tolera 0.",
  [pca4(100), S("25", 1)])
t("2A", "dato", "Límite de cloruros en el concreto según el ACI 318, citado por la PCA (% del peso de cemento)",
  "El ACI 318 limita los iones cloruro solubles en agua del concreto armado, en porcentaje del peso de cemento:\nPreesforzado: 0,06 %.\nReforzado expuesto a cloruros durante su vida: 0,15 %.\nReforzado que se mantendrá seco y protegido de la humedad: 1,00 %.\nOtras construcciones de concreto reforzado: 0,30 %.\nEn concreto simple (sin acero) el ACI 318 no limita los cloruros.\nOjo: este límite es del concreto y se da en % del cemento. La tabla de tolerancias del agua da ppm. Son bases distintas y no se comparan directamente.",
  [pca4(97)])

# ======================== TARJETAS 2B · Cantidad y comportamiento en estado fresco ========================
t("2B", "concepto", "Efecto de la relación a/c en la mezcla",
  "La presentación compara mezclas con a/c de 0,4, 0,6 y 0,8: a mayor a/c, mezcla más fluida y con más asentamiento. La relación a/c es una relación POR MASA.",
  [S("05", 11), S("06", 2), S("06", 10), E("X01", 4, "relacione a/c")])
t("2B", "dato", "Rangos de relación a/c según el cuestionario del curso",
  "Concreto convencional: 0,40 a 0,80.\nConcreto convencional con buena trabajabilidad: 0,55 a 0,60.\nRelación a/c necesaria para hidratar las partículas de cemento: 0,22.",
  [E("X01", 4, "preguntas 3 y 4")], verificar="Estos valores solo aparecen en la clave del cuestionario (fuente del profe); las fuentes de teoría no los desarrollan.")
t("2B", "concepto", "Exudación o sangrado",
  "Es la aparición de agua en la superficie del concreto después de consolidado y antes de la fragua. Las partículas sólidas (cemento y agregados) se asientan, no logran retener toda el agua y esta sube. Siempre ocurre, aunque a veces no se nota. Se mide con la ASTM C232.",
  [navas20(6), navas20(7), S("06", 4)])
t("2B", "concepto", "Efectos del sangrado excesivo",
  "Sube la relación a/c en la superficie (capa débil, porosa, propensa al desgaste y poco durable), aumenta la porosidad (canales), produce agrietamiento y reduce la adherencia, porque quedan bolsas de agua bajo el agregado y las varillas. En poca cantidad puede ayudar a controlar las fisuras por contracción plástica.",
  [navas20(6)])
t("2B", "concepto", "¿Cómo se reduce la exudación?",
  "Sobre todo reduciendo la relación a/c. También ayudan los cementos más finos, una buena graduación de los agregados, los agregados muy finos (pasando la No. 100), las puzolanas y los aditivos inclusores de aire.",
  [navas20(7)])
t("2B", "concepto", "Contracción del concreto en estado fresco: los dos tipos",
  "La contracción plástica y la contracción autógena.", [S("06", 6)])
t("2B", "concepto", "Contracción autógena",
  "Es la reducción de volumen causada por el consumo INTERNO de agua durante la hidratación del cemento. Es muy pequeña en concretos normales y significativa con a/c muy bajas (menores que 0,30). Para reducirla lo más importante es empezar el curado lo antes posible y mantenerlo al menos 7 días.",
  [navas20(7)])
t("2B", "concepto", "Contracción plástica",
  "Es el cambio de volumen mientras el concreto está plástico, por pérdida de agua debida a influencias EXTERNAS (exudación, formaletas, evaporación). Produce fisuras en la superficie antes o durante el acabado. Las superficies horizontales (losas y pavimentos) son las más propensas.",
  [navas20(7)])
t("2B", "concepto", "Medidas para reducir la contracción plástica",
  "Humedecer las formaletas y los agregados, empezar el curado rápido (a las 8 h), usar cobertores contra la evaporación, usar un sello de concreto pobre y saturar las superficies de contacto. La contracción plástica aumenta con el contenido de pasta y con la a/c.",
  [navas20(8)])
t("2B", "norma", "Tasa de evaporación y contracción plástica",
  "La tasa de evaporación se obtiene con el ábaco del ACI 305 (Guía para concretar en clima caluroso) a partir de la temperatura del aire, la humedad relativa, la temperatura del concreto y la velocidad del viento.",
  [S("06", 8)])
t("2B", "concepto", "Grietas por asentamiento plástico",
  "Aparecen sobre las barras de refuerzo y cerca de los elementos que restringen el movimiento: la restricción al asentamiento genera esfuerzos de tensión y fisuras.",
  [S("06", 7), E("X01", 6, "F/V 6")])
t("2B", "concepto", "Vibración del concreto",
  "Puede ser interna (vibrador de inmersión, eléctrico o con motor de gasolina) o externa (sobre las formaletas).", [S("06", 5)])
t("2B", "norma", "Normas de asentamiento",
  "ASTM C143: asentamiento del concreto convencional (cono).\nASTM C1611: flujo de asentamiento del concreto autocompactante.\nASTM C192: elaboración y curado de especímenes en el laboratorio.",
  [S("06", 9), S("06", 10)])
# ======================== PREGUNTAS DE EXAMEN ========================
q("2A", "verdadero_falso", "Las sales de carbonato pueden acelerar o retardar el fraguado del concreto",
  "Falso. El carbonato de sodio puede causar fraguado RÁPIDO; los que pueden acelerar o retardar son los bicarbonatos.",
  [pca4(97), S("05", 3)], "examen", E("08", 1, "1.1, caso 2"), I26, VF, "b",
  justificacion_oficial="Las sales de carbonato pueden causar fraguado rápido. Las de bicarbonato acelerar o retardar el fraguado")
q("2A", "verdadero_falso",
  "Al tener agua dudosa para fabricar concreto se puede utilizar la norma ASTM C109. Debe cumplir al menos un 90% de la resistencia a la compresión con el agua patrón al ensayar a los 14 días.",
  "Falso por la edad: la comparación del 90 % se hace a los 7 días, no a los 14.",
  [S("05", 9), pca4(96)], "examen", E("08", 1, "1.1, caso 4"), I26, VF, "b", justificacion_oficial="Se realiza la prueba a los 7 días")
q("2A", "respuesta_corta", "Indique la principal consecuencia de un exceso de sulfatos en el agua de una mezcla de concreto",
  "Las diapositivas del curso dicen que los sulfatos pueden provocar reacciones expansivas, y la PCA habla de reacciones expansivas y ataque de sulfatos. Por decisión de Adrián (contradicción C3), se usa «expansiones».",
  [S("05", 3), S("05", 5), pca4(97)], "examen", E("08", 2, "1.2, pregunta 1"), I26,
  respuesta_modelo="Reacciones expansivas (expansiones) y eflorescencias", puntos_clave=["reacciones expansivas", "eflorescencias"],
  verificar="La clave del examen dice «Eflorescencias y contracciones»; las diapositivas dicen expansiones (contradicción C3).")
q("2B", "respuesta_corta", "Explique la causa de la exudación del concreto",
  "Coincide con la definición de Navas.", [navas20(6)], "examen", E("08", 2, "1.2, pregunta 2"), I26,
  respuesta_modelo="Las partículas sólidas de la mezcla (cemento y agregados) se asientan, no pueden retener el agua y esta sube a la superficie",
  puntos_clave=["las partículas sólidas se asientan", "no retienen el agua", "el agua sube a la superficie"])
q("2B", "respuesta_corta", "Explique que es la contracción autógena del concreto",
  "Coincide con Navas: la clave es que el consumo de agua es INTERNO, por la hidratación.", [navas20(7)], "examen", E("08", 2, "1.2, pregunta 3"), I26,
  respuesta_modelo="Reducción de volumen causada por el consumo interno de agua en la hidratación del concreto",
  puntos_clave=["reducción de volumen", "consumo interno de agua", "hidratación del cemento"])
q("2A", "respuesta_corta", "Que indica principalmente el término de dureza del agua",
  "La dureza se caracteriza por el contenido de calcio y magnesio, expresado como CaCO₃.", [S("05", 3)], "examen", E("08", 2, "1.2, pregunta 4"), I26,
  respuesta_modelo="Indica el contenido de calcio y magnesio", puntos_clave=["calcio", "magnesio"])

q("2A", "seleccion_unica", "¿Cuál es el límite máximo de sulfatos como SO₄ en el agua de mezcla? (1 puntos)",
  "Correcta la B: 3 000 ppm. La A (600 ppm) es el límite de los álcalis, la C (5 000 ppm) el de los sólidos totales en la presentación y la D (10 000 ppm) el del sulfato de sodio en la tabla de tolerancias.",
  [S("05", 8), S("25", 1)], "examen", E("X02", 1, "1, pregunta 1"), I25, ["600 ppm", "3 000 ppm", "5 000 ppm", "10 000 ppm"], "b")
q("2B", "seleccion_unica", "¿Qué efecto produce el sangrado excesivo? (1 puntos)",
  "Correcta la B: el flujo de agua no uniforme provoca cambios de volumen diferenciales y fisuras, y además crea una capa superficial débil. La A está al revés (disminuye la adherencia). La C y la D no son efectos del sangrado.",
  [navas20(6)], "examen", E("X02", 1, "1, pregunta 2"), I25, ["Aumento de adherencia", "Grietas en superficie", "Reducción de tensión", "Homogeneidad mejorada"], "b")
q("2B", "seleccion_unica", "¿Qué práctica reduce la contracción plástica según la presentación? (1 puntos)",
  "Correcta la B. La A empeora la contracción plástica, que aumenta con la a/c. Retardar el curado (D) también la empeora, porque el curado debe empezar rápido. La C no aparece como medida.",
  [navas20(8)], "examen", E("X02", 1, "1, pregunta 3"), I25,
  ["Aumentar la relación a/c", "Humedecer formaletas y agregados", "Usar aditivo homogenizante", "Retardar el curado"], "b")
q("2B", "seleccion_unica", "¿Qué medida reduce la exudación? (1 puntos)",
  "Correcta la B. Aumentar la a/c (A) la empeora. El agua destilada (C) y reducir el curado (D) no son medidas para la exudación.",
  [navas20(7)], "examen", E("X02", 1, "1, pregunta 4"), I25,
  ["Aumentar relación agua/cemento", "Usar cementos más finos", "Emplear agua destilada", "Reducir el curado"], "b")
q("2A", "verdadero_falso", "Si va a diseñar una planta de tratamiento para aguas residuales, debe revisar los límites permitidos de sales de Cloruro",
  "Falso según la clave: la sal que hay que revisar son los sulfatos.", [], "examen", E("X02", 2, "2, caso 2"), I25, VF, "b",
  justificacion_oficial="Sulfatos",
  verificar="Las fuentes de teoría no tratan las plantas de tratamiento; la respuesta se apoya solo en la clave. La PCA (pág. 97) asocia los sulfatos con el ataque al concreto expuesto a suelos o aguas con sulfatos.")
q("2B", "verdadero_falso", "El documento que permite obtener la tasa de evaporación es la ASTM C 305",
  "Falso: es el ACI 305 (Guía para concretar en clima caluroso). La ASTM C305 es la práctica de mezclado mecánico de pastas y morteros.",
  [S("06", 8)], "examen", E("X02", 2, "2, caso 3"), I25, VF, "b", justificacion_oficial="ACI 305")
q("2B", "respuesta_corta", "¿Qué es la contracción autógena?", "Coincide con Navas.", [navas20(7)], "examen", E("X02", 3, "3, pregunta 1"), I25,
  respuesta_modelo="Reducción de volumen de la mezcla de concreto por consumo interno de agua", puntos_clave=["reducción de volumen", "consumo interno de agua"])
q("2B", "respuesta_corta", "Defina el térmico de exudación en el concreto", "Coincide con Navas.", [navas20(6)], "examen", E("X02", 3, "3, pregunta 3"), I25,
  respuesta_modelo="Las partículas sólidas de la mezcla (cemento, agregados) se asientan y son incapaces de retener toda el agua",
  puntos_clave=["las partículas sólidas se asientan", "no retienen el agua", "el agua sube a la superficie"])
q("2A", "respuesta_corta", "Indique el método estándar para analizar químicamente el agua",
  "La ASTM C114 es el método de análisis químico que la presentación asocia a los cloruros y los sulfatos. La C1602 fija los requisitos, pero no define métodos analíticos.",
  [S("05", 7), S("05", 8)], "examen", E("X02", 3, "3, pregunta 5"), I25, respuesta_modelo="ASTM C114", puntos_clave=["ASTM C114"])
q("2B", "respuesta_corta", "¿Qué es la contracción plástica?", "Coincide con Navas.", [navas20(7)], "examen", E("X02", 3, "3, pregunta 10"), I25,
  respuesta_modelo="Es el cambio de volumen que ocurre mientras el concreto está en estado plástico debido a perdida de agua por influencias externas.",
  puntos_clave=["cambio de volumen", "estado plástico", "pérdida de agua por influencias externas"])

for preg, resp, expl, fu in [
    ("Sal contenida en el agua que puede provocar reacciones expansivas (Valor: 1 punto)", "Calcio, magnesio o sulfatos",
     "La clave acepta calcio, magnesio o sulfatos. Las sales de calcio y magnesio producen eflorescencias y expansiones, y los sulfatos reacciones expansivas.", [S("05", 3), S("05", 5)]),
    ("Sal contenida en el agua que puede acelerar o retardar el fraguado (Valor: 1 punto)", "Bicarbonatos",
     "Los bicarbonatos pueden acelerar o retardar el fraguado; el carbonato de sodio causa fraguado rápido.", [S("05", 3), pca4(97)]),
    ("Sal contenida en el agua que puede provocar corrosión (Valor: 1 punto)", "Cloruros",
     "Los cloruros atacan la capa protectora del acero.", [S("05", 3), pca4(97)])]:
    q("2A", "respuesta_corta", "Complete (sólo puede indicar una respuesta en cada cuadro, si indica más de una la respuesta es inválida): " + preg,
      expl, fu, "examen", E("X04", 1, "Parte 1a, cuadro de sales"), II22, respuesta_modelo=resp, puntos_clave=[resp])
q("2B", "respuesta_corta",
  "Contracciones del concreto fresco. Uno de los tipos es: contracción plástica. Indique por qué se provoca y una forma de evitarla.",
  "La clave del examen coincide con Navas: la contracción plástica se debe a la pérdida de agua por influencias externas.", [navas20(7), navas20(8), S("06", 8)],
  "examen", E("X04", 1, "Parte 1a, cuadro de contracciones"), II22,
  respuesta_modelo="Se provoca por la tasa de evaporación del agua de la superficie o por la pérdida de agua por factores externos (exudación, formaletas). Se evita controlando la temperatura y la humedad ambiental, controlando la temperatura del concreto o con vibración.",
  puntos_clave=["evaporación o pérdida de agua por factores externos", "control de la temperatura y la humedad (curado y protección)"])
q("2B", "respuesta_corta",
  "Contracciones del concreto fresco. Uno de los tipos es: contracción autógena. Indique por qué se provoca y una forma de evitarla.",
  "La clave acepta «consumo interno de agua al hidratar» y, para evitarla, el curado o reducir la a/c. Navas indica que lo más importante es curar pronto y al menos 7 días.",
  [navas20(7)], "examen", E("X04", 1, "Parte 1a, cuadro de contracciones"), II22,
  respuesta_modelo="Se provoca por el consumo interno de agua al hidratarse el cemento (también se acepta: esfuerzos de tensión por restricciones). Se evita con curado (iniciarlo pronto y mantenerlo al menos 7 días), reduciendo la a/c o con vibración.",
  puntos_clave=["consumo interno de agua en la hidratación", "curado temprano"])
q("2B", "verdadero_falso", "En poca cantidad, el sangrado puede ayudar a controlar las fisuras por contracción plástica",
  "Verdadero, lo dice Navas.", [navas20(6)], "examen", E("X04", 2, "Parte 1a, F/V 1"), II22, VF, "a")
q("2B", "verdadero_falso", "Las superficies verticales como paredes y muros suelen ser los más propensos a sufrir contracción plástica",
  "Falso: las más propensas son las superficies horizontales (pavimentos y losas), por la rápida evaporación.", [navas20(7)],
  "examen", E("X04", 2, "Parte 1a, F/V 2"), II22, VF, "b",
  justificacion_oficial="Las superficies horizontales, como pavimentos y losas suelen ser los más propensos a sufrir contracción plástica")

q("2A", "seleccion_unica", "Si Usted en su proyecto no dispone de agua potable, puede usar agua del sitio en primera instancia, si previamente:",
  "Correcta la B: el agua dudosa se puede usar si se verifica que cumple los criterios (C1602 y los ensayos de resistencia y fraguado). La A y la D son tratamientos que no garantizan el cumplimiento, y la C no usa el agua del sitio.",
  [pca4(95), S("05", 9)], "examen", E("X06", 1, "Pregunta 3"), I20,
  ["Filtra el agua en depósitos arenosos", "Evalúa la calidad de agua y compara con los parámetros de aceptación de las normas",
   "Transporta el agua potable del lugar mas cercano", "Coloca cloro en el agua"], "b")
q("2B", "respuesta_corta", "Refierase a la relación agua / Cemento en el concreto y por qué su importancia",
  "El comentario del profesor en la clave fue «Ley de Abrams, es por masa». La respuesta modelo se armó con las fuentes del curso.",
  [S("05", 11), S("06", 10), navas20(7), navas20(8), E("X01", 4, "relacione a/c")], "examen", E("X06", 2, "Pregunta 4"), I20,
  respuesta_modelo="Es la relación POR MASA entre el agua y el cemento. A mayor a/c, la mezcla es más fluida y trabajable, pero menos resistente (ley de Abrams), con más exudación y más contracción plástica. En el concreto convencional va de 0,40 a 0,80.",
  puntos_clave=["relación por masa", "mayor a/c → menos resistencia (ley de Abrams)", "mayor a/c → más trabajabilidad", "rango usual de 0,40 a 0,80"], clave="documental",
  verificar="La ley de Abrams solo aparece en el comentario de la clave; las fuentes de teoría no la explican.")
q("2B", "verdadero_falso",
  "Si se emplea, por ejemplo, un saco de cemento por batida, la relación agua cemento es el valor obtenido al dividir la cantidad de agua que se dosifica por saco de cemento entre la cantidad de cemento en masa",
  "Falso. La relación a/c usa el agua de DISEÑO; solo coincide con el agua dosificada si los agregados están en condición SSS.",
  [S("13", 9)], "examen", E("X06", 3, "Pregunta 7"), I20, VF, "b",
  justificacion_oficial="Es el agua de diseño. Solo sería posible si los agregados están en condición SSS, porque Wdiseño=Wdosificación.")
q("2A", "seleccion_unica", "El agua cumple tres funciones en el concreto hidráulico, a saber:",
  "Correcta la A según la clave. La B, la C y la E nombran solo una parte de la función química, y la D no aplica.",
  [], "examen", E("X07", 1, "captura 1, pregunta 2"), I20,
  ["Creación de enlaces, proveer trabajabilidad a la mezcla y disponer de los espacios para los productos de las reacciones",
   "Suplir los enlaces químicos", "Junto con el cemento reacciona y crea los enlaces", "Ninguna de las anteriores", "Reaccionar con el cemento y los aditivos"], "a",
  verificar="Las fuentes de teoría no enumeran las tres funciones del agua; la respuesta se apoya solo en la clave.")

q("2A", "seleccion_unica", "Evitar aguas acidas con un pH menor a:",
  "La clave da 3.5. La PCA dice pH menor que 3,0, y la tabla del curso da un rango aceptable de 6,5 a 8,5.",
  [pca4(98), S("25", 1)], "examen", E("X01", 3, "pregunta 4"), X01P, ["9", "6", "3.5", "4.5"], "c",
  verificar="Contradicción C15: el cuestionario dice 3,5, la PCA 3,0 y la tabla del curso 6,5–8,5.")
q("2A", "seleccion_unica", "La sal que principalmente perjudica la corrosion del acero de refuerzo es:",
  "Correcta la B: los cloruros atacan la capa protectora del acero. Las sales de magnesio (A) causan eflorescencias y expansiones, y las de sodio y potasio (C, D) afectan el fraguado.",
  [pca4(97), S("05", 3)], "examen", E("X01", 3, "pregunta 5"), X01P, ["Sal de magnesio", "Sal de cloruro", "Sal de potasio", "Sal de sodio"], "b")
q("2A", "seleccion_multiple", "Elija las opciones correctas\nEl exceso de impurezas en el agua de mezcla puede:",
  "Correctas la B, la C y la E: las impurezas afectan el fraguado, causan eflorescencias y corrosión. La A y la D son efectos contrarios a los reales.",
  [pca4(96)], "examen", E("X01", 4, "pregunta 1"), X01P,
  ["Aumentar la resistencia del concreto", "Disminuir o adelantar el tiempo de fraguado", "Causar eflorescencias", "Aumentar la durabilidad", "Puede causar corrosión en elementos reforzados"],
  ["b", "c", "e"])
q("2A", "verdadero_falso", "Responda verdadero o falso\nUna alta alcalinidad corresponde a un valor de pH de 9.5",
  "Falso según la clave: la alta alcalinidad del concreto corresponde a un pH superior a 12,5.",
  [pca4(97), S("05", 3)], "examen", E("X01", 4, "pregunta 2"), X01P, VF, "b", justificacion_oficial="Superior a 12,5",
  verificar="En la captura, el «9,5» del enunciado está tachado a mano y reemplazado por «mayor a 12,5»; se usa el enunciado original.")
q("2B", "respuesta_corta", "La relación agua/cemento necesaria para hidratar las partículas de cemento es de\nSolo coloque los números separados por coma. Ejemplo: 0,99",
  "Respuesta de la clave del cuestionario.", [], "examen", E("X01", 4, "pregunta 3"), X01P, respuesta_modelo="0,22", puntos_clave=["0,22"],
  verificar="El valor 0,22 no aparece en las fuentes de teoría; solo en esta clave.")
q("2B", "respuesta_corta",
  "Relacione los siguientes conceptos: (1) Rango aceptable de relación a/c para un concreto convencional con buena trabajabilidad; (2) Rango aceptable de relación a/c para un concreto convencional; (3) a/c. Opciones: 0,40 a 0,80 · 0,55 a 0,60 · Corresponde a una relación por masa",
  "Respuesta de la clave del cuestionario (pregunta de emparejamiento).", [], "examen", E("X01", 4, "pregunta 4"), X01P,
  respuesta_modelo="(1) 0,55 a 0,60; (2) 0,40 a 0,80; (3) corresponde a una relación por masa",
  puntos_clave=["buena trabajabilidad: 0,55 a 0,60", "convencional: 0,40 a 0,80", "relación por masa"],
  verificar="Los rangos solo aparecen en esta clave.")
q("2B", "respuesta_corta",
  "Relaciones conceptos: (1) Aumento de a/c en la superficie; (2) Poca cantidad de exudación; (3) Debido a agua atrapada en el acero de refuerzo. Opciones: Causa superficie débil de fácil desgaste · Puede colaborar al control de grietas por contracción plástica · Disminución de la adherencia",
  "Coincide con los efectos del sangrado que describe Navas.", [navas20(6)], "examen", E("X01", 4, "pregunta 5"), X01P,
  respuesta_modelo="(1) Causa superficie débil de fácil desgaste; (2) puede colaborar al control de grietas por contracción plástica; (3) disminución de la adherencia",
  puntos_clave=["a/c en la superficie → capa débil", "poca exudación → ayuda con la contracción plástica", "agua bajo el acero → menos adherencia"])
q("2B", "respuesta_corta", "El asentamiento de un concreto convencional se realiza por medio de la norma ASTM C ___ Indique el número. Ejemplo: 35",
  "ASTM C143 (cono de asentamiento).", [S("06", 9), S("06", 10)], "examen", E("X01", 5, "pregunta 1"), X01P, respuesta_modelo="143", puntos_clave=["C143"])
q("2B", "respuesta_corta", "El asentamiento de un concreto autocompactante se realiza por medio de la norma ASTM C ___ Indique el número. Ejemplo: 35",
  "ASTM C1611 (flujo de asentamiento del concreto autocompactante).", [S("06", 9)], "examen", E("X01", 5, "pregunta 2"), X01P, respuesta_modelo="1611", puntos_clave=["C1611"])
q("2B", "verdadero_falso",
  "Considere las siguientes condiciones para una losa de pavimento.\nTemperatura del aire: 25°C\nHumedad relativa: 60%\nTemperatura del concreto: 32°C\nVelocidad del viento: 32km/hr\nSegún el ingeniero a cargo, no hay problemas de contracción plástica.\nIndique si es verdadero o falso",
  "Falso según la clave. Con el ábaco del ACI 305 se entra con la temperatura del aire y la humedad relativa, luego con la temperatura del concreto y después con la velocidad del viento; esas condiciones dan una tasa de evaporación alta, con riesgo de contracción plástica.",
  [S("06", 8)], "examen", E("X01", 5, "pregunta 5"), X01P, VF, "b",
  figura={"src": "img/examenes/X01-p5-abaco.jpg", "alt": "Ábaco de tasa de evaporación (ACI 305) incluido en la pregunta", "fuente": [S("X01", 5)]},
  verificar="La lectura exacta de la tasa de evaporación en el ábaco no está en la clave ni en las fuentes; se respeta el «Falso» de la clave.")
q("2B", "verdadero_falso",
  "Las grietas por asentamiento plástico aparecen sobre las barras de acero de refuerzo y cerca de elementos que restringen el movimiento",
  "Verdadero: la restricción al asentamiento genera esfuerzos de tensión y fisuras.", [S("06", 7)], "examen", E("X01", 6, "F/V 6"), X01P, VF, "a",
  justificacion_oficial="Porque imponen restricción a la contracción generando fisuras")
q("2B", "verdadero_falso",
  "Si se emplea, por ejemplo, un saco de cemento por batida, la relación agua cemento es el valor obtenido al dividir la cantidad de agua que se dosifica por saco de cemento entre la cantidad de cemento en masa",
  "Falso: la a/c es con el agua de diseño (igual al agua dosificada solo si los agregados están en SSS).", [S("13", 9)], "examen", E("X01", 6, "F/V 11"), X01P, VF, "b",
  justificacion_oficial="Es el agua de diseño. Solo sería posible si los agregados están en condición SSS, porque Wdiseño=Wdosificación.")
q("2B", "verdadero_falso", "El sangrado en forma excesiva disminuye la relación a/c de una mezcla de concreto en su superficie",
  "Falso: la AUMENTA en la superficie, y crea una capa débil y porosa.", [navas20(6)], "examen", E("X01", 7, "a, caso 3"), X01P, VF, "b",
  justificacion_oficial="Aumento de la relación w/c en la superficie: se crea una capa débil, porosa, propensa al desgaste y de poca durabilidad en la superficie")
q("2B", "verdadero_falso", "La contracción autógena es reducción de volumen causada por el consumo externo de agua durante la hidratación del cemento",
  "Falso: el consumo de agua es INTERNO.", [navas20(7)], "examen", E("X01", 7, "a, caso 4"), X01P, VF, "b",
  justificacion_oficial="La contracción autógena es reducción de volumen causada por el consumo interno de agua durante la hidratación del cemento")
q("2A", "respuesta_corta", "El tipo de sal que provoca mayor dificultad para eflorescencias y expansiones del concreto es:",
  "Las sales de calcio y magnesio producen eflorescencias y expansiones; la clave da las de magnesio.", [S("05", 5)], "examen", E("X01", 7, "b, pregunta 3"), X01P,
  respuesta_modelo="Sales de magnesio", puntos_clave=["magnesio"])
q("2A", "respuesta_corta", "Usted duda del tipo de agua para un proyecto. Como consultor, cual norma de laboratorio recomienda para verificar tolerancias químicas del agua",
  "La ASTM C1602 es la especificación del agua de mezcla y fija los límites químicos.", [S("05", 7), S("05", 8)], "examen", E("X01", 7, "b, pregunta 4"), X01P,
  respuesta_modelo="ASTM C 1602", puntos_clave=["ASTM C1602"])
q("2A", "verdadero_falso", "El método estándar para analizar químicamente el agua corresponde con la norma ASTM C1602",
  "Falso: la C1602 establece requisitos químicos y físicos, pero no define métodos analíticos; el análisis químico se hace con la ASTM C114.",
  [S("05", 8)], "examen", E("X01", 8, "F/V 3"), X01P, VF, "b",
  justificacion_oficial="Establece requisitos químicos y físicos, pero no define métodos analíticos (corrección a mano)")
q("2B", "verdadero_falso", "La norma que se utiliza para asentamiento de concreto autocompactante es la ASTM C1611",
  "Verdadero.", [S("06", 9)], "examen", E("X01", 8, "F/V 5"), X01P, VF, "a")
q("2A", "respuesta_corta",
  "El exceso de impurezas en el agua de mezcla no sólo puede afectar la resistencia del concreto, sino también puede causar eflorescencias, manchado, corrosión del refuerzo, instabilidad del volumen y reducción de la durabilidad. Indique otra consecuencia:",
  "La PCA dice que las impurezas también afectan el tiempo de fraguado.", [pca4(96)], "examen", E("X01", 8, "respuesta corta 1"), X01P,
  respuesta_modelo="Retardamiento del fraguado (afecta el tiempo de fraguado)", puntos_clave=["tiempo de fraguado"])
q("2B", "respuesta_corta",
  "Cuando las partículas sólidas de la mezcla (cemento, agregados) se asientan y son incapaces de retener toda el agua, se produce:",
  "Es la definición de exudación de Navas, de la clave de 2025 y de la de 2026.", [navas20(6)], "examen", E("X01", 8, "respuesta corta 3"), X01P,
  respuesta_modelo="Exudación (sangrado)", puntos_clave=["exudación o sangrado"],
  verificar="La corrección en rojo de este examen escribe «compactación por asentamiento» (contradicción C17).")
q("2B", "respuesta_corta",
  "Para reducirla lo más importante es iniciar el proceso de curado lo antes posible y mantenerlo al menos 7 días. La definición anterior se refiere al concepto de:",
  "La corrección en rojo del examen dice «contracción plástica». Sin embargo, Navas escribe esa misma frase, palabra por palabra, sobre la contracción AUTÓGENA.",
  [navas20(7)], "examen", E("X01", 8, "respuesta corta 4"), X01P,
  respuesta_modelo="Contracción plástica (según la corrección del examen); en Navas la frase corresponde a la contracción autógena",
  puntos_clave=["contracción (plástica según la clave; autógena según Navas)"],
  verificar="Contradicción nueva C18: la corrección dice contracción plástica y Navas (4/7) dice contracción autógena. Hay que consultarlo con el profe.")
q("2B", "respuesta_corta", "Indique el documento que permite obtener la tasa de evaporación",
  "El ábaco de tasa de evaporación es del ACI 305.", [S("06", 8)], "examen", E("X01", 8, "respuesta corta 5"), X01P,
  respuesta_modelo="ACI 305 R-99", puntos_clave=["ACI 305"])
q("2B", "respuesta_corta",
  "Aumento de la relación a/c en la superficie, agrietamiento, disminución de adherencia y resistencia son consecuencias negativas del sangrado, otra es:",
  "Navas también menciona el aumento de la porosidad y la capa superficial débil.", [navas20(6)], "examen", E("X01", 8, "respuesta corta 8"), X01P,
  respuesta_modelo="Capa débil que reduce la resistencia al desgaste y la durabilidad (también: aumento de la porosidad)",
  puntos_clave=["capa superficial débil", "menos resistencia al desgaste y menos durabilidad", "más porosidad"])

# ======================== PREGUNTAS NUEVAS (teoría) ========================
SU = "seleccion_unica"
q("2A", SU, "Según la tabla de tolerancias del curso, ¿cuál es la concentración máxima de cloruro (como Cl⁻) en el agua para concreto PREESFORZADO?",
  "Correcta la A: 500 ppm. La B (1000 ppm) es para concreto húmedo o con aluminio o metales galvanizados, la C es la del cloruro de sodio y la D la del cloruro de magnesio.",
  [S("25", 1)], opciones=["500 ppm", "1000 ppm", "20 000 ppm", "40 000 ppm"], correcta="a")
q("2A", SU, "El agua de mar (hasta 35 000 ppm de sales) puede usarse en:",
  "Correcta la C. En concreto reforzado o preesforzado (A, B) no se recomienda por la corrosión. La D es falsa porque el agua de mar puede agravar la reacción álcali-agregado.",
  [pca4(98), S("25", 1)], opciones=["Concreto reforzado", "Concreto preesforzado", "Concreto sin refuerzo", "Concreto con agregados potencialmente reactivos"], correcta="c")
q("2A", SU, "En el ensayo de aceptación de un agua dudosa, ¿qué norma se usa para el tiempo de fraguado?",
  "Correcta la B: ASTM C191 (desde 1:00 antes hasta 1:30 después del control). La A es la de resistencia de cubos, la C la de sólidos en el agua y la D la del análisis químico.",
  [S("05", 9), pca4(96)], opciones=["ASTM C109", "ASTM C191", "ASTM C1603", "ASTM C114"], correcta="b")
q("2A", SU, "¿Cuál es el límite de álcalis en el agua de mezcla según la presentación (ASTM C1602)?",
  "Correcta la A: 600 ppm. La B es la de sulfatos, la C la de sólidos totales y la D la del cloruro de sodio en la tabla de tolerancias.",
  [S("05", 8)], opciones=["600 ppm", "3 000 ppm", "5 000 ppm", "20 000 ppm"], correcta="a")
q("2A", SU, "Según la tabla de tolerancias del curso, el contenido máximo de azúcar en el agua es:",
  "Correcta la C: 500 ppm (coincide con la PCA). La A es la de yodato, fosfato y borato de sodio, la B la de los bicarbonatos de calcio y magnesio y la D la de los carbonatos de sodio y potasio.",
  [S("25", 1), pca4(99)], opciones=["100 ppm", "400 ppm", "500 ppm", "1000 ppm"], correcta="c")
q("2B", SU, "¿En qué tipo de elemento es más probable la contracción plástica?",
  "Correcta la B: en las superficies horizontales el agua se evapora rápido. Las otras opciones son superficies verticales o protegidas.",
  [navas20(7)], opciones=["Muros", "Losas y pavimentos", "Columnas", "Pilotes"], correcta="b")
q("2B", SU, "La contracción autógena es significativa cuando:",
  "Correcta la D: con a/c muy bajas (menores que 0,30). En concretos normales es muy pequeña. La A, la B y la C no son las condiciones que da la fuente.",
  [navas20(7)], opciones=["Hay viento fuerte", "La temperatura del aire es alta", "Hay mucha exudación", "La relación a/c es muy baja (< 0,30)"], correcta="d")
q("2B", SU, "¿Qué datos se necesitan para leer el ábaco de tasa de evaporación del ACI 305?",
  "Correcta la A: el ábaco usa la temperatura del aire, la humedad relativa, la temperatura del concreto y la velocidad del viento.",
  [S("06", 8)], opciones=["Temperatura del aire, humedad relativa, temperatura del concreto y velocidad del viento",
                          "Relación a/c, asentamiento y tipo de cemento", "Temperatura del concreto y espesor de la losa", "Humedad relativa y tiempo de curado"], correcta="a")
q("2B", SU, "¿Qué norma mide la exudación (sangrado) del concreto?",
  "Correcta la C: la ASTM C232. La A es la de asentamiento, la B la de flujo del autocompactante y la D la de elaboración de especímenes.",
  [S("06", 4)], opciones=["ASTM C143", "ASTM C1611", "ASTM C232", "ASTM C192"], correcta="c")
q("2B", SU, "¿Cuál es la PRINCIPAL forma de disminuir la exudación?",
  "Correcta la B. La A la aumenta. La C y la D no son medidas que menciona la fuente.",
  [navas20(7)], opciones=["Aumentar la relación a/c", "Reducir la relación a/c", "Vibrar más tiempo", "Usar agregado grueso de mayor tamaño"], correcta="b")
q("2B", "seleccion_multiple", "Marque las medidas que reducen la contracción plástica:",
  "Correctas la A, la B y la D. La C la empeora: la contracción plástica aumenta con el contenido de pasta y la a/c.",
  [navas20(8)], opciones=["Humedecer formaletas y agregados", "Iniciar el curado rápidamente", "Aumentar el contenido de pasta", "Usar cobertores para reducir la evaporación"],
  correcta=["a", "b", "d"])
RC = "respuesta_corta"
q("2A", RC, "Explique por qué preocupan los cloruros en el agua de mezcla.",
  "Lo dicen la PCA y la diapositiva del curso.", [pca4(97), S("05", 3)],
  respuesta_modelo="Porque los iones cloruro atacan la capa de óxido que protege al acero, formada por la alta alcalinidad del concreto (pH mayor que 12,5), y producen corrosión del refuerzo. Por eso los límites son más estrictos en concreto preesforzado.",
  puntos_clave=["atacan la capa protectora del acero", "pH > 12,5", "corrosión del refuerzo", "límite más estricto en preesforzado"])
q("2B", RC, "Diferencie la contracción plástica de la contracción autógena.",
  "Se resume de Navas.", [navas20(7)],
  respuesta_modelo="La plástica ocurre en estado plástico por pérdida de agua por influencias externas (evaporación, exudación, formaletas) y produce fisuras superficiales. La autógena se debe al consumo interno de agua por la hidratación del cemento y es significativa con a/c muy bajas.",
  puntos_clave=["plástica: pérdida de agua externa", "autógena: consumo interno por hidratación", "plástica: fisuras superficiales", "autógena: importa con a/c bajas"])
q("2A", RC, "¿Qué requisitos debe cumplir un agua no potable para aceptarse en concreto?",
  "Tabla de la ASTM C1602 en la presentación.", [S("05", 9), pca4(96)],
  respuesta_modelo="La resistencia de los cubos de mortero (C109) debe ser al menos el 90 % de la del control a los 7 días, y el tiempo de fraguado (C191) debe estar entre 1:00 h antes y 1:30 h después del control. El control se hace con agua potable o destilada.",
  puntos_clave=["≥ 90 % de resistencia a 7 días (C109)", "fraguado de 1:00 antes a 1:30 después (C191)", "control con agua potable o destilada"])

# --- Tabla de tolerancias (fuente 25): preguntas de práctica para memorizar sus valores ---
q("2A", SU, "Según la tabla de tolerancias del curso, ¿qué intervalo de pH se acepta en el agua para concreto?",
  "Correcta la A: de 6,5 a 8,5. Las otras opciones no son el intervalo de la tabla.",
  [S("25", 1)], opciones=["6,5 a 8,5", "4,0 a 6,0", "7,0 a 9,0", "8,5 a 10,5"], correcta="a")
q("2A", SU, "En la tabla de tolerancias del curso, ¿qué sustancia tiene un límite de 20 000 ppm?",
  "Correcta la C: el cloruro de sodio. El cloruro de magnesio tolera 40 000 ppm (A), el sulfato de sodio 10 000 ppm (B) y el cloruro de calcio se da aparte: 2 % del peso del cemento (D).",
  [S("25", 1)], opciones=["Cloruro de magnesio", "Sulfato de sodio", "Cloruro de sodio", "Cloruro de calcio"], correcta="c")
q("2A", SU, "En la tabla de tolerancias del curso, ¿qué sustancia tiene un límite de 400 ppm?",
  "Correcta la B: el carbonato de calcio y magnesio, medido como ion bicarbonato. El carbonato de sodio y potasio tolera 1000 ppm (A), el cloruro de magnesio 40 000 ppm (C) y el sulfato de magnesio 25 000 ppm (D).",
  [S("25", 1)], opciones=["Carbonato de sodio y potasio", "Carbonato de calcio y magnesio, como ion bicarbonato", "Cloruro de magnesio", "Sulfato de magnesio"], correcta="b")
q("2A", SU, "Según la tabla de tolerancias del curso, ¿cuánta materia orgánica se tolera en el agua?",
  "Correcta la A: 20 ppm. La B es la tolerancia del yodato, fosfato y borato de sodio, la C la del carbonato de calcio y magnesio (como bicarbonato) y la D la de los sólidos en suspensión en agua natural.",
  [S("25", 1)], opciones=["20 ppm", "100 ppm", "400 ppm", "2000 ppm"], correcta="a")
q("2A", SU, "Según la tabla de tolerancias del curso, ¿cuánta agua con algas se tolera?",
  "Correcta la A: nada (0). La PCA recomienda un máximo de 1000 ppm (C), pero para el curso manda la tabla del profe. La B es la tolerancia del azúcar y la D la de los sólidos en suspensión en agua natural.",
  [S("25", 1), pca4(100)], opciones=["Nada (0)", "500 ppm", "1000 ppm", "2000 ppm"], correcta="a")
q("2A", SU, "Según la tabla de tolerancias del curso, ¿qué hidróxido se tolera hasta 1,20 % del peso del cemento?",
  "Correcta la D: el hidróxido de potasio (KOH). El de sodio tiene un límite menor: 0,50 % (A). La PCA habla del hidróxido de calcio con 1,2 % (B), pero para el curso manda la tabla del profe.",
  [S("25", 1), pca4(99)], opciones=["Hidróxido de sodio", "Hidróxido de calcio", "Hidróxido de magnesio", "Hidróxido de potasio"], correcta="d")
q("2A", SU, "En la tabla de tolerancias del curso, los límites del hidróxido de sodio (0,50 %), del hidróxido de potasio (1,20 %) y del aceite mineral (2 %) se dan:",
  "Correcta la B: como porcentaje del peso (masa) del cemento, no en ppm del agua. Las otras opciones no son la base de la tabla.",
  [S("25", 1)], opciones=["En ppm del agua de mezcla", "Como porcentaje del peso (masa) del cemento", "Como porcentaje de la masa de los agregados", "Como porcentaje del volumen del concreto"], correcta="b")
q("2A", "verdadero_falso", "El límite de 20 000 ppm del cloruro de sodio es el mismo que el del cloruro como Cl⁻ (500 o 1000 ppm) en la tabla de tolerancias.",
  "Falso. La tabla trae dos filas distintas: 20 000 ppm es para la sal completa (NaCl); 500 ppm (preesforzado) o 1000 ppm (concreto húmedo o con aluminio o metales galvanizados) es para el cloruro como Cl⁻. En el cloruro de sodio solo una parte de la masa es cloruro, por eso los valores no coinciden.",
  [S("25", 1)], opciones=VF, correcta="b")

# --- Límites de cloruros del ACI 318 citados por la PCA (porcentaje del peso de cemento) ---
q("2A", SU, "Según el ACI 318 (citado por la PCA), ¿cuál es el límite de cloruros solubles en agua, en % del peso de cemento, para el concreto PREESFORZADO?",
  "Correcta la A: 0,06 %. La B (0,15 %) es para el concreto reforzado expuesto a cloruros, la C (0,30 %) para otras construcciones de concreto reforzado y la D (1,00 %) para el reforzado que se mantendrá seco y protegido de la humedad.",
  [pca4(97)], opciones=["0,06 %", "0,15 %", "0,30 %", "1,00 %"], correcta="a")
q("2A", SU, "Según el ACI 318 (citado por la PCA), ¿en cuál de estos concretos se permite el MAYOR contenido de cloruros?",
  "Correcta la C: el reforzado que se mantendrá seco y protegido de la humedad (1,00 %). El reforzado expuesto a cloruros durante su vida tiene 0,15 % (A), otras construcciones de concreto reforzado 0,30 % (B) y el preesforzado 0,06 % (D).",
  [pca4(97)], opciones=["Reforzado expuesto a cloruros durante su vida", "Otras construcciones de concreto reforzado", "Reforzado que se mantendrá seco y protegido de la humedad", "Preesforzado"], correcta="c")
q("2A", "verdadero_falso", "El ACI 318 limita el contenido de cloruros del concreto simple, el que no lleva acero.",
  "Falso. La PCA aclara que el ACI 318 no limita los cloruros en el concreto simple. Los límites son para el concreto armado, porque los cloruros atacan el acero.",
  [pca4(97), S("05", 3)], opciones=VF, correcta="b")
q("2A", RC, "¿Por qué no se puede comparar directamente el 0,06 % de cloruro del ACI 318 con los 500 ppm de cloruro de la tabla de tolerancias?",
  "Se resume de la PCA y de la tabla del curso.", [pca4(97), S("25", 1)],
  respuesta_modelo="Porque tienen bases distintas: los 500 ppm son la concentración de cloruro en el agua de mezcla (tabla del curso), y el 0,06 % es el cloruro soluble en agua del concreto preesforzado, en porcentaje del peso de cemento (ACI 318).",
  puntos_clave=["500 ppm: concentración en el agua", "0,06 %: cloruro del concreto respecto al cemento", "bases distintas"])

# ======================== GLOSARIO ========================
g("Agua de mezcla", "Agua que se añade al cemento y los agregados para preparar el concreto; prácticamente cualquier agua potable sirve.", [pca4(95)], "2A")
g("Agua dudosa", "Agua no potable o de calidad desconocida. Se acepta si cumple los requisitos de resistencia (C109) y tiempo de fraguado (C191) frente a un control.", [pca4(95), S("05", 9)], "2A")
g("Dureza del agua", "Indicador del contenido de sales, sobre todo de calcio y magnesio, expresado como CaCO₃.", [S("05", 3)], "2A")
g("Eflorescencia", "Depósito de sales en la superficie del concreto, asociado a sales como las de calcio y magnesio.", [S("05", 5), pca4(96)], "2A")
g("ppm", "Partes por millón: unidad de concentración de impurezas en el agua.", [S("25", 1)], "2A")
g("Relación agua/cemento (a/c)", "Relación por masa entre el agua de diseño y el cemento.", [E("X01", 4, "relacione a/c"), S("13", 9)], "2B")
g("Exudación (sangrado)", "Aparición de agua en la superficie del concreto después de consolidado y antes de la fragua, porque los sólidos se asientan y no retienen el agua.", [navas20(6)], "2B")
g("Contracción plástica", "Cambio de volumen del concreto en estado plástico por pérdida de agua debida a influencias externas.", [navas20(7)], "2B")
g("Contracción autógena", "Reducción de volumen causada por el consumo interno de agua durante la hidratación del cemento.", [navas20(7)], "2B")
g("Tasa de evaporación", "Cantidad de agua que se evapora de la superficie del concreto; se estima con el ábaco del ACI 305.", [S("06", 8)], "2B")
g("Asentamiento", "Medida de la consistencia del concreto fresco con el cono (ASTM C143); en autocompactante se mide el flujo (ASTM C1611).", [S("06", 9)], "2B")
g("Vibración", "Consolidación del concreto fresco, interna (vibrador de inmersión) o externa (sobre la formaleta).", [S("06", 5)], "2B")
