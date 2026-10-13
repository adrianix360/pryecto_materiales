from comun import S, pca, navas24, navas16, navas20, E

P = []


def _id(sub):
    return f"p3-{sub}-x{len([x for x in P if x['subtema'] == sub and x['origen'] == 'examen']) + 1:02d}"


def q(sub, tipo, enunciado, examen, periodo, explicacion, fuente, opciones=None, correcta=None,
      respuesta_modelo=None, puntos_clave=None, clave="oficial", justificacion_oficial=None, figura=None, verificar=None):
    item = {"id": _id(sub), "tema": 3, "subtema": sub, "tipo": tipo, "enunciado": enunciado, "origen": "examen",
            "examen": dict(examen, periodo=periodo), "clave": clave, "explicacion": explicacion, "fuente": fuente}
    if opciones is not None:
        item["opciones"] = [{"id": chr(97 + i), "texto": o} for i, o in enumerate(opciones)]
    if correcta is not None:
        item["correcta"] = correcta
    if respuesta_modelo:
        item["respuesta_modelo"] = respuesta_modelo
    if puntos_clave:
        item["puntos_clave"] = puntos_clave
    if justificacion_oficial:
        item["justificacion_oficial"] = justificacion_oficial
    if figura:
        item["figura"] = figura
    if verificar:
        item["verificar"] = verificar
    P.append(item)


VF = ["Verdadero", "Falso"]
I26, I25, II22, I20 = "I-2026", "I-2025", "II-2022", "I-2020"
X01P = "Sin fecha (cuestionario de Mediación Virtual)"

# ======================= 08 · I-2026 =======================
q("3C", "verdadero_falso",
  "Se realiza la prueba de laboratorio ASTM C566 (Humedad de los agregados). El agregado grueso tiene una humedad de 5,5%. Su absorción es de 3,5%. Tiene agua libre e hinchamiento",
  E("08", 1, "1.1, caso 1"), I26,
  "Falso. Como la humedad (5,5 %) supera la absorción (3,5 %), el agregado sí tiene agua libre (2 %). Pero el hinchamiento es un fenómeno exclusivo de la arena: en el agregado grueso las partículas son muy grandes comparadas con la capa de agua y no se forma el menisco que las separa.",
  [navas24(6), S("13", 2)], opciones=VF, correcta="b", justificacion_oficial="El agregado grueso no tiene hinchamiento.")
q("3B", "verdadero_falso", "Al utilizar rocas dolomíticas se podría producir reacción álcali – sílice",
  E("08", 1, "1.1, caso 3"), I26,
  "Falso. Las rocas dolomíticas se asocian con la reacción álcali-carbonato (RAC), no con la álcali-sílice. La RAS se da con minerales silíceos reactivos.",
  [S("15", 18), pca(126)], opciones=VF, correcta="b", justificacion_oficial="Reacción álcali carbonato")
q("3C", "verdadero_falso", "El volumen masivo de cemento se obtiene de la densidad aparente del cemento",
  E("08", 1, "1.1, caso 5"), I26,
  "Falso. Según la clave, con la densidad aparente se obtiene el volumen seco (sólido) del cemento: δs = Ps/Vs. El volumen masivo incluye además los espacios entre partículas.",
  [S("13", 5), S("13", 9)], opciones=VF, correcta="b", justificacion_oficial="Corresponde al volumen seco")
q("3C", "respuesta_corta", "Si va a determinar la cantidad de vacíos en una masa de agregados, cual norma recomienda",
  E("08", 2, "1.2, pregunta 5"), I26,
  "La ASTM C29 determina el peso unitario (densidad masiva) y, a partir de él y de la GBS, el contenido de vacíos entre partículas.",
  [S("19", 99), S("19", 107)], respuesta_modelo="ASTM C29", puntos_clave=["ASTM C29", "peso unitario y vacíos"])

NORMAS_08 = "ASTM D75, ASTM C702, ASTM C117, ASTM C136, ASTM C33, ASTM C131, ASTM C127, ASTM C128, ASTM C566, ASTM C29, ASTM C40, ASTM C586, ASTM C227, ASTM C1260, ASTM D4791, ASTM C114, ASTM C1602"
for letra, foto, norma, expl, pags, verif in [
    ("a", "2026-1_3-a", "ASTM C702", "La foto muestra un separador mecánico de canales con sus bandejas: es el método A de reducción de muestras.", [25, 28], None),
    ("b", "2026-1_3-b", "ASTM C117", "Se vierte el agua de lavado sobre las mallas anidadas (No. 16 sobre No. 200): es el lavado para determinar el material más fino que 75 µm.", [40], "La clave dice «ASTM C117 / ASTM C131 al lavar». La ASTM C131 es la abrasión de Los Ángeles; aquí se acepta solo la C117."),
    ("c", "2026-1_3-c", "ASTM C136", "Se coloca la muestra en el juego de mallas apiladas: es el análisis granulométrico.", [51, 52], None),
    ("d", "2026-1_3-d", "ASTM C127", "La canasta de alambre suspendida en el tanque sirve para pesar sumergido el agregado grueso: gravedad específica y absorción del grueso.", [68, 70], None),
    ("e", "2026-1_3-e", "ASTM C128", "Picnómetro con arena y termómetro (control a 23 ± 2 °C): gravedad específica y absorción del agregado fino.", [85, 90], None)]:
    q("3E", "respuesta_corta",
      f"Respuesta corta. Normativa. A continuación se mencionan algunas normas vistas en clase y laboratorio: {NORMAS_08}. Indique la NUMERACIÓN de norma ASTM que corresponde a la imagen de referencia (Ej: ASTM D75).",
      E("08", 3 if letra != "e" else 4, f"1.3, imagen {letra}"), I26, expl, [S("19", p) for p in pags],
      respuesta_modelo=norma, puntos_clave=[norma],
      figura={"src": f"img/examenes/{foto}.jpg", "alt": "Imagen de referencia del examen", "fuente": [S("08", 3 if letra != "e" else 4)]},
      verificar=verif)

# ======================= X02 · I-2025 =======================
q("3C", "seleccion_unica", "Usted realiza la prueba ASTM C29 y determina la cantidad de vacíos en los agregados. Concluye:",
  E("X02", 2, "1, pregunta 6"), I25,
  "Correcta la A: la cantidad de vacíos entre partículas afecta la demanda de pasta (la PCA da 30–45 % en el grueso y 40–50 % en el fino). La B es falsa porque la pasta debe llenar esos vacíos, así que no son despreciables. La C contradice la A. La D está al revés: el fino suele tener más vacíos que el grueso.",
  [pca(114)], opciones=["La cantidad de vacíos entre las partículas afecta la demanda de pasta en el diseño de la mezcla",
                        "No es importante pues al mezclar todos los componentes es despreciable",
                        "La cantidad de vacíos entre las partículas NO afecta la demanda de pasta en el diseño de la mezcla",
                        "Un agregado grueso tiene generalmente más % de vacíos que un agregado fino"], correcta="a")
q("3D", "seleccion_unica", "¿Qué factor aumenta de forma aleatoria el contenido de aire en la mezcla? (1 puntos)",
  E("X02", 1, "1, pregunta 5"), I25,
  "Correcta la B. Según Navas, el aire siempre entra en la mezcla en cantidad aleatoria y aumenta con más agregado fino (sobre todo entre las mallas No. 30 y No. 50), con un tamaño máximo menor y con un mezclado más fuerte o más largo. La A está al revés: el vibrado prolongado reduce el aire. La C y la D no aparecen en las fuentes como causas.",
  [navas20(8)], opciones=["Uso de vibrador externo", "Mayor proporción de agregado fino", "Aumento de a/c", "Usar mezcladoras más eficientes"],
  correcta="b")
