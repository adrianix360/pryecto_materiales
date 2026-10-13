from comun import S, pca, navas24, navas16, E

T = []


def t(sub, tipo, frente, reverso, fuente, figura=None, verificar=None):
    item = {"id": f"t3-{sub}-{len([x for x in T if x['subtema'] == sub]) + 1:02d}", "tema": 3, "subtema": sub,
            "tipo": tipo, "frente": frente, "reverso": reverso, "fuente": fuente, "origen": "teoria"}
    if figura:
        item["figura"] = figura
    if verificar:
        item["verificar"] = verificar
    T.append(item)


# ---------------- 3A. Importancia, clasificación y características ----------------
t("3A", "concepto", "¿Cuáles son los cuatro aspectos en los que los agregados son importantes para el concreto?",
  "Economía, resistencia, trabajabilidad y durabilidad.", [S("15", 3)])
t("3A", "dato", "¿Qué fracción del concreto ocupan los agregados?",
  "Entre 66 % y 78 % del volumen, y entre 70 % y 85 % de la masa.", [S("15", 4)])
t("3A", "dato", "Superficie por cubrir con pasta: ¿agregado grueso de 38 mm o arena de granulometría media?",
  "La arena: unos 388 m² por cada 100 kg, contra unos 14 m² por cada 100 kg en el grueso de 38 mm (1½\"). Por eso los finos piden más pasta.",
  [S("15", 4)])
t("3A", "concepto", "Características deseables de un agregado para concreto",
  "Resistente a la compresión y a la abrasión, durable, limpio, no reactivo, con buena forma, textura y graduación.", [S("15", 10)])
t("3A", "clasificacion", "Clasificación por su proceso de obtención",
  "Natural: de río, de tajo o de mar. Artificial: subproductos de procesos industriales, como la escoria de alto horno (subproducto del acero; sus componentes principales son sílice, alúmina y cal).",
  [S("14", 2), S("14", 8)])
t("3A", "clasificacion", "Clasificación por peso unitario masivo seco (δb)",
  "Pesados: δb > 1900 kg/m³.\nNormales: 1120 < δb < 1900 kg/m³ (2,4 < GBS < 2,8).\nLivianos: δb < 1120 kg/m³.",
  [S("14", 9)])
t("3A", "dato", "Agregados livianos: ejemplos y usos",
  "Perlita y vermiculita expandidas: concreto aislante (ASTM C332). Pómez y escoria: concreto de relleno y aislante. Arcilla o pizarra expandida, cenizas y escoria expandida: concreto estructural (ASTM C330).",
  [S("14", 11)])
t("3A", "dato", "Agregados pesados: ejemplos y función",
  "Barita, magnetita, limonita, ilmenita, ferrofósforo y agregado de acero, entre otros. Se usan en concreto de blindaje contra la radiación (ASTM C637).",
  [S("14", 10), E("X01", 8, "respuesta corta 10")])
t("3A", "clasificacion", "Tamaños comerciales de piedra (Decreto 10854-MEIC)",
  "Tercera: 37,5 a 4,75 mm\nCuarta: 25,0 a 4,75 mm\nCuartilla: 19,0 a 4,75 mm\nQuinta: 12,7 a 4,75 mm\nQuintilla: 9,5 a 2,36 mm",
  [S("14", 13)])
t("3A", "clasificacion", "Formas de partícula y límite de partículas planas y elongadas",
  "Redondeadas, subredondeadas, angulosas o cuboidales, y planas y elongadas. Plana: espesor/ancho < 0,5. Elongada: largo/ancho > 1,5. Máximo 15 % en masa de la muestra (ASTM D4791).",
  [S("15", 19), S("14", 14)])
t("3A", "concepto", "Efectos de las partículas planas y elongadas",
  "En el concreto fresco: más pasta y más agua, mezclado, acabado y vibración más difíciles, más vacíos. En el endurecido: más permeabilidad, menos resistencia y menos durabilidad. En losas dificultan la salida del agua de sangrado.",
  [S("15", 20)])
t("3A", "concepto", "Forma y textura: ¿qué favorece la trabajabilidad y qué la resistencia?",
  "Trabajabilidad: partículas redondeadas y lisas (menos interacción y mejor lubricación de la pasta). Resistencia: partículas angulares, cúbicas y rugosas (más área de unión y mejor adherencia), aunque piden más pasta y agua.",
  [navas24(4), navas24(5), pca(113)])
t("3A", "concepto", "Agregados limpios: efectos nocivos de la suciedad",
  "Interfiere con la hidratación del cemento (problemas de resistencia), retarda el fraguado y deteriora el concreto si hay partículas degradables.",
  [S("15", 12)])
t("3A", "norma", "Normas de abrasión que menciona el curso",
  "ASTM C131: abrasión del agregado grueso en la Máquina de Los Ángeles. ASTM C418: abrasión del concreto por chorro de arena. ASTM C994: abrasión de superficies de concreto o mortero por corte rotativo.",
  [S("15", 11), S("19", 112)])
t("3A", "concepto", "¿Influye la resistencia del agregado en un concreto convencional?",
  "Poco: la resistencia del agregado rara vez se ensaya y, en concreto convencional, influye menos que la resistencia de la pasta y la adherencia pasta-agregado. Se vuelve importante en concreto de alta resistencia.",
  [pca(118)])