q("3B", "verdadero_falso", "Los álcalis del cemento que puede afectar a las mezclas se pueden clasificar como concentraciones de hierro y potasio",
  E("X02", 2, "2, caso 1"), I25,
  "Falso. Los álcalis del cemento son los óxidos de sodio (Na₂O) y de potasio (K₂O); el hierro no es un álcali.",
  [S("15", 15)], opciones=VF, correcta="b", justificacion_oficial="Sodio y potasio")
q("3C", "verdadero_falso",
  "Masa del agregado seco al aire por unidad de volumen de las partículas de agregado, incluyendo el volumen de los poros permeables e impermeables dentro de las partículas del agregado, pero sin incluir los vacíos entre las partículas. La definición corresponde con “Densidad bruta seca”",
  E("X02", 2, "2, caso 4"), I25,
  "Falso, por una sola palabra: la densidad bruta seca se define con el agregado seco AL HORNO, no seco al aire. El resto de la definición es correcto.",
  [S("13", 6), S("19", 64)], opciones=VF, correcta="b", justificacion_oficial="El agregado debe ser seco al horno")
q("3A", "verdadero_falso",
  "Para obtener el Ensayo de Partículas planas y Elongadas se utiliza la norma ASTM D 5260 y establece una relación máxima de 15% en el volumen",
  E("X02", 2, "2, caso 5"), I25,
  "Falso: el límite es 15 % en MASA, no en volumen, y la norma de partículas planas y elongadas es la ASTM D4791.",
  [S("15", 19)], opciones=VF, correcta="b", justificacion_oficial="Norma ASTM D4790. 15% en masa",
  verificar="La clave dice «ASTM D4790», pero las diapositivas del curso (15, pág. 19; 14, pág. 14) dicen ASTM D4791.")
q("3E", "respuesta_corta",
  "Al realizar su informe de laboratorio para la norma ASTM C131, el resultado se debe comparar con una tolerancia máxima a cumplir en base a la norma ASTM C33, indique el valor.",
  E("X02", 3, "3, pregunta 2"), I25,
  "La clave da 40 %. El manual solo dice que las especificaciones fijan una pérdida máxima por abrasión.",
  [S("19", 112), pca(118)], respuesta_modelo="40%", puntos_clave=["40 %", "pérdida máxima por abrasión"],
  verificar="El 40 % no aparece en ninguna fuente de teoría del curso; solo en esta clave.")
q("3C", "respuesta_corta",
  "Al realizar su ensayo de laboratorio ASTM C128 de forma correcta, la gravedad específica de un agregado dio un valor de 2,3, ¿Que concluye de este valor?",
  E("X02", 3, "3, pregunta 4"), I25,
  "Un agregado normal tiene GBS entre 2,4 y 2,8. Un valor de 2,3 queda por debajo, así que la clave lo clasifica como agregado ligero.",
  [S("14", 9)], respuesta_modelo="Agregado ligero", puntos_clave=["menor que 2,4", "agregado ligero (liviano)"])
q("3A", "respuesta_corta", "Indique un tipo de roca considerada liviana",
  E("X02", 3, "3, pregunta 6"), I25,
  "Entre los agregados livianos del curso están la pómez, la escoria volcánica y la ceniza volante.",
  [S("14", 11)], respuesta_modelo="Pómez (también se aceptan ceniza volante o escoria volcánica)", puntos_clave=["pómez", "escoria volcánica", "ceniza volante"])
q("3A", "respuesta_corta", "Indique el nombre de uno de los tipos de trituradores que se utilizan en la producción de agregado",
  E("X02", 3, "3, pregunta 7"), I25,
  "La clave acepta el triturador rotatorio o el de mandíbula. La conferencia (26, pág. 18) explica que los equipos de trituración generan fuerzas de compresión e impacto.",
  [S("26", 18)], respuesta_modelo="Rotatorio o de mandíbula", puntos_clave=["rotatorio", "mandíbula"],
  verificar="Los tipos de triturador solo aparecen en la clave de examen, no en las fuentes de teoría.")
q("3C", "respuesta_corta", "Según el diagrama de pesos y volúmenes, indique los elementos que involucra el Volumen Bruto de agregado",
  E("X02", 3, "3, pregunta 8"), I25,
  "El volumen bruto es el volumen sólido más el de los poros permeables (VB = Vs + Vpp); no incluye los vacíos entre partículas.",
  [S("13", 4), navas24(8)], respuesta_modelo="Vs + Vpp", puntos_clave=["volumen sólido", "poros permeables"])
q("3D", "respuesta_corta", "Defina el tamaño máximo nominal de un agregado",
  E("X02", 3, "3, pregunta 9"), I25,
  "Es la definición del manual de laboratorio. No se confunde con el tamaño máximo, que es la malla más pequeña por la que pasa el 100 %.",
  [S("19", 9), S("19", 50)], respuesta_modelo="Es el mayor tamaño de malla donde queda retenido material respetando un retenido máximo permisible",
  puntos_clave=["mayor tamaño de malla", "queda retenido material", "retenido máximo permisible"])
q("3B", "respuesta_corta", "Indique la norma para determinar expansiones de álcali sílice a 14 días",
  E("X02", 3, "3, pregunta 11"), I25, "La ASTM C1260 (barra de mortero) rechaza si la expansión supera 0,10 % a los 14 días.",
  [S("15", 17)], respuesta_modelo="ASTM C1260", puntos_clave=["ASTM C1260"])
q("3B", "respuesta_corta", "Indique la norma para determinar expansiones de álcali sílice a 3 meses y seis meses",
  E("X02", 3, "3, pregunta 12"), I25, "La ASTM C227 (barra de mortero) rechaza si la expansión supera 0,05 % a los 3 meses o 0,10 % a los 6 meses.",
  [S("15", 17)], respuesta_modelo="ASTM C227", puntos_clave=["ASTM C227"])

# ======================= X04 · II-2022 =======================
q("3C", "respuesta_corta",
  "Indique una variable para disminuir el contenido de vacíos en una mezcla de concreto (sólo puede indicar una variable, si indica más de una la respuesta es inválida). Valor 1 punto",
  E("X04", 2, "Parte 1a, respuesta corta 1"), II22,
  "Los vacíos aumentan con la angularidad y disminuyen con una mejor granulometría y con tamaños mayores bien graduados.",
  [pca(114), pca(107)], respuesta_modelo="Disminución de partículas angulosas, o mejorar la granulometría", puntos_clave=["menos partículas angulosas", "mejor granulometría"])
q("3A", "respuesta_corta",
  "Indique el valor superior del peso unitario (kg/m3) de un agregado para considerarlo como un material pesado (sólo puede indicar un valor, si indica más de uno la respuesta es inválida) Valor 1 punto.",
  E("X04", 2, "Parte 1a, respuesta corta 2"), II22, "Un agregado es pesado si su peso unitario masivo seco supera 1900 kg/m³.",
  [S("14", 9)], respuesta_modelo="Superior a 1900 kg/m3", puntos_clave=["δb > 1900 kg/m³"])
q("3B", "respuesta_corta",
  "Indique una norma de ensayo para determinar la reacción álcali sílice (sólo puede indicar una, si indica más de una, la respuesta es inválida) Valor 1 punto",
  E("X04", 2, "Parte 1a, respuesta corta 4"), II22, "Las tres normas de reacción álcali-sílice del curso son la C227, la C1260 y la C289.",
  [S("15", 17)], respuesta_modelo="ASTM C227 (también ASTM C1260 o ASTM C289)", puntos_clave=["C227", "C1260", "C289"])
q("3C", "verdadero_falso",
  "La densidad de un agregado usa directamente en algunos cálculos de proporcionamiento y del control de la mezcla, tales como el volumen ocupado por el agregado en el método del volumen absoluto de diseño de mezcla",
  E("X04", 2, "Parte 1a, F/V 3"), II22,
  "Falso según la clave: lo que se usa en esos cálculos es la gravedad específica (densidad relativa), tal como lo dice la PCA.",
  [pca(114)], opciones=VF, correcta="b", justificacion_oficial="Corresponde a gravedad especifica o densidad relativa")

# ======================= X06 · I-2020 =======================
q("3C", "seleccion_unica", "Los agregados de peso normal tienen densidades (gravedades) especificas del orden de :",
  E("X06", 1, "Pregunta 1"), I20,
  "Correcta la B: un agregado normal tiene GBS entre 2,4 y 2,8. La A es demasiado amplia, la C y la D corresponden a agregados pesados, y la E es falsa porque la gravedad específica es una propiedad del agregado, no del concreto.",
  [S("14", 9)], opciones=["Entre 2 y 3", "de 2.4 a 2.8", "Mas de 5.0", "3.0 o más", "Dependen del concreto a usar"], correcta="b",
  verificar="Otras fuentes dan rangos distintos (ver la tarjeta de gravedad específica normal).")
q("3A", "verdadero_falso",
  "Los agregados livianos no son comunes en nuestro país debido a que eran antiguamente fáciles de encontrar en las capas superficiales de las canteras que ya perdieron su vida útil.",
  E("X06", 1, "Pregunta 2"), I20,
  "Según la clave del cuestionario, es «Verdadero». Las fuentes de teoría del curso no tratan este tema.",
  [], opciones=VF, correcta="a",
  verificar="La clave dice «Verdadero», pero la documentación de teoría no respalda ni desmiente la afirmación y la redacción es confusa.")
q("3C", "respuesta_corta", "El hinchamiento en arenas se da principalmente por :",
  E("X06", 2, "Pregunta 5"), I20,
  "El comentario del profesor resalta la presencia de agua libre. El mecanismo es la tensión superficial: el agua libre forma meniscos que separan las partículas.",
  [navas24(6), pca(115)], respuesta_modelo="Presencia de agua libre, que por tensión superficial forma meniscos y separa las partículas",
  puntos_clave=["agua libre", "tensión superficial (menisco)", "solo en arenas"])
q("3A", "verdadero_falso",
  "No se debe admitir más de un 15 % en volumen de partículas alargadas y aplanadas, obtenido con base en una muestra de agregado representativa",
  E("X06", 2, "Pregunta 6"), I20, "Falso: el límite es 15 % en masa.",
  [S("15", 19), navas24(4)], opciones=VF, correcta="b", justificacion_oficial="Es 15 % en masa, no en volumen")
q("3C", "seleccion_unica",
  "Si la humedad de compra es 3 % y la humedad de dosificación es 2 %, considero que el agregado no siempre va a aportar agua al agua de diseño en una mezcla de concreto ?",
  E("X06", 3, "Pregunta 8"), I20,
  "Correcta la A: que el agregado aporte o quite agua depende de si su humedad supera o no la absorción (w > D aporta; w < D absorbe). Sin la absorción no se puede concluir. La B y la E responden sin esa información. La C falla porque estar por encima del peso seco no basta. La D supone una absorción que el enunciado no da.",
  [navas24(6), S("13", 2)], opciones=["No, debo revisar absorción", "No", "Si, ya que ambas son mayores que la condición de peso seco",
                                     "Si, ya que la humedad es mayor a la absorción", "Si"], correcta="a")
q("3B", "verdadero_falso", "Aunque los agregados sean reactivos, las reacciones álcali-agregado solo ocurren si hay presencia de agua",
  E("X06", 3, "Pregunta 9"), I20,
  "Falso: no basta el agua. Tienen que darse tres condiciones a la vez: agregado reactivo, exceso de álcalis y humedad.",
  [S("15", 13), pca(122)], opciones=VF, correcta="b",
  justificacion_oficial="Además de ser reactivos, debe haber dos condiciones más : agua para que se generen las reacciones de expansión pero también, se debe superar el máximo permitido de álcalis")
q("3A", "seleccion_unica",
  "En la misma mezcla de concreto se puede reducir la cantidad de pasta entre un ___% y ___% si se pasa de usar agregados laminados y planos a agregados de formas cúbicas y de mejor textura superficial",
  E("X06", 3, "Pregunta 10"), I20,
  "La clave da la A (4 % a 5 %). Las fuentes del curso confirman la idea (las partículas planas piden más pasta), pero no el porcentaje.",
  [S("15", 20)], opciones=["4 % a 5 %", "Ninguno de los anteriores", "1 % a 2 %", "10 % a 12 %", "18 % a 20 %"], correcta="a",
  verificar="El rango de 4 % a 5 % solo aparece en la clave del cuestionario.")
q("3C", "respuesta_corta",
  "Debido a la imposibilidad práctica de medirlos, consideramos que los poros impermeables están incluidos en :",
  E("X06", 4, "Pregunta 11"), I20,
  "Los poros impermeables no intercambian humedad, así que se cuentan dentro del volumen sólido.",
  [navas24(8)], respuesta_modelo="El volumen del sólido", puntos_clave=["volumen sólido (Vs)"])
q("3B", "respuesta_corta", "Generalmente los agregados de río en nuestro país son de origen (una sola palabra):",
  E("X06", 4, "Pregunta 12"), I20, "En Costa Rica los mejores agregados provienen de rocas ígneas.",
  [S("26", 11)], respuesta_modelo="Ígneo", puntos_clave=["ígneo"])

# ======================= X07 · I-2020 (capturas) =======================
q("3A", "verdadero_falso",
  "Para producir un concreto de 20 MPa de resistencia a compresión simple a 28 días de curado, no es necesario utilizar un agregado grueso de muy alta calidad mecánica.",
  E("X07", 1, "captura 1, pregunta 1"), I20,
  "Verdadero. En concreto convencional, la resistencia del agregado influye menos que la de la pasta y la adherencia; los agregados resisten mucho más que 20 MPa (la PCA da 65 a 270 MPa en compresión). Según la clave de X01 (pág. 6), es a partir de unos 34 MPa que la calidad mecánica del agregado se vuelve esencial.",
  [pca(118), E("X01", 6, "F/V 3")], opciones=VF, correcta="a",
  justificacion_oficial="Usualmente los agregados tienen mucho más resistencia que 20 MPa")
q("3A", "seleccion_unica", "Cite las cuatro funciones clave de los agregados en las mezclas de concreto",
  E("X07", 4, "captura 4, pregunta 2"), I20,
  "Correcta la A: son los cuatro aspectos de importancia que da la presentación del curso. La B incluye «reacción con el cemento», algo que justamente no se desea (agregado inerte). La C mezcla acabado y textura, que son características, no funciones. La D habla de proveer humedad, lo cual no es una función del agregado.",
  [S("15", 3)], opciones=["Economia, durabilidad, resistencia y trabajabilidad", "Resistencia, volumen, reacción con el cemento y dureza",
                          "Acabado, textura, economia y durabilidad", "Proveer volumen, brindar espacios, proveer humedad y durabilidad"], correcta="a")

# ======================= X01 · cuestionario y claves =======================
q("3D", "verdadero_falso",
  "Analice la siguiente afirmación e indique si es falsa o verdadera.\nUn agregado de 38 mm (37,5 mm) por su tamaño máximo es adecuado para construir una losa de piso sin refuerzo",
  E("X01", 1, "pregunta 1"), X01P,
  "Verdadero. Un tamaño máximo nominal mayor necesita menos pasta (menos superficie que cubrir), lo que ahorra y reduce las contracciones. En una losa sin refuerzo no limita la separación de barras.",
  [pca(109), S("15", 4)], opciones=VF, correcta="a",
  justificacion_oficial="Un tamaño máximo nominal de 38 mm (37,5 mm) es adecuado para la construcción de la losa. Este tipo de tamaño máximo nominal brinda ahorro al requerir menos pasta y por lo tanto menores contracciones.")