# ---------------- 3B. Rocas y reactividad ----------------
t("3B", "clasificacion", "Clasificación de las rocas por su origen",
  "Ígneas: enfriamiento de magma (basalto, granito). Sedimentarias: se forman en la superficie por meteorización, erosión y cementación (arenisca, caliza). Metamórficas: rocas sometidas a muy altas presiones y temperaturas que recristalizan (mármol).",
  [S("26", 9)])
t("3B", "concepto", "Textura de las rocas ígneas según la velocidad de enfriamiento",
  "Instantáneo: textura vítrea, sin minerales (obsidiana, pómez). Rápido: cristales pequeños que no se ven a simple vista (rocas extrusivas o volcánicas). Lento: cristales grandes visibles (rocas intrusivas).",
  [S("26", 21), S("26", 22)])
t("3B", "concepto", "Minerales félsicos y máficos",
  "Félsicos: claros y ricos en sílice (cuarzo, plagioclasa, ortosa, muscovita). Máficos: oscuros y ricos en magnesio y hierro (biotita, anfíbol, piroxeno, olivino).",
  [S("26", 20)])
t("3B", "dato", "¿De qué rocas provienen los mejores agregados en Costa Rica?",
  "De rocas ígneas. Los agregados de río del país son, por lo general, de origen ígneo.",
  [S("26", 11), E("X06", 4, "Pregunta 12")])
t("3B", "concepto", "El agregado ígneo ideal",
  "Proviene de una lava con escasa porosidad (lava densa o piroclástica bien soldada). Es sano (no meteorizado), inerte, con minerales de diverso tamaño fuertemente entrelazados, pocos minerales grandes y poco vidrio volcánico.",
  [S("26", 50)])
t("3B", "concepto", "Rocas volcánicas antiguas (Formación Aguacate, unos 66 millones de años)",
  "Tienen amplia distribución, pero calidad variable: suelen estar alteradas (meteorización y alteración hidrotermal). Hay que vigilar los cloruros (corrosión del acero) y los sulfatos (expansión), y pueden tener sílice amorfa (posible reacción álcali-sílice).",
  [S("26", 28), S("26", 29), S("26", 30), S("26", 31)])
t("3B", "concepto", "Rocas volcánicas recientes (unos 1,6 millones de años)",
  "Son buenos agregados: sanas, duras y tenaces, casi siempre lavas andesíticas. Problemas posibles: textura vesicular, exceso de vidrio, textura seriada y lajamiento (textura fluidal), que producen partículas planas.",
  [S("26", 36), S("26", 51), S("26", 52), S("26", 53), S("26", 54)])
t("3B", "concepto", "Rocas piroclásticas: poco soldadas frente a ignimbritas",
  "Las poco soldadas se enfrían rápido, tienen mucho vidrio y se meteorizan con facilidad. Las ignimbritas están muy soldadas y pueden servir para construcción. En general, las piroclásticas son porosas, gastan mucha pasta y dan malos valores de abrasión Los Ángeles.",
  [S("26", 43), S("26", 45), S("26", 48)])
t("3B", "concepto", "Rocas sedimentarias: clásticas y químicas",
  "Clásticas: fragmentos cementados (arenisca, conglomerado); su resistencia depende del cemento que las une y son poco útiles como agregado. Químicas: por precipitación de químicos en el agua (caliza, sal, yeso).",
  [S("26", 59), S("26", 60), S("26", 62)])
t("3B", "concepto", "Calizas como agregado",
  "Son muy usadas, pero su resistencia varía según el grado de cristalización. Son fáciles de extraer (calcita, dureza 3). En mezclas asfálticas se pulen y no se deben usar en la superficie de ruedo.",
  [S("26", 63), S("26", 64)])
t("3B", "concepto", "Procesos de meteorización química en el trópico",
  "Hidrólisis (los feldespatos forman arcillas), oxidación (por ejemplo, del hierro), hidratación (el agua se combina con el mineral) y disolución (sal, yeso, calizas).",
  [S("26", 34), S("26", 17)])
t("3B", "concepto", "Reactividad álcali-agregado: sus dos formas",
  "Reacción álcali-sílice (RAS) y reacción álcali-carbonato (RAC). La RAS preocupa más porque los agregados con sílice reactiva son más comunes.",
  [pca(121)])
t("3B", "concepto", "Reacción álcali-sílice (RAS)",
  "El hidróxido alcalino ataca los minerales silíceos y forma un gel que se expande al absorber agua. Las presiones internas desintegran la masa de concreto. Se manifiesta entre los 4 y 7 años y es más crítica con ciclos de humedecimiento y secado.",
  [S("15", 16), pca(122)])
t("3B", "concepto", "Las tres condiciones para que ocurra la reacción álcali-agregado",
  "1. Agregado reactivo.\n2. Exceso de álcalis (máximo 0,6 % en masa).\n3. Humedad.\nSi falta una, la reacción no ocurre.",
  [S("15", 13), pca(122)])
t("3B", "concepto", "¿Qué son los álcalis del cemento?",
  "Los óxidos de sodio (Na₂O) y de potasio (K₂O).", [S("15", 15)])