q("3B", "seleccion_multiple",
  "Marque aquellas rocas que considere que son aptas para fabricar concreto hidráulico en Costa Rica\nPuede marcar varias alternativas",
  E("X01", 1, "pregunta 2"), X01P,
  "Son correctas la caliza, el granito y la andesita (escrita «Andecita» en el original). Las lavas andesíticas recientes son la fuente típica del país y las calizas son muy usadas. La dolomita se asocia con la reacción álcali-carbonato y la pirita es un sulfuro de hierro que vuelve reactivo al agregado.",
  [S("26", 54), S("26", 63), S("15", 14), S("15", 18)], opciones=["Caliza", "Granito", "Andecita", "Dolomita", "Pirita"], correcta=["a", "b", "c"])
q("3B", "seleccion_unica", "Elija la opción que corresponda con rocas sedimentarias",
  E("X01", 1, "pregunta 3"), X01P,
  "Correcta la B: la arenisca y el conglomerado son sedimentarias clásticas (fragmentos cementados). La A son ígneas y la C son metamórficas.",
  [S("26", 59), S("26", 9)], opciones=["Basalto, granito", "Arenizca, conglomerado", "Marmol, cuarcita"], correcta="b")
q("3B", "verdadero_falso",
  "Los materiales más finos que 75 µm (tamiz No. 200) no afectan la resistencia o durabilidad del concreto dado su pequeño tamaño",
  E("X01", 1, "pregunta 4"), X01P,
  "Falso. El limo y la arcilla forman una capa sobre las partículas que debilita la adherencia pasta-agregado y aumenta la demanda de agua.",
  [pca(120)], opciones=VF, correcta="b",
  justificacion_oficial="Los materiales más finos que 75 µm (tamiz No. 200), especialmente el limo y la arcilla, pueden estar presentes como polvo suelto y pueden formar un revestimiento en las partículas de agregados. [...] debilitan la adherencia entre la pasta de cemento y el agregado. Si ciertos tipos de limo o arcilla están presentes en cantidades excesivas, la demanda de agua puede aumentar significantemente. Lectura Agregados para Concreto. Pag 119")
q("3E", "seleccion_unica",
  "Para el proyecto APM Terminals se solicita que los agregados cumplan estrictamente especificaciones. Uno de los ensayos es la abrasión de agregado ASTM C131, pues indica:",
  E("X01", 1, "pregunta 5"), X01P,
  "Correcta la A según la clave: la C131 mide la degradación por abrasión, impacto y trituración en la Máquina de Los Ángeles. La B y la D no son correctas porque la C131 no es un ensayo de compresión. La C tampoco: la abrasión de superficies de concreto se mide con la C418 o la C994.",
  [S("19", 112), S("15", 11)], opciones=["La resistencia al impacto del agregado", "La resistencia a la compresión", "La abrasión de la superficie de concreto",
                                         "La resistencia a la compresión de forma indirecta"], correcta="a")
q("3B", "seleccion_unica",
  "En una visita de campo se evidencia un ataque a la pasta de cemento que degradó una masa de concreto.\nInvestigando corresponde con el fenómeno llamado:",
  E("X01", 2, "pregunta 1"), X01P,
  "Correcta la A: en la álcali-carbonato el producto forma grietas en la pasta (el agregado ataca la pasta). La álcali-sílice, en cambio, actúa por presiones internas del agregado. El sangrado es un fenómeno del concreto fresco, y el hidróxido alcalino es un reactivo, no un fenómeno.",
  [S("15", 18), S("15", 16)], opciones=["Álcali carbonato", "Sangrado", "Álcali sílice", "Hidróxido alcalino"], correcta="a")
q("3B", "seleccion_unica",
  "En una visita de campo se evidencia presiones internas que degradaron una masa de concreto.\nInvestigando corresponde con el fenómeno llamado:",
  E("X01", 2, "pregunta 2"), X01P,
  "Correcta la A: en la álcali-sílice el gel expansivo genera presiones internas que desintegran la masa de concreto. La álcali-carbonato se reconoce por el ataque a la pasta. El sangrado y el hidróxido alcalino no son el fenómeno.",
  [S("15", 16)], opciones=["Álcali sílice", "Hidróxido alcalino", "Sangrado", "Álcali carbonato"], correcta="a")
q("3B", "seleccion_unica", "Las álcalis del cemento se pueden determinan como:",
  E("X01", 2, "pregunta 3"), X01P,
  "Correcta la C: óxidos de sodio (Na₂O) y de potasio (K₂O). La A confunde los álcalis con las reacciones que provocan, y el hierro y el magnesio de la B no son álcalis.",
  [S("15", 15)], opciones=["Concentraciones de álcali sílice y álcali carbonato", "Concentraciones de óxidos de hierro y magnesio",
                           "Concentraciones de óxidos de sodio y potasio"], correcta="c")
q("3D", "verdadero_falso",
  "Indique si la siguiente afirmación es correcta. Un agregado de 25 mm al ser de más grande introduce más aire a la mezcla de concreto que uno de 19 mm.",
  E("X01", 2, "pregunta 4"), X01P, "Falso: el agregado más pequeño es el que introduce más aire, por su mayor área superficial.",
  [S("15", 4), navas20(8)], opciones=VF, correcta="b", justificacion_oficial="Un agregado pequeño introduce mas aire por su área superficial")
q("3C", "seleccion_unica",
  "Se realiza la prueba de laboratorio ASTM C566 (Humedad de los agregados). El agregado grueso tiene una humedad de 5,5%. Su absorción es de 3,5%.\nPara este caso.",
  E("X01", 3, "pregunta 1"), X01P,
  "Correcta la A: la humedad supera la absorción, así que hay 2 % de agua libre que se suma a la mezcla y hay que ajustar el agua de dosificación. La B ignora ese aporte. La C y la D hablan de hinchamiento, que no ocurre en el agregado grueso.",
  [navas24(6), S("19", 66)], opciones=["Es necesario ajustar el agua dosificación de la mezcla de concreto", "No es importante el aporte de agua de los agregados gruesos",
                                       "No es necesario ajustar el agua de dosificación, pues no afecta su hinchamiento", "Como tiene agua libre se debe determinar su hinchamiento"], correcta="a")
q("3C", "seleccion_unica", "El volumen bruto de los agregados incluye:",
  E("X01", 3, "pregunta 3"), X01P,
  "Correcta la C: VB = Vs + Vpp. La A es solo el volumen sólido. La B no tiene sentido, porque el aire no forma parte de la partícula. La D, con los vacíos entre partículas, es el volumen masivo.",
  [S("13", 4), navas24(8)], opciones=["Volumen sólido", "Volumen sólido + Volumen de aire", "Volumen sólido + Volumen de poros permeables", "Volumen sólido + volumen de vacíos"], correcta="c")
q("3D", "seleccion_unica", "La granulometría corresponde con:",
  E("X01", 5, "pregunta 3"), X01P,
  "Correcta la A: la granulometría expresa la distribución de tamaños (la graduación) del material. La B describe la masa mínima de muestra, que es otra cosa.",
  [S("19", 47)], opciones=["Forma en que se expresa la graduación de los materiales", "Cantidad de muestra para realizar ensayos"], correcta="a")
q("3D", "seleccion_unica", "La importancia de una granulometría suave y continua corresponde con:",
  E("X01", 5, "pregunta 4"), X01P,
  "Correcta la B: una curva suave y continua reduce vacíos y pasta, lo que favorece la economía, la trabajabilidad, la resistencia y la durabilidad.",
  [navas16(17), pca(107)], opciones=["No es importante para un concreto de calidad", "Contribuye a la economía, trabajabilidad, resistencia y durabilidad del concreto"], correcta="b")

F6 = [
    ("3C", "El volumen masivo de cemento es mayor que el volumen sólido de cemento porque en el primer caso se toman en cuenta los poros permeables", "b",
     "En el volumen masivo lo que se toma en cuenta son los espacios entre partículas, no posee poros permeables",
     "Falso. El volumen masivo sí es mayor que el sólido, pero porque incluye los espacios entre partículas, no los poros permeables.", [S("13", 4)]),
    ("3D", "Se dispone de dos arenas con los módulos de finura siguientes (MFA= 2,4 y MFB= 3,0); para mejorar trabajabilidad se usará la arena B.", "b",
     "A mayor valor, más gruesa es la arena, por ende menos trabajable",
     "Falso. La arena B (MF 3,0) es más gruesa; una arena más fina tiene más partículas que ayudan a la trabajabilidad.", [S("19", 48), navas16(22)]),
    ("3A", "Para producir un concreto de 20 MPa de resistencia a compresión simple a 28 días de curado, no es necesario utilizar un agregado grueso de muy alta calidad mecánica.", "a",
     "Es a partir de 34 MPa donde resulta esencial la calidad mecánica del agregado. O bien: lo que interesa en la adherencia y no la resistencia mecánica del agregado.",
     "Verdadero. En concreto convencional importan más la pasta y la adherencia que la resistencia del agregado.", [pca(118)]),
    ("3C", "El agua de diseño es mayor al agua de dosificación cuando los agregados se dosifican con agua libre.", "b",
     "Es menor porque los agregados aportan el resto para llegar al agua de diseño",
     "Falso. Si los agregados traen agua libre, aportan parte del agua de diseño; por eso el agua que se dosifica es menor, no mayor.", [navas24(6)]),
    ("3A", "La tenacidad es una medida de qué tan resistente es el agregado grueso ante el desgaste por abrasión", "b",
     "Es una medida de qué tanto soporta cargas de impacto",
     "Falso. La tenacidad se refiere al impacto; el desgaste es la abrasión.", [S("19", 112)]),
    ("3D", "El módulo de finura de una arena es un indicador de la calidad cuando se ubica dentro especificaciones", "b",
     "Sólo indica qué tan gruesa o qué tan fina es. Es indicador de la trabajabilidad que podría aportar",
     "Falso. El MF solo describe qué tan gruesa o fina es la arena; granulometrías distintas pueden dar el mismo MF.", [navas16(22), pca(109)]),
    ("3B", "La caliza y el basalto si bien pertenecen a grupos mineralógicos distintos, ambos son aptos para la fabricación de concreto estructural", "a",
     "Caliza: sedimentaria. Basalto: ignea",
     "Verdadero. La caliza es sedimentaria y el basalto es ígneo; ambos sirven como agregado.", [S("26", 9), S("26", 63)]),
    ("3A", "No se debe admitir más de un 15 % en volumen de partículas alargadas y aplanadas, obtenido con base en una muestra de agregado representativa", "b",
     "15 % en masa", "Falso: el límite es 15 % en masa.", [S("15", 19)]),
    ("3C", "El volumen efectivo del cemento de uso general contenido en un saco es aproximadamente 0,035 m3", "b",
     "Es el volumen masivo el que es aproximadamente 0,035 m3",
     "Falso. Unos 0,035 m³ es el volumen masivo del saco; el volumen efectivo (sólido) es menor (con Gs = 3,10, unos 0,016 m³).", [E("X01", 7, "b, pregunta 2")]),
    ("3A", "Los agregados contribuyen a reducir los fenómenos de contracción y elevación de la temperatura del concreto durante el fraguado", "a",
     "A mayor contenido de cemento en una mezcla con respecto a la cantidad de agregados, más calor se libera, así como mayor contracción debido a la alta finura del cemento",
     "Verdadero. Los agregados reemplazan pasta; menos cemento significa menos calor y menos contracción.", []),
    ("3B", "Aunque los agregados sean reactivos, las reacciones álcali-agregado solo ocurren si hay presencia de agua", "b",
     "Además de ser reactivos, debe haber agua para que se generen las reacciones de expansión pero también, se debe superar el máximo permitido de álcalis",
     "Falso. Hacen falta las tres condiciones: agregado reactivo, humedad y exceso de álcalis.", [S("15", 13)]),
    ("3C", "La densidad relativa bruta seca de un agregado da una idea relativa sobre la facilidad de adherencia con la pasta de cemento", "a",
     "A menor valor de densidad relativa bruta seca, más poroso es el agregado, por tanto, la adherencia pasta agregado será mejor",
     "Verdadero según la clave: una GBS menor indica un agregado más poroso, y eso mejora la adherencia.", []),
    ("3D", "El tamaño máximo efectivo es aquel tamaño en que se admite un sobre-tamaño que puede variar entre 5 % a 15 % dependiendo de qué tamaño se trate", "b",
     "Es el tamaño máximo nominal",
     "Falso. Lo descrito corresponde al tamaño máximo nominal (la PCA admite retener del 5 al 15 % en ese tamiz).", [pca(111), S("19", 50)]),
]
NUM_F6 = [1, 2, 3, 4, 5, 7, 9, 10, 12, 13, 14, 15, 16]  # numeración de la pág. 6 (se omiten 6 y 11, que son del tema 2)
for i, (sub, enun, corr, just, expl, fu) in enumerate(F6):
    q(sub, "verdadero_falso", enun, E("X01", 6, f"F/V {NUM_F6[i]}"), X01P, expl, fu, opciones=VF, correcta=corr, justificacion_oficial=just)
for it in P:
    if it["examen"]["doc"] == "X01" and it["examen"]["pag"] == 6 and not it["fuente"]:
        it["verificar"] = "Las fuentes de teoría no desarrollan esta afirmación; la respuesta se apoya en la clave del examen."

q("3D", "verdadero_falso", "El uso de menores tamaños máximos nominales en losas de concreto hidráulico contribuyen a reducir el agrietamiento",
  E("X01", 6, "F/V 8"), X01P,
  "Falso. Un tamaño máximo menor pide más finos y más pasta, lo que aumenta las grietas. Según la clave, cuanto más pequeño el tamaño máximo, mayor la propensión a la contracción por asentamiento plástico.",
  [pca(109)], opciones=VF, correcta="b",
  justificacion_oficial="Tanto más pequeño sea el tamaño máximo del agregado, mayor propensión a la contracción por asentamiento plástico (anotación a mano: + finos + pasta + grietas)")

q("3A", "seleccion_unica",
  "Seleccione la respuesta correcta:\nNo se debe admitir más de un 15% en masa de partículas alargadas y aplanadas, obtenido con base en una muestra de agregado representativa",
  E("X01", 7, "b, pregunta 1"), X01P,
  "Correcta la D: el límite es 15 % por masa. La A no es un porcentaje, la B no dice la base, y la C usa el volumen, que no corresponde.",
  [S("15", 19)], opciones=["Kilogramo", "15 %", "15 % por volumen", "15 % por masa"], correcta="d")
q("3C", "seleccion_unica",
  "Seleccione la respuesta correcta:\nSi el Gs del cemento es de 3.10, el volumen efectivo del cemento contenido en un saco de cemento de 50 kg es aproximadamente ___ m3",
  E("X01", 7, "b, pregunta 2"), X01P,
  "Correcta la B: Vs = Ps / (Gs·δw) = 50 kg / (3,10 × 1000 kg/m³) ≈ 0,0161 m³ = 16,1 L. La A (0,035 m³) es el volumen masivo, no el efectivo. La C (0,017 m³) no sale del cálculo con Gs = 3,10.",
  [S("13", 10)], opciones=["0.035 m3", "16,1 litros", "0.017 m3", "Ninguna de las anteriores"], correcta="b")