t("3B", "norma", "Ensayos de reacción álcali-sílice",
  "ASTM C227: barras de mortero; rechazo si la expansión supera 0,05 % a los 3 meses o 0,10 % a los 6 meses.\nASTM C1260: barras de mortero; rechazo si supera 0,10 % a los 14 días.\nASTM C289: reactividad potencial; mide la sílice disuelta en hidróxido de sodio.",
  [S("15", 17)])
t("3B", "concepto", "Reacción álcali-carbonato (RAC)",
  "Ocurre con rocas dolomíticas (la dolomita es carbonato de calcio y magnesio). El producto forma grietas en la pasta: el agregado ataca la pasta. Ensayo: ASTM C586, expansión de cilindros de roca en hidróxido de sodio durante 1 año.",
  [S("15", 18), pca(126)])
t("3B", "dato", "Materiales perjudiciales: sustancia, efecto y norma (PCA, Tabla 5-7)",
  "Impurezas orgánicas: afectan el fraguado y el endurecimiento (ASTM C40).\nMaterial más fino que 75 µm: afecta la adherencia y aumenta la demanda de agua (ASTM C117).\nTerrones de arcilla y partículas desmenuzables: afectan la trabajabilidad y la durabilidad (ASTM C142).\nCarbón, lignito y material ligero: afectan la durabilidad y causan manchas (ASTM C123).",
  [pca(120)])
t("3B", "dato", "Sulfuros de hierro que vuelven reactivo un agregado",
  "Pirita, marcasita y pirrotita.", [S("15", 14)])

# ---------------- 3C. Volúmenes, masas y humedad ----------------
t("3C", "clasificacion", "Estados de humedad del agregado",
  "Seco al horno: w = 0.\nSeco al aire: w < D (absorción).\nSaturado superficie seca (SSS): w = D.\nCon agua libre: w > D.",
  [S("13", 2), navas24(6)])
t("3C", "concepto", "¿Por qué la condición SSS es la de referencia?",
  "Es la única condición en la que el agregado no absorbe ni cede agua a la mezcla.", [navas24(6), pca(115)])
t("3C", "concepto", "¿Qué pasa si el agregado está seco o con agua libre al hacer la mezcla?",
  "Seco (w < D): absorbe agua de la pasta, baja la relación a/c real y causa problemas de trabajabilidad. Con agua libre (w > D): aporta agua, sube la relación a/c y la fluidez. En ambos casos cambian la resistencia y la durabilidad.",
  [navas24(6)])
t("3C", "formula", "Agua total del agregado",
  "W = WL + WD: agua libre más agua de absorción.", [S("13", 2), S("13", 10)])
t("3C", "concepto", "Hinchamiento (abundamiento) de la arena",
  "Es el aumento del volumen masivo de la arena húmeda frente al que ocupaba seca. Lo causa el agua libre: la tensión superficial forma meniscos que separan las partículas. Al saturarse, el menisco se destruye y el volumen baja. Es exclusivo de la arena.",
  [navas24(6), pca(115)])
t("3C", "dato", "¿Qué arena se hincha más?",
  "La más fina. Según la curva del curso, la arena fina llega a cerca de 35 % y la gruesa a cerca de 15 %.", [S("13", 3), pca(115)])
t("3C", "formula", "Fórmulas del hinchamiento",
  "H = ΔV / Vm\nV'm = Vm (1 + H)\n(V'm: volumen masivo hinchado)", [S("13", 10), navas24(7)])
t("3C", "concepto", "Volumen sólido, volumen bruto y volumen masivo",
  "Vs: volumen del sólido (incluye los poros impermeables).\nVB = Vs + Vpp: el sólido más los poros permeables.\nVm: el volumen bruto más los vacíos entre partículas.\nV'm: el volumen masivo hinchado.",
  [S("13", 4), navas24(8), navas24(12)])
t("3C", "concepto", "¿Dónde quedan los poros impermeables en los cálculos?",
  "Se consideran parte del volumen sólido, porque no intercambian humedad.", [navas24(8), E("X06", 4, "Pregunta 11")])
t("3C", "formula", "Densidad y gravedad específica aparente",
  "δs = Ps / Vs (solo la porción impermeable de las partículas)\nGs = δs / δw = Ps / (Vs·δw)", [S("13", 5), S("19", 63)])
t("3C", "formula", "Densidad y gravedad específica bruta seca",
  "δBS = Ps / VB (masa seca al horno entre el volumen de las partículas, con poros permeables e impermeables y sin los vacíos entre partículas)\nGBS = δBS / δw = Ps / (VB·δw)",
  [S("13", 6), S("19", 64)])
t("3C", "formula", "Densidad y gravedad específica saturada superficie seca",
  "δBSS = Psss / VB\nGBSS = δBSS / δw = Psss / (VB·δw)", [S("13", 7), S("13", 10), S("19", 65)],
  verificar="La diapositiva 13, pág. 7, escribe la fórmula como δs = Psss/VB, pero el texto de la misma diapositiva y el formulario usan δBSS.")
t("3C", "formula", "Absorción",
  "D = PWD / Ps × 100\n(PWD: peso del agua de absorción; Ps: peso seco)", [S("19", 66), S("13", 10)])
t("3C", "formula", "Relaciones entre gravedades específicas (formulario del curso)",
  "Gs = GBS / (1 − D·GBS)\nGBSS = GBS (1 + D)", [S("13", 10)])
t("3C", "concepto", "Peso unitario (densidad masiva)",
  "Es la masa de una unidad de volumen de agregado, contando las partículas y los vacíos entre ellas: δb = Ps / Vm. Se determina suelto o varillado (ASTM C29). El varillado es más homogéneo porque la muestra se compacta.",
  [S("19", 99), navas24(13)])
t("3C", "dato", "Contenido usual de vacíos",
  "Agregado grueso: 30 % a 45 %. Agregado fino: 40 % a 50 %. Los vacíos aumentan con la angularidad y disminuyen con una mejor granulometría. Afectan la demanda de pasta.",
  [pca(114)])
t("3C", "formula", "Porosidad, razón de vacíos y saturación",
  "n = Vv / Vm\ne = Vv / Vs\nn = e / (1 + e)\nS = Vw / Vv", [S("13", 10), navas24(14)])
t("3C", "formula", "Volumen de concreto",
  "Vc = Vs cemento + VB arena + VB piedra + Vw diseño + Vaire\nLos agregados entran con su volumen bruto (con GBS) y el cemento con su volumen seco (sólido).",
  [S("13", 9)])
t("3C", "dato", "Gravedad específica bruta seca de un agregado de peso normal",
  "Entre 2,4 y 2,8, según la presentación del profe y los exámenes del curso.", [S("14", 9), E("X01", 8, "respuesta corta 9")],
  verificar="Las fuentes no coinciden: el manual (19, pág. 63) dice 2,4–3,0, Navas (24, pág. 2/8) dice 2,5–2,8 y la PCA (pág. 114) dice 2,4–2,9.")
t("3C", "concepto", "¿Para qué se usa la gravedad específica del agregado?",
  "Para calcular el volumen que ocupa el agregado en el diseño de mezclas por volumen absoluto. Normalmente no se usa como medida de calidad.",
  [pca(114), S("19", 63)])
t("3C", "dato", "Volumen masivo de un saco de cemento de uso general",
  "Aproximadamente 0,035 m³. Ese es el volumen masivo, no el volumen efectivo (sólido).",
  [E("X01", 6, "F/V 12"), E("X06", 2, "Pregunta 6")])

# ---------------- 3D. Granulometría ----------------
t("3D", "concepto", "Granulometría (análisis granulométrico)",
  "Es la distribución porcentual en masa de los tamaños de partícula de un agregado. Se obtiene pasando una muestra seca por mallas en orden decreciente de abertura (ASTM C136).",
  [S("19", 47), navas16(17)])
t("3D", "concepto", "¿Por qué importa la granulometría?",
  "Define cuánta pasta se necesita para lograr trabajabilidad, resistencia y durabilidad, y afecta la contracción. Un agregado bien graduado reduce los vacíos y, con eso, la pasta y el costo.",
  [navas16(17), pca(107)])
t("3D", "clasificacion", "Tipos de curva granulométrica",
  "Bien gradada: curva suave y continua.\nUniforme: casi vertical (un solo tamaño).\nAbierta: parte central vertical con extremos extendidos.\nFraccionada o discontinua: con un tramo horizontal porque faltan tamaños.",
  [navas16(18)])
t("3D", "concepto", "Agregado fino y agregado grueso",
  "Fino: pasa la malla No. 4 (4,75 mm) y queda retenido en la No. 200 (75 µm). Grueso: queda retenido en la malla No. 4.",
  [navas16(18), S("19", 6)])
t("3D", "dato", "Límites ASTM C33 para el agregado fino (% pasando)",
  "9,5 mm: 100\nNo. 4: 95–100\nNo. 8: 80–100\nNo. 16: 50–85\nNo. 30: 25–60\nNo. 50: 5–30\nNo. 100: 0–10\nAdemás: no más de 45 % retenido entre dos mallas consecutivas.",
  [navas16(19), pca(108), pca(109)])
t("3D", "concepto", "Tamaño máximo y tamaño máximo nominal",
  "Tamaño máximo: la malla más pequeña por la que pasa el 100 % del material. Tamaño máximo nominal: el mayor tamaño de malla donde queda retenido material, respetando un retenido máximo permisible.",
  [S("19", 9), S("19", 50)],
  verificar="Otras fuentes lo dicen distinto. Navas (16, pág. 2/21): la mayor abertura por la que pasa el 85–95 %. PCA (pág. 111): el menor tamiz por el que pasa la mayor parte, pudiendo retener del 5 al 15 %.")
t("3D", "dato", "Límites del tamaño máximo según el elemento",
  "No debe exceder un quinto de la dimensión menor del elemento, un tercio del espesor de la losa ni tres cuartos de la separación libre entre barras de refuerzo.",
  [navas16(21), pca(112)])
t("3D", "formula", "Módulo de finura (MF)",
  "MF = Σ % retenidos acumulados en las mallas No. 4, 8, 16, 30, 50 y 100 / 100\nA mayor MF, más grueso el agregado.",
  [S("19", 48), S("19", 55), navas16(22)])
t("3D", "dato", "Rango aceptable del módulo de finura de la arena",
  "Mayor que 2,3 y menor que 3,1. Además, no debe variar más de 0,2 respecto del valor típico de la fuente.",
  [S("19", 48), navas16(22), pca(109)])