q("3B", "respuesta_corta", "Indique las tres condiciones que debe tener un agregado para provocar reacciones expansivas",
  E("X01", 7, "b, pregunta 5"), X01P, "Son las tres condiciones de la reacción álcali-agregado.",
  [S("15", 13), pca(122)], respuesta_modelo="Agregado reactivo, exceso de álcalis y humedad",
  puntos_clave=["agregado reactivo", "exceso de álcalis (máx. 0,6 %)", "humedad"])
q("3B", "verdadero_falso",
  "Las partículas más finas que 75 µm, por su tamaño, no tiene importancia directa en la mezcla de concreto",
  E("X01", 7, "a, caso 5"), X01P,
  "Falso. Los finos y las impurezas afectan el fraguado, la resistencia y la demanda de agua.",
  [pca(120)], opciones=VF, correcta="b",
  justificacion_oficial="Los finos y las impurezas orgánicas pueden retrasar el fraguado y el endurecimiento del concreto, reducir el desarrollo de la resistencia y, en algunos casos poco usuales, causar el deterioro")

q("3C", "verdadero_falso",
  "La gravedad especifica aparente corresponde con la masa por unidad de volumen de la porción impermeable de las partículas del agregado",
  E("X01", 8, "F/V 1"), X01P,
  "Falso según la corrección: la masa por unidad de volumen de la porción impermeable es la densidad aparente (δs). La gravedad específica aparente es adimensional: es esa densidad dividida entre la del agua.",
  [S("19", 63), S("13", 5)], opciones=VF, correcta="b", clave="oficial",
  justificacion_oficial="Incluye los poros no accesibles al agua, pero excluye los vacíos (corrección a mano)",
  verificar="La corrección en rojo es breve; el argumento de «densidad contra gravedad específica» sale del manual (19, pág. 63).")
q("3A", "verdadero_falso", "Un peso unitario masivo seco de 1300 kg/m3 se cataloga como un agregado liviano",
  E("X01", 8, "F/V 4"), X01P, "Falso: los livianos tienen δb < 1120 kg/m³; 1300 kg/m³ cae en el rango normal (1120 a 1900).",
  [S("14", 9)], opciones=VF, correcta="b", justificacion_oficial="Los agregados livianos son los que tienen δb < 1120 kg/m3 (corrección a mano)")
q("3B", "respuesta_corta", "Indique una roca sedimentaria clasificada como química",
  E("X01", 8, "respuesta corta 6"), X01P, "Las sedimentarias químicas se forman por precipitación: la caliza (carbonato de calcio), la sal o el yeso.",
  [S("26", 62)], respuesta_modelo="Caliza", puntos_clave=["caliza (o sal, yeso)"])
q("3C", "respuesta_corta",
  "Indique a que corresponde la siguiente definición: masa del agregado seco al horno por unidad de volumen de las partículas de agregado, incluyendo el volumen de los poros permeables e impermeables, dentro de las partículas del agregado, pero sin incluir los vacíos entre las partículas.",
  E("X01", 8, "respuesta corta 7"), X01P,
  "La definición es, palabra por palabra, la de la densidad bruta seca en la diapositiva del curso y en el manual.",
  [S("13", 6), S("19", 64)], respuesta_modelo="Densidad bruta seca (δBS)", puntos_clave=["densidad bruta seca", "seco al horno", "incluye poros permeables e impermeables"],
  verificar="La corrección en rojo de este examen escribe «gravedad específica aparente» (contradicción C16 de ALCANCE.md). Se muestra la respuesta de las diapositivas y de la clave de 2025.")
q("3C", "respuesta_corta", "La gravedad especifica de un agregado normal está en el rango de 2,4 y de ___",
  E("X01", 8, "respuesta corta 9"), X01P, "Un agregado normal tiene 2,4 < GBS < 2,8.",
  [S("14", 9)], respuesta_modelo="2,8", puntos_clave=["2,8"])
q("3A", "respuesta_corta", "Una función del agregado catalogado como pesado es:",
  E("X01", 8, "respuesta corta 10"), X01P,
  "Los agregados pesados (magnetita, barita, etc.) se usan en concreto de blindaje contra la radiación (ASTM C637).",
  [S("14", 10)], respuesta_modelo="Agregados de alta densidad como magnetita, titanio, etc., proporcionan blindaje contra radiación",
  puntos_clave=["alta densidad", "blindaje contra radiación (ASTM C637)"])

# ======================= Desarrollo (X14, X15) — sin clave oficial =======================
q("3C", "respuesta_corta",
  "Explique en términos de economía, resistencia y trabajabilidad, porqué es importante tomar en cuenta el hinchamiento de la arena en el cálculo de cantidades a dosificar y a comprar.",
  {"doc": "X15", "pag": 1, "pregunta": "Teoría (20 %)"}, "II-2009",
  "No hay clave oficial; la respuesta modelo se armó solo con las fuentes. La arena húmeda ocupa más volumen masivo que seca (V'm = Vm(1 + H)). Si se compra o se dosifica por volumen sin corregir: (1) economía: se compra menos arena de la que se cree; (2) resistencia: entra menos arena y más agua libre, cambian las proporciones y la relación a/c, y con ella la resistencia; (3) trabajabilidad: cambia la proporción arena/piedra. Por eso la PCA recomienda dosificar en masa y ajustar por humedad.",
  [pca(115), S("13", 10), navas24(6)],
  respuesta_modelo="La arena húmeda con agua libre aumenta su volumen masivo (V'm = Vm(1+H)). Si no se considera: se compra menos arena real de la pagada (economía); al dosificar por volumen entra menos arena y más agua, lo que altera las proporciones y la relación a/c (resistencia) y la proporción de finos (trabajabilidad). Por eso se dosifica en masa y se ajusta la humedad.",
  puntos_clave=["el agua libre aumenta el volumen masivo (V'm = Vm(1+H))", "economía: se compra menos arena real", "resistencia: cambian las proporciones y la relación a/c", "trabajabilidad: cambia la proporción de arena", "dosificar en masa y corregir humedad"],
  clave="documental")
q("3C", "respuesta_corta",
  "Defina los términos siguientes e indique en qué caso se utiliza uno u otro y porqué: Volumen sólido de cemento; Volumen masivo de cemento.",
  {"doc": "X14", "pag": 1, "pregunta": "1"}, "I-2009",
  "No hay clave oficial; la respuesta se armó solo con las fuentes. Volumen sólido: volumen de las partículas sin los espacios entre ellas (Vs = Ps / (Gs·δw)); es el que entra en el volumen de concreto. Volumen masivo: incluye los espacios entre partículas; se usa cuando se dosifica o se compra por volumen (por ejemplo, unos 0,035 m³ por saco).",
  [S("13", 9), S("13", 10), E("X01", 6, "F/V 1 y 12")],
  respuesta_modelo="El volumen sólido es el de las partículas sin espacios entre ellas (Vs = Ps/(Gs·δw)) y se usa para calcular el volumen de concreto (Vc = Vs cem + ...). El volumen masivo incluye los espacios entre partículas y se usa para dosificar o comprar por volumen (saco de unos 0,035 m³).",
  puntos_clave=["sólido: sin espacios entre partículas", "masivo: incluye los espacios entre partículas", "sólido → cálculo del volumen de concreto", "masivo → dosificación o compra por volumen"],
  clave="documental")