t("3D", "clasificacion", "Clasificación de la arena por módulo de finura",
  "< 2,0 muy fina · 2,0–2,3 fina · 2,3–2,6 medio fina · 2,6–2,9 media · 2,9–3,2 medio gruesa · 3,2–3,5 gruesa · > 3,5 muy gruesa",
  [S("22", 1)])
t("3D", "concepto", "Limitación del módulo de finura",
  "Granulometrías muy diferentes pueden dar el mismo MF, así que no sirve para comparar agregados distintos. Solo indica qué tan gruesa o fina es la arena, no su calidad.",
  [navas16(22), pca(109), E("X01", 6, "F/V 7")])
t("3D", "concepto", "Si la curva no cumple la ASTM C33, ¿cómo se corrige?",
  "Por masa retenida, con un factor, con una fórmula matemática o combinando agregados.", [S("19", 55)])
t("3D", "concepto", "Granulometría discontinua",
  "Se omiten a propósito algunos tamaños de partícula. Se usa en concreto arquitectónico con agregado expuesto y también en concreto estructural normal.",
  [pca(112)])

# ---------------- 3E. Ensayos de laboratorio ----------------
def fig(nombre, alt, pags):
    return {"src": f"img/ensayos/{nombre}.jpg", "alt": alt,
            "fuente": [S("19", p) for p in pags]}


FIG = {
    "d75": fig("d75", "Muestreo: cargador remezclando la pila, división del área en cuadrantes A-B-C-D, tablilla horizontal sobre el punto de muestreo y plantilla para bases.", [11, 12, 14]),
    "c702": fig("c702", "Reducción: separador mecánico de canales, y cuarteo (apilar en cono, dividir en cuartos y retirar dos cuartos opuestos).", [25, 29]),
    "c117": fig("c117", "Lavado: cubrir con agua, agitar, verter el agua sobre las mallas anidadas y retornar el material retenido.", [40]),
    "c136": fig("c136", "Granulometría: juego de mallas, colocación de la muestra, agitador mecánico y suficiencia de tamizado manual.", [49, 51, 52, 53]),
    "c127": fig("c127", "Grueso: canasta de alambre, inmersión 24 h, secado superficial con paño (SSS) y pesaje sumergido en el tanque.", [68, 70]),
    "c128": fig("c128", "Fino: molde cónico y mazo, apisonado con 25 caídas, leve desplome del cono (SSS) y picnómetro.", [81, 84, 85]),
    "c40": fig("c40", "Impurezas orgánicas: botella graduada, nivel de 130 ml de arena, vidrios de color estándar y comparación del color.", [93, 94, 95]),
    "c29": fig("c29", "Peso unitario: llenado suelto con cucharón, varillado por capas, enrasado y pesaje del molde.", [104, 105, 106]),
    "c131": fig("c131", "Abrasión: Máquina de Los Ángeles, carga del agregado y de las esferas, y tamizado posterior.", [114, 116]),
}

ENSAYOS = [
    ("d75", "ASTM D75 · Muestreo de agregados en campo",
     ["Obtener una muestra representativa: el muestreo es tan importante como el ensayo; si la muestra no es representativa, los resultados no son confiables.",
      "Fuente de descarga continua: unidades elegidas al azar (ASTM D3665), al menos 3 porciones de toda la sección del flujo; nunca de la descarga inicial ni final.",
      "Banda transportadora: detenerla, insertar 2 plantillas, sacar todo el material entre ellas y recoger los finos con escobilla.",
      "Pila: evitar muestrear pilas y unidades de transporte; si es necesario, hacer un plan de muestreo. Con cargador: remezclar, dividir en 4 cuadrantes y no muestrear a menos de 0,3 m de los bordes. Sin maquinaria: tercios superior, medio e inferior, con tablilla. Arena: tubo muestreador, al menos 5 inserciones, a 1 m de altura como mínimo."],
     "Balanza móvil (no requiere precisión), termómetro-higrómetro, pala, sacos, plantillas, brocha, tubo muestreador (unos 30 mm de diámetro, 2 m de largo y punta cortada a 45°) y tablones o tablilla.",
     "Masa mínima de muestra de campo según el tamaño máximo nominal: 37,5 mm → 75 kg; 25 mm → 50 kg; 19 mm → 25 kg; 12,7 mm → 15 kg; 9,5 mm → 10 kg; arena → 10 kg. Si es mezcla de grueso y fino, la del grueso más 10 kg.",
     "La norma no da un resultado numérico: se reporta la información de la bitácora y la masa obtenida al gramo más cercano. Las muestras van en sacos identificados para evitar pérdidas y contaminación.",
     [S("19", 6), S("19", 8), S("19", 9), S("19", 10), S("19", 11), S("19", 12), S("19", 14), S("19", 15)]),
    ("c702", "ASTM C702 · Reducción de muestras a tamaño de ensayo",
     ["Revisar el tipo de agregado y su humedad para elegir el método.",
      "Método A, separador mecánico: distribuir la muestra en la tolva y vaciarla con flujo libre; quedarse con una mitad y repetir hasta llegar a la masa necesaria.",
      "Método B, cuarteo: en una superficie rígida y nivelada, mezclar al menos 3 veces, apilar en cono, aplanar hasta un diámetro de 4 a 8 veces el espesor, dividir en 4 y retirar 2 cuartos opuestos.",
      "Método C, apilamiento miniatura (solo arena húmeda): igual que el cono aplanado, pero se toman al menos 5 incrementos en lugares al azar."],
     "Separador mecánico con número par de canales (al menos 8 para grueso y 12 para fino; en arena seca, canales de 12,5 a 20 mm), pala o cucharón, brocha, balanza y termómetro.",
     "Grueso o mezcla: método A (preferido) o B; el C no se permite. Arena más seca que SSS: método A. Arena con agua libre: método B o C. El ancho del canal debe ser al menos 50 % mayor que la partícula más grande.",
     "Se reporta la masa de cada reducción al gramo más cercano. Si una o dos partículas grandes pueden sesgar la interpretación, se ensaya la muestra completa.",
     [S("19", 23), S("19", 24), S("19", 25), S("19", 27), S("19", 28), S("19", 29), S("19", 30)]),
    ("c117", "ASTM C117 · Material más fino que 75 µm (No. 200) por lavado",
     ["Secar el espécimen a masa constante a 110 ± 5 °C y pesar.",
      "Cubrirlo con agua (procedimiento A) o con agua y agente humectante (B) y agitar para poner en suspensión los finos.",
      "Verter el agua de lavado sobre las mallas anidadas (la No. 16 arriba y la No. 200 abajo), evitando decantar partículas gruesas. Repetir hasta que el agua salga clara.",
      "Retornar a la muestra el material retenido en las mallas, secar a masa constante y pesar."],
     "Balanza legible a 0,1 g, mallas No. 16 (1,18 mm) y No. 200 (0,075 mm), contenedor, horno de 110 ± 5 °C y agente humectante opcional.",
     "Se usa el procedimiento A salvo que la especificación pida otro. Masa mínima si la muestra es solo para la C117: 300 g para arena (4,75 mm o menos), 1000 g hasta 9,5 mm, 2500 g hasta 19 mm y 5000 g para 37,5 mm o más.",
     "L (%) = (Minicial − Mfinal) / Minicial × 100. Se reporta al 0,1 % si es menor que 10 %. Si se pierde material al decantar, el ensayo se desecha. Se hace antes de la granulometría (C136).",
     [S("19", 36), S("19", 38), S("19", 39), S("19", 40), S("19", 41), S("19", 42)]),
    ("c136", "ASTM C136 · Análisis granulométrico",
     ["Si hace falta conocer los finos, hacer primero la C117; lavar, secar a 110 ± 5 °C y pesar.",
      "Anidar las mallas de mayor a menor abertura con tapa y charola, y colocar la muestra en la malla superior.",
      "Agitar a mano o con agitador mecánico, máximo 10 minutos (más tiempo degrada el material).",
      "Suficiencia de tamizado: unos 150 golpes por minuto, girando la malla 1/6 de vuelta cada 25 golpes, hasta que pase menos del 1 % de lo retenido. Pesar lo retenido en cada malla."],
     "Mallas según ASTM E11, agitador mecánico, balanza (0,1 g para arena; 0,5 g para grueso), horno de 110 ± 5 °C, recipientes, brocha y cepillo de bronce.",
     "Masa mínima: arena 300 g; grueso según el tamaño máximo nominal (37,5 mm → 15 kg; 25 mm → 10 kg; 19 mm → 5 kg; 12,7 mm → 2 kg; 9,5 mm → 1 kg). Sobrecarga: en mallas menores que la No. 4, máximo 7 kg/m² (unos 200 g en malla de 203 mm).",
     "Si la masa total después de tamizar difiere en más de 0,3 % de la inicial, el resultado no sirve para aceptación. Se calculan el % retenido, el % retenido acumulado, el % pasando y el MF (al 0,01), y se grafica la curva contra los límites de la C33.",
     [S("19", 47), S("19", 48), S("19", 49), S("19", 50), S("19", 51), S("19", 52), S("19", 53), S("19", 54), S("19", 55)]),
    ("c127", "ASTM C127 · Gravedad específica y absorción del agregado grueso",
     ["Desechar lo que pasa la malla No. 4 y lavar; secar a 110 ± 5 °C.",
      "Sumergir en agua 24 ± 4 h.",
      "Pesar sumergido en la canasta (agua del tanque a 23 ± 2 °C, removiendo el aire atrapado).",
      "Secar la superficie con el paño hasta quitar el brillo (condición SSS) y pesar Msss. Luego secar al horno a masa constante y pesar Mseca."],
     "Canasta de alambre No. 6 (3,35 mm) de 4 a 7 L, balanza con sistema de suspensión, tanque de agua, malla No. 4, horno de 110 ± 5 °C, paño absorbente y termómetro.",
     "Masa mínima según el tamaño máximo nominal: 37,5 mm → 5 kg; 25 mm → 4 kg; 19 mm → 3 kg; 12,7 mm o menos → 2 kg. No se recomienda para agregados livianos (δBS < 1120 kg/m³), porque sus poros no se llenan en 24 h.",
     "GBS = Mseca / (Msss − Msum)\nGBSS = Msss / (Msss − Msum)\nGs = Mseca / (Mseca − Msum)\nD = (Msss − Mseca) / Mseca × 100\nSe reporta la gravedad específica al 0,01 y la absorción al 0,1 %.",
     [S("19", 66), S("19", 67), S("19", 68), S("19", 69), S("19", 70), S("19", 71), S("19", 72)]),
    ("c128", "ASTM C128 · Gravedad específica y absorción del agregado fino",
     ["Usar el material que pasa la malla No. 4, secarlo y sumergirlo en agua 24 ± 4 h.",
      "Decantar y secar en bandeja con aire caliente, removiendo, hasta acercarse a la condición SSS.",
      "Prueba del cono: llenar el molde, apisonar con 25 caídas libres del mazo desde unos 5 mm y levantar el molde. Si hay un leve desplome, la arena está en SSS.",
      "Meter 500 ± 10 g de arena SSS en el picnómetro, llenar al 90 %, eliminar las burbujas (15 a 20 min), enrasar a 23 ± 2 °C y pesar. Luego secar la arena al horno y pesar Mseca."],
     "Picnómetro (método gravimétrico), molde cónico (40 mm arriba, 90 mm abajo y 75 mm de alto) con mazo de 340 g, soplador de aire caliente, horno de 110 ± 5 °C, balanza de 0,1 g, agua destilada y termómetro.",
     "Si el cono no se desploma, todavía hay humedad libre; si se desmorona de golpe, la arena ya está más seca que SSS. Muestra de 4 kg reducida a 1 kg aproximadamente.",
     "GBS = Mseca / (Mcal + Msss − Msum)\nD = (Msss − Mseca) / Mseca × 100\n(Mcal: picnómetro con agua hasta la marca; Msum: picnómetro con agua y muestra)",
     [S("19", 81), S("19", 82), S("19", 83), S("19", 84), S("19", 85), S("19", 86), S("19", 87)]),
    ("c40", "ASTM C40 · Impurezas orgánicas en el agregado fino",
     ["Reducir la arena a unos 450 g.",
      "Llenar la botella hasta el nivel de 130 ml con arena.",
      "Añadir solución de hidróxido de sodio al 3 % hasta un volumen total de 200 ml.",
      "Tapar, agitar con vigor y dejar reposar 24 h; comparar el color del líquido con los vidrios de color estándar."],
     "Botella de vidrio transparente graduada (240 a 470 ml), vidrio de color estándar con 5 colores (escala Gardner), solución de NaOH al 3 % y balanza.",
     "Solución: 3 partes en masa de NaOH en 97 partes de agua. Es una prueba cualitativa: no lleva cálculos ni precisión.",
     "Si el líquido es más oscuro que el vidrio estándar No. 3 (Gardner No. 11), la arena posiblemente tiene impurezas orgánicas perjudiciales. Se recomienda entonces el ensayo de resistencia en mortero (ASTM C87) antes de aprobarla.",
     [S("19", 92), S("19", 93), S("19", 94), S("19", 95), S("19", 98)]),
    ("c29", "ASTM C29 · Peso unitario (densidad masiva) y vacíos",
     ["Secar la muestra a 110 ± 5 °C y mezclarla sin segregar.",
      "Suelto: llenar el molde con cucharón hasta desbordar, descargando a no más de 50 mm sobre el borde, enrasar y pesar.",
      "Varillado: llenar en 3 capas y dar 25 golpes de varilla por capa, sin tocar el fondo en la primera ni penetrar la capa anterior; enrasar y pesar.",
      "Hacer 3 determinaciones de cada procedimiento y promediar."],
     "Varilla de acero de 16 mm de diámetro y unos 600 mm de largo, molde cilíndrico rígido de metal (altura entre 80 % y 150 % del diámetro), regla enrasadora, cucharón, malla No. 4, horno y balanza.",
     "Para agregados de tamaño máximo nominal de hasta 37,5 mm. Masa de muestra entre 125 % y 200 % de la necesaria para llenar el molde. Masas al 0,05 kg.",
     "δb = (Mmolde+muestra − Mmolde) / Vmolde\n% vacíos = (GBS·W − δb) / (GBS·W) × 100, con W = 997,5 kg/m³\nSe reporta δb al 10 kg/m³ y los vacíos al 1 %.",
     [S("19", 99), S("19", 102), S("19", 103), S("19", 104), S("19", 105), S("19", 106), S("19", 107)]),
    ("c131", "ASTM C131 · Abrasión en la Máquina de Los Ángeles",
     ["Lavar, secar a 110 ± 5 °C, separar por tamaños y recombinar según la graduación A, B, C o D (5000 g en total).",
      "Escoger la carga abrasiva (esferas de acero) según la graduación y pesar Minicial.",
      "Hacer girar la máquina a 30–33 rev/min durante 500 revoluciones.",
      "Tamizar en la malla No. 12, lavar lo retenido, secar a masa constante y pesar Mfinal."],
     "Máquina de Los Ángeles (cilindro de acero de 711 mm de diámetro interno y 508 mm de largo, con repisa interna), esferas de acero de unos 46,8 mm (390 a 445 g), malla No. 12, horno y balanza.",
     "Carga abrasiva: graduación A → 12 esferas; B → 11; C → 8; D → 6. Se aplica a agregado grueso menor que 37,5 mm. Mide la degradación por abrasión o desgaste, impacto y trituración.",
     "A (%) = (Minicial − Mfinal) / Minicial × 100, reportado al 1 %. Las especificaciones fijan una pérdida máxima. Ejemplo del manual: 21,6 % → se reporta 22 %.",
     [S("19", 112), S("19", 113), S("19", 114), S("19", 115), S("19", 116), S("19", 117)]),
]