q("3D", "respuesta_corta",
  "Partiendo de los supuestos siguientes para la elaboración de un concreto hidráulico a ser usado en las columnas de un edificio de apartamentos de cuatro pisos: Piedra: se debe escoger entre un tamaño máximo de 13 mm u otro de 19 mm, y en ambos casos la granulometría está dentro de especificaciones ASTM, están limpios y no son reactivos. Arena: con granulometría dentro de especificaciones ASTM y un módulo de finura de 2,2, limpia y no reactiva. Justifique claramente su elección de tamaño máximo de agregado.",
  {"doc": "X14", "pag": 1, "pregunta": "2"}, "I-2009",
  "No hay clave oficial; la respuesta se armó solo con las fuentes. A mayor tamaño máximo, menos superficie que cubrir, menos agua y menos cemento para una relación a/c dada. El tamaño máximo está limitado por la dimensión del elemento y por la separación del refuerzo. Una arena muy fina (MF 2,2, menor que 2,3) aporta trabajabilidad y permite más agregado grueso.",
  [pca(109), pca(112), navas16(21), navas16(22), S("22", 1)],
  respuesta_modelo="Se escoge el mayor tamaño que permitan el elemento y el refuerzo (no más de 1/5 de la dimensión menor ni más de 3/4 de la separación libre entre barras), porque reduce la superficie por cubrir y la demanda de agua y cemento. Con una arena fina (MF 2,2) la mezcla gana trabajabilidad y se puede aumentar el agregado grueso.",
  puntos_clave=["mayor tamaño → menos pasta, agua y cemento", "límite: 1/5 de la dimensión menor y 3/4 de la separación libre del refuerzo", "la arena fina (MF < 2,3) aporta trabajabilidad"],
  clave="documental", verificar="Es una pregunta abierta: la elección final (13 o 19 mm) depende de la separación real del refuerzo, que el enunciado no da.")

# ======================= X17 · I-2019 (teoría, con clave) =======================
# Se agregan al final para no mover los ids de las preguntas anteriores.
I19 = "I-2019"
q("3D", "respuesta_corta",
  "Para la granulometría que se indica, si se corrige en la malla de 2,36 mm (N°8) para que pase el valor correspondiente al límite fino de la especificación, el porcentaje pasando después de la corrección es el que se indica como % pasando corregido. INDIQUE SI o NO y JUSTIFIQUE SU RESPUESTA (5 %)\n"
  "Tamiz · % pasando antes de corrección · % pasando corregido · Especificaciones\n"
  "9,5 mm (3/8): 100 · 100 · 100\n4,75 mm (N°4): 90 · 100 · 95-100\n2,36 mm (N°8): 75 · 100 · 80-100\n"
  "1,18 mm (N°16): 45 · 45 · 50-85\n0,60 mm (N°30): 22 · 22 · 25-60\n0,30 mm (N°50): 9 · 9 · 10-30\n"
  "0,15 (N°100): 7 · 7 · 2-10\nCharola: 0 · 0 · -",
  E("X17", 1, "1"), I19,
  "No es correcto. Según la clave, cada vez que se hace una corrección granulométrica, sea que se elimine o se incorpore material, la masa seca total cambia; por lo tanto, todos los porcentajes pasando cambian, no solo el de la malla corregida. La clave calcula un factor = 100/80 = 1,25 y multiplica por él cada % pasando: N°16 → 56,25; N°30 → 27,5; N°50 → 11,25; N°100 → 8,75. El manual menciona la corrección «con un factor» entre las formas de corregir una curva que no cumple.",
  [S("X17", 1), S("19", 55)],
  respuesta_modelo="No. Al corregir (eliminar o incorporar material) cambia la masa seca total, así que cambian todos los porcentajes pasando. Cada % pasando se multiplica por un factor (en la clave, 100/80 = 1,25).",
  puntos_clave=["No es correcto", "al eliminar o incorporar material cambia la masa seca total", "todos los porcentajes pasando cambian", "cada % pasando se multiplica por un factor"],
  justificacion_oficial="No es correcto. Cada vez que se hace una corrección granulométrica, sea que elimine o se incorpore material, la masa seca total cambia, por lo tanto, todos los porcentajes pasando cambian. Factor = 100/80 = 1.25. Cada uno de los porcentajes pasando se deben multiplicar por este factor.",
  verificar="La clave no cuadra en sí misma: con el factor 1,25 la malla N°8 daría 75 × 1,25 = 93,75, pero su tabla corregida pone 100 (y 100/75 sería 1,33). Las mallas N°16 a N°100 sí siguen el factor 1,25. Lo seguro es el concepto: cambian todos los porcentajes pasando.")
q("3C", "respuesta_corta",
  "¿Existe relación entre el peso unitario masivo seco de un agregado, la relación de vacíos y la granulometría del agregado (mismo agregado y sólo varía su granulometría)? Fundamente su respuesta de manera clara y precisa. (5 %)",
  E("X17", 1, "2"), I19,
  "Sí existe relación. La clave usa δb = Ps / [Vs (1 + e)]: a mayor relación de vacíos (e), menor es el peso unitario masivo seco. Si es el mismo agregado, con una granulometría muy cerrada y otra más abierta, el peso unitario masivo seco es mayor con la más cerrada, porque deja menos volumen de vacíos.",
  [S("X17", 1), S("13", 10)],
  respuesta_modelo="Sí. δb = Ps / [Vs (1 + e)]: a mayor relación de vacíos, menor peso unitario masivo seco. Con el mismo agregado, la granulometría más cerrada deja menos vacíos y da un peso unitario masivo seco mayor que una más abierta.",
  puntos_clave=["Sí existe relación", "δb = Ps / [Vs (1 + e)]", "a mayor relación de vacíos, menor peso unitario masivo seco", "granulometría más cerrada → menos vacíos → mayor peso unitario"],
  justificacion_oficial="Entonces, SÍ existe relación. A mayor relación de vacíos (e), menor es el peso unitario masivo seco de un agregado. Por otro lado, si es el mismo agregado, pero en un caso con una granulometría muy cerrada y en otro caso con granulometría más abierta, el peso unitario masivo seco será mayor cuando la granulometría es más cerrada dado que habrá menos volumen de vacíos.")
q("3D", "seleccion_unica",
  "De acuerdo con las proporciones de dosificación dadas, seleccione aquella que le garantizará el menor costo del concreto. Todos los factores que intervienen en la fabricación del concreto son constantes excepto la proporción y el tamaño máximo nominal del agregado grueso. Justifique su elección, de manera clara y precisa. (5 %)",
  E("X17", 2, "3"), I19,
  "Correcta la opción 1 (1:2,5:3,5 con Tmáx = 19 mm). Según la clave, tiene menos agregado fino (arena), y un tamaño máximo nominal de 19 mm asegura una granulometría menos fina que uno más pequeño como el de 16 mm. A mayor tamaño de las partículas, menor es la superficie específica que hay que cubrir con pasta de cemento, y viceversa; menos pasta significa menos cemento y menor costo. La opción 2 tiene más arena y un Tmáx menor: más superficie que cubrir.",
  [S("X17", 2), S("15", 4)],
  opciones=["Opción 1: 1:2,5:3.5 con Tmáx. = 19 mm", "Opción 2: 1:3:3 con Tmáx. = 16 mm"], correcta="a",
  justificacion_oficial="En la opción 1 se tiene menos agregado fino (arena); por otro lado, un tamaño máximo nominal de 19 mm asegura una granulometría menos fina que si se utilizara uno más pequeño como el de 16 mm. A mayor tamaño de las partículas, menor es la superficie específica a cubrir con la pasta de cemento, y viceversa.")