for clave, titulo, pasos, equipo, parametros, criterio, fuentes in ENSAYOS:
    verif = None
    if clave == "c131":
        verif = "El manual llama a la malla No. 12 de 1,17 mm en la lista de equipo (pág. 113) y de 1,70 mm en el procedimiento (pág. 116)."
    if clave == "c29":
        verif = "El 'Resumen' de la sección del C29 en el manual (pág. 111) describe por error el ensayo de impurezas orgánicas (C40); no se usa."
    t("3E", "proceso", f"{titulo}: pasos", "\n".join(f"{i + 1}. {p}" for i, p in enumerate(pasos)), fuentes,
      figura=FIG[clave], verificar=verif)
    t("3E", "equipo", f"{titulo}: equipo", equipo, fuentes, figura=FIG[clave])
    t("3E", "parametros", f"{titulo}: parámetros clave", parametros, fuentes)
    t("3E", "criterio", f"{titulo}: resultado y criterio", criterio, fuentes)

t("3E", "concepto", "¿Por qué se usa el método A (separador) para arena seca y el B o C para arena con agua libre?",
  "El separador necesita que el material fluya libre por los canales; si la arena tiene humedad libre, se pega. En el cuarteo o el apilamiento miniatura, la arena húmeda conserva la forma del cono. Si se quiere usar B o C con arena seca, primero se humedece.",
  [S("19", 27)])
t("3E", "concepto", "¿En qué se diferencia la densidad que da el C127/C128 de la que da el C29?",
  "El C127 y el C128 dan la densidad de las partículas, sin los vacíos entre ellas. El C29 da la densidad masiva, que sí incluye los vacíos entre partículas.",
  [S("19", 66), S("19", 80)])
t("3E", "concepto", "Humedad libre a partir del C566",
  "El ASTM C566 da el contenido total de humedad por secado. La humedad libre es esa humedad total menos la absorción.",
  [S("19", 66)])

# ---------------- Teoría del I examen 2019 (X17) ----------------
# Se agregan al final para no mover los ids de las tarjetas anteriores.
t("3D", "concepto", "Si se corrige la granulometría en una malla, ¿qué pasa con los demás porcentajes pasando?",
  "Cambian todos. Al eliminar o incorporar material, cambia la masa seca total, así que cambian todos los porcentajes pasando, no solo el de la malla corregida. Cada % pasando se multiplica por un mismo factor.",
  [S("X17", 1), S("19", 55)])
t("3C", "concepto", "Relación entre peso unitario masivo seco, relación de vacíos y granulometría",
  "δb = Ps / [Vs (1 + e)]. A mayor relación de vacíos (e), menor peso unitario masivo seco. En un mismo agregado, una granulometría más cerrada deja menos vacíos y da un δb mayor que una más abierta.",
  [S("X17", 1), S("13", 10)])
t("3D", "concepto", "¿Por qué menos arena y un tamaño máximo nominal mayor abaratan el concreto?",
  "Dan una granulometría menos fina. A mayor tamaño de las partículas, menor superficie específica que cubrir con pasta de cemento, y viceversa: menos pasta, menos cemento, menor costo. Ejemplo del examen de 2019: 1:2,5:3,5 con Tmáx 19 mm sale más barato que 1:3:3 con Tmáx 16 mm.",
  [S("X17", 2), S("15", 4)])
t("3C", "concepto", "¿Por qué importa la densidad relativa bruta seca (GBS) al producir concreto?",
  "1. Resistencia: los agregados más porosos tienen menor GBS y son menos resistentes.\n2. Peso unitario del concreto y cargas muertas: GBS de 2,4 a 2,8 ↔ pesos unitarios de 1 120 a 1 900 kg/m³ ↔ concretos de 2 100 a 2 550 kg/m³.\n3. Adherencia: a menor GBS, más poroso el agregado y mejor la adherencia con la pasta.\n4. Dosificación y compra: con la GBS se obtiene el volumen bruto, VB = Ps / (GBS·δw), que entra en Vc.",
  [S("X17", 2), S("14", 9), S("13", 9)],
  verificar="La razón 1 sale de la clave de 2019; la PCA (pág. impresa 114) dice que la gravedad específica normalmente no se usa como medida de calidad. El rango de 2 100 a 2 550 kg/m³ del concreto solo aparece en esa clave.")
t("3C", "concepto", "En Vc = Vs cem + VBA + VBP + Vw + Vaire, ¿qué agua es Vw y por qué no se usan los volúmenes masivos?",
  "Vw es siempre el agua de diseño, aunque a los agregados les falte agua para llegar a SSS: la corrección por humedad se hace al calcular el agua a dosificar, no en Vc.\nLos volúmenes masivos solo aseguran la masa efectiva; en Vc entran los volúmenes efectivos de esas masas (VB = Ps / (GBS·δw)). Al mezclar, las partículas pequeñas llenan los espacios entre las grandes y la vibración reduce aún más los vacíos.",
  [S("X17", 3), S("13", 9)])