q("3C", "respuesta_corta",
  "Dé tres razones por las cuales la densidad relativa bruta seca de un agregado es un parámetro importante a considerar en la producción de concreto hidráulico. Utilice el formato dado: «Es un parámetro importante porque» (2 % c/u) · «Explique» (2 % c/u).",
  E("X17", 2, "4"), I19,
  "La clave da cuatro razones (basta con tres): (1) da una idea cuantitativa de qué tan resistente puede ser un agregado: los más porosos tienen menor GBS y son menos resistentes; (2) se relaciona con el peso unitario del concreto, que sirve para calcular las cargas muertas: GBS entre 2,4 y 2,8 corresponden a pesos unitarios volumétricos de 1 120 a 1 900 kg/m³ y a concretos de 2 100 a 2 550 kg/m³ (agregados dentro de especificaciones granulométricas); (3) da una idea relativa de la adherencia con la pasta: a menor GBS, más poroso el agregado y mejor la adherencia; (4) se necesita para las proporciones de la mezcla y las cantidades por comprar: con la GBS se obtiene el volumen bruto, que entra en Vc = Vs + VBA + VBP + Vw + Vaire.",
  [S("X17", 2), S("14", 9), S("13", 9), pca(114)],
  respuesta_modelo="(1) Indica qué tan resistente puede ser: más poroso → menor GBS → menos resistente. (2) Se relaciona con el peso unitario del concreto y las cargas muertas (GBS 2,4–2,8 → 1 120–1 900 kg/m³ → concreto de 2 100–2 550 kg/m³). (3) Indica la adherencia con la pasta: menor GBS → más poroso → mejor adherencia. (4) Sirve para las proporciones y las cantidades por comprar: da el volumen bruto que entra en Vc.",
  puntos_clave=["resistencia: más poroso → menor GBS → menos resistente", "peso unitario del concreto y cargas muertas", "adherencia: menor GBS → más poroso → mejor adherencia", "proporciones: la GBS da el volumen bruto para Vc"],
  justificacion_oficial="Da una idea cuantitativa de qué tan resistente puede ser un agregado (agregados más porosos tienen menor GBS y son menos resistentes). Se puede relacionar con el peso unitario del concreto hidráulico, que es de valor en el cálculo de las cargas muertas (GBS entre 2,4 y 2,8 ↔ pesos unitarios volumétricos entre 1120 y 1900 kg/m³ ↔ concretos entre 2100 y 2550 kg/m³). Da una idea relativa sobre la facilidad de adherencia con la pasta de cemento. Es de interés en el cálculo de las proporciones de la mezcla y de las cantidades de materiales a comprar (VC = VS + VBA + VBP + VW + VAIRE).",
  verificar="La primera razón de la clave (la GBS da idea de la resistencia) choca con la PCA (pág. impresa 114): la gravedad específica «normalmente no se usa como medida de calidad», aunque los agregados porosos suelen tenerla baja. Ninguna de las dos es fuente del profe.")
q("3C", "verdadero_falso",
  "Si el volumen de concreto hidráulico: Vc = Vscem. + VBA + VBP + Vw + Vaire\nY a los agregados les falta agua para llegar a la condición de absorción máxima, el volumen de agua en este caso corresponde a la suma del agua de diseño más el agua que requieren los agregados para alcanzar la condición saturada superficie seca. Responda FALSO o VERDADERO, y justifique su respuesta de manera clara y precisa. (5 %)",
  E("X17", 3, "5, primera parte"), I19,
  "Falso. En la ecuación, el volumen de agua siempre corresponde al agua de diseño. Aunque el volumen bruto es el volumen seco más el agua absorbida y a los agregados les falta agua para llegar a SSS, la corrección por humedad no se hace en el volumen de concreto, sino al determinar la cantidad de agua a dosificar.",
  [S("X17", 3), S("13", 9)], opciones=VF, correcta="b",
  justificacion_oficial="En la ecuación, el volumen de agua siempre corresponde al agua de diseño. Si bien el volumen bruto es el volumen seco más el volumen de agua absorbida, y en este caso les falta agua para alcanzar la condición saturada superficie seca (SSS), la corrección por humedad no se hace en la determinación del volumen de concreto (ecuación dada), sino al momento de determinar la cantidad de agua a dosificar.")
q("3C", "respuesta_corta",
  "Si a la mezcla se incorpora un volumen masivo de cemento, un volumen masivo o masivo hinchado de arena y un volumen masivo de piedra, porqué en la determinación del volumen de concreto no se utilizan estos volúmenes sino los indicados en la fórmula indicada arriba (Vc = Vscem. + VBA + VBP + Vw + Vaire). (3 %)",
  E("X17", 3, "5, segunda parte"), I19,
  "Según la clave, los volúmenes masivos que se incorporan aseguran la masa efectiva necesaria para producir el volumen de concreto proyectado. En el volumen de concreto intervienen los volúmenes efectivos, que se obtienen con esas masas efectivas (por ejemplo, VB = Ps / (GBS·δw)). Al mezclar, las partículas más pequeñas ocupan los espacios que dejan las más grandes y todo se compacta, lo que reduce los vacíos; la vibración los reduce aún más.",
  [S("X17", 3), S("13", 9)],
  respuesta_modelo="Los volúmenes masivos solo aseguran la masa efectiva necesaria; en Vc entran los volúmenes efectivos que salen de esas masas (VB = Ps/(GBS·δw)). Al mezclar, las partículas pequeñas llenan los espacios entre las grandes y se reducen los vacíos, más aún con la vibración.",
  puntos_clave=["los volúmenes masivos aseguran la masa efectiva", "en Vc intervienen los volúmenes efectivos", "VB = Ps/(GBS·δw)", "las partículas pequeñas ocupan los espacios entre las grandes", "la vibración reduce aún más los vacíos"],
  justificacion_oficial="Los volúmenes masivos que se incorporan a la mezcla están asegurando una masa efectiva necesaria para producir un volumen de concreto proyectado, de ahí que en la determinación del volumen de concreto lo que intervienen son los volúmenes efectivos, los que se obtienen con base en esas masas efectivas: Vc = Vscem. + VBA + VBP + Vw + Vaire y VB = Ps/(GBS·δw). Cuando los materiales se mezclan, las partículas más pequeñas ocupan los espacios que dejan las más grandes y todo se compacta reduciendo la cantidad de vacíos, mismos que se reducen aún más por efecto de la vibración.")
q("3A", "respuesta_corta",
  "Para asegurar la resistencia a compresión de un concreto proyectado a 28 MPa es necesario asegurar la buena calidad mecánica de: la pasta de cemento y del agregado grueso. ¿Ambas afirmaciones son correctas? Justifique su respuesta de manera clara y precisa. (5 %)",
  E("X17", 3, "6"), I19,
  "No ambas. Pasta de cemento: correcta; sin importar la resistencia proyectada, la pasta debe ser lo bastante resistente para soportar la resistencia especificada y permitir una buena adherencia pasta-agregado. Agregado grueso: incorrecta para 28 MPa; en concretos por debajo de 34 MPa lo más importante es la adherencia pasta-agregado, no la calidad mecánica del agregado.",
  [S("X17", 3), pca(118), E("X01", 6, "F/V 3")],
  respuesta_modelo="Pasta: sí, debe resistir la resistencia especificada y dar buena adherencia pasta-agregado. Agregado grueso: no; por debajo de 34 MPa lo que importa es la adherencia pasta-agregado y no la calidad mecánica del agregado.",
  puntos_clave=["pasta de cemento: correcta", "la pasta debe soportar la resistencia especificada y adherirse bien al agregado", "agregado grueso: incorrecta", "por debajo de 34 MPa importa la adherencia pasta-agregado, no la calidad mecánica del agregado"],
  justificacion_oficial="Pasta de cemento: la afirmación es correcta. Independientemente de la resistencia proyectada, es necesario lograr una pasta lo suficientemente resistente para que soporte la resistencia especificada y permita una buena adherencia pasta-agregado. Agregado grueso: para concretos por debajo de los 34 MPa, lo más importante es la adherencia pasta-agregado, y no la calidad mecánica del agregado.")
