from comun import S, pca, navas24, navas16, E

P = []


def q(sub, tipo, enunciado, explicacion, fuente, opciones=None, correcta=None, respuesta_modelo=None, puntos_clave=None, verificar=None, figura=None):
    n = len([x for x in P if x["subtema"] == sub]) + 1
    item = {"id": f"p3-{sub}-t{n:02d}", "tema": 3, "subtema": sub, "tipo": tipo, "enunciado": enunciado, "origen": "teoria",
            "clave": "documental", "explicacion": explicacion, "fuente": fuente}
    if opciones is not None:
        item["opciones"] = [{"id": chr(97 + i), "texto": o} for i, o in enumerate(opciones)]
        item["correcta"] = correcta
    if respuesta_modelo:
        item["respuesta_modelo"] = respuesta_modelo
        item["puntos_clave"] = puntos_clave
    if verificar:
        item["verificar"] = verificar
    if figura:
        item["figura"] = figura
    P.append(item)


SU, SM, RC = "seleccion_unica", "seleccion_multiple", "respuesta_corta"

# ---------- 3A ----------
q("3A", SU, "Un agregado con peso unitario masivo seco de 2 240 kg/m³ se clasifica como:",
  "Correcta la C: supera los 1900 kg/m³. La A sería menor que 1120 kg/m³; la B estaría entre 1120 y 1900 kg/m³. La D no existe en la clasificación por peso unitario del curso.",
  [S("14", 9)], ["Liviano", "Normal", "Pesado", "Ultraliviano"], "c")
q("3A", SU, "¿Qué fracción de piedra comercial corresponde a la «quintilla», según el Decreto 10854-MEIC?",
  "Correcta la D. La A es la piedra cuarta, la B la quinta y la C la cuartilla.",
  [S("14", 13)], ["25,0 mm a 4,75 mm", "12,7 mm a 4,75 mm", "19,0 mm a 4,75 mm", "9,5 mm a 2,36 mm"], "d")
q("3A", SM, "Marque los efectos de las partículas planas y elongadas en el concreto endurecido:",
  "Correctas la A, la B y la D: la diapositiva del curso indica más permeabilidad, menos resistencia y menos durabilidad. La C es falsa: estas partículas piden más agua, no menos.",
  [S("15", 20)], ["Aumentan la permeabilidad", "Reducen la resistencia", "Reducen la demanda de agua", "Reducen la durabilidad"], ["a", "b", "d"])
q("3A", SU, "¿Qué norma se aplica a los agregados para concreto de blindaje contra la radiación?",
  "Correcta la B: la ASTM C637 es la especificación de agregados para concreto de blindaje contra la radiación (agregados pesados). La A y la C son para agregados livianos (aislante y estructural) y la D es de partículas planas y elongadas.",
  [S("14", 10), S("14", 11)], ["ASTM C332", "ASTM C637", "ASTM C330", "ASTM D4791"], "b")
q("3A", SU, "Desde el punto de vista de la RESISTENCIA del concreto, ¿qué partícula de agregado se prefiere?",
  "Correcta la C: las partículas angulares, cúbicas y rugosas dan más área de unión y mejor adherencia. La A favorece la trabajabilidad, no la resistencia. La B y la D son quebradizas y bajan la resistencia.",
  [navas24(5)], ["Redondeada y lisa", "Plana", "Angular, cúbica y rugosa", "Elongada"], "c")

# ---------- 3B ----------
q("3B", SU, "Una roca ígnea cuyo magma se enfrió en forma lenta, en el interior de la corteza, tendrá:",
  "Correcta la A: con un enfriamiento lento los cristales crecen y se ven a simple vista (rocas intrusivas). La B corresponde al enfriamiento instantáneo (vidrio) y la C al rápido (volcánicas). La D no tiene relación con la velocidad de enfriamiento.",
  [S("26", 21), S("26", 22)], ["Cristales grandes visibles (roca intrusiva)", "Textura vítrea sin minerales", "Cristales pequeños no visibles (roca volcánica)", "Fragmentos cementados por calcita"], "a")
q("3B", SU, "Según la conferencia de geología, ¿por qué se debe vigilar el contenido de cloruros y sulfatos en agregados de rocas volcánicas antiguas (Grupo Aguacate)?",
  "Correcta la B: la conferencia lo asocia con la corrosión del acero (cloruros) y la expansión del concreto (sulfatos). Las otras opciones no son las razones que da la fuente.",
  [S("26", 28)], ["Porque aumentan la trabajabilidad", "Por la corrosión del acero y la expansión del concreto", "Porque reducen la absorción", "Porque aceleran el curado"], "b")
q("3B", SU, "En el ensayo ASTM C1260 (barra de mortero), ¿cuándo se rechaza el agregado?",
  "Correcta la C: expansión mayor que 0,10 % a los 14 días. La A y la B son los criterios de la ASTM C227 (3 y 6 meses). La D (1 año) corresponde a los cilindros de la ASTM C586 para la reacción álcali-carbonato.",
  [S("15", 17), S("15", 18)], ["Expansión > 0,05 % a los 3 meses", "Expansión > 0,10 % a los 6 meses", "Expansión > 0,10 % a los 14 días", "Expansión medida en cilindros a 1 año"], "c")
q("3B", SU, "¿Cuál de los siguientes es un sulfuro de hierro que puede volver reactivo un agregado?",
  "Correcta la D: pirita, marcasita y pirrotita son sulfuros de hierro. La calcita es carbonato de calcio, la dolomita carbonato de calcio y magnesio, y el cuarzo es sílice.",
  [S("15", 14)], ["Calcita", "Dolomita", "Cuarzo", "Marcasita"], "d")
q("3B", SU, "Según la PCA (Tabla 5-7), ¿qué efecto tienen los terrones de arcilla y las partículas desmenuzables en el concreto?",
  "Correcta la A. La B describe las impurezas orgánicas, la C los agregados reactivos con los álcalis y la D el carbón o lignito.",
  [pca(120)], ["Afectan la trabajabilidad y la durabilidad; pueden causar erupciones", "Afectan el tiempo de fraguado y el endurecimiento",
               "Causan expansión anormal y fisuración en forma de mapa", "Causan manchas en la superficie por ser material ligero"], "a")

# ---------- 3C ----------
q("3C", SU, "Un agregado está en condición saturada superficie seca (SSS) cuando:",
  "Correcta la B: w = D, los poros permeables están llenos y no hay agua en la superficie. La A es seco al horno, la C seco al aire y la D con agua libre.",
  [S("13", 2), navas24(6), S("19", 65)], ["w = 0", "Su humedad es igual a su absorción (w = D)", "w < D", "w > D"], "b")
q("3C", SU, "Una arena tiene un volumen masivo seco de 10 m³ y un hinchamiento de 25 %. ¿Cuál es su volumen masivo hinchado?",
  "Correcta la C: V'm = Vm (1 + H) = 10 × 1,25 = 12,5 m³. La A ignora el hinchamiento; la B divide en lugar de multiplicar; la D suma 25 m³ en lugar de 25 %.",
  [S("13", 10), navas24(7)], ["10,0 m³", "8,0 m³", "12,5 m³", "35,0 m³"], "c")
q("3C", SU, "¿Qué expresión corresponde a la absorción (D) de un agregado?",
  "Correcta la A: D = PWD / Ps × 100, el agua de absorción entre el peso SECO. La B usa el peso total, la C el agua libre (que no es absorción) y la D invierte la razón.",
  [S("19", 66), S("13", 10)], ["D = PWD / Ps × 100", "D = PWD / PT × 100", "D = PWL / Ps × 100", "D = Ps / PWD × 100"], "a")
q("3C", SU, "Si GBS = 2,60 y D = 2 %, ¿cuánto vale la GBSS?",
  "Correcta la B: GBSS = GBS (1 + D) = 2,60 × 1,02 = 2,652 ≈ 2,65. La A ignora la absorción, la C resta en lugar de sumar y la D suma 2 en lugar de 2 %.",
  [S("13", 10)], ["2,60", "2,65", "2,55", "4,60"], "b")
q("3C", SU, "¿Cuál de los siguientes volúmenes incluye los vacíos ENTRE partículas?",
  "Correcta la D: el volumen masivo (Vm) incluye los vacíos entre partículas. El volumen sólido (A) solo considera el sólido; el volumen bruto (B) suma los poros permeables; y el volumen de poros permeables (C) está dentro de las partículas.",
  [S("13", 4), navas24(12)], ["Volumen sólido (Vs)", "Volumen bruto (VB)", "Volumen de poros permeables (Vpp)", "Volumen masivo (Vm)"], "d")
q("3C", SU, "La porosidad (n) y la razón de vacíos (e) se relacionan por:",
  "Correcta la A, según el formulario del curso (ec. 17). Las demás no corresponden a ninguna ecuación del formulario.",
  [S("13", 10)], ["n = e / (1 + e)", "n = e (1 + e)", "n = 1 / (1 + e)", "n = (1 + e) / e"], "a")

# ---------- 3D ----------
q("3D", SU, "Una arena tiene MF = 2,75. Según la tabla del curso, se clasifica como:",
  "Correcta la C: 2,6 a 2,9 es arena media. La A es 2,0–2,3, la B 2,3–2,6 y la D 2,9–3,2.",
  [S("22", 1)], ["Fina", "Medio fina", "Media", "Medio gruesa"], "c")
q("3D", SU, "¿Qué mallas se usan para calcular el módulo de finura de una arena?",
  "Correcta la B: los porcentajes retenidos acumulados de las mallas No. 4, 8, 16, 30, 50 y 100 se suman y se dividen entre 100. La No. 200 y la charola no entran (A, C), y la D omite mallas de la serie.",
  [S("19", 48)], ["No. 4 a No. 200", "No. 4, 8, 16, 30, 50 y 100", "No. 8 a la charola", "Solo No. 30, 50 y 100"], "b")
q("3D", SU, "Una curva granulométrica con un tramo horizontal indica una graduación:",
  "Correcta la D: el tramo horizontal muestra que faltan tamaños (fraccionada o discontinua). La A es la curva suave y continua, la B es casi vertical y la C tiene la parte central vertical con extremos extendidos.",
  [navas16(18)], ["Bien gradada", "Uniforme", "Abierta", "Fraccionada (discontinua)"], "d")
q("3D", SU, "En una losa de 12 cm de espesor, sin otra restricción, el tamaño máximo del agregado no debería exceder:",
  "Correcta la B: un tercio del espesor de la losa da 120/3 = 40 mm. La A sale de usar un quinto, que aplica a la dimensión menor de un elemento. La C sale de 3/4, que aplica a la separación del refuerzo. La D es el espesor completo.",
  [pca(112), navas16(21)], ["24 mm", "40 mm", "90 mm", "120 mm"], "b")

# ---------- 3E ----------
q("3E", SU, "Para reducir una muestra de AGREGADO GRUESO, ¿qué método NO está permitido por la ASTM C702?",
  "Correcta la C: el apilamiento miniatura solo se permite para arena húmeda. Para grueso se usa el separador mecánico (A, preferido) o el cuarteo (B). La D no es un método de la norma.",
  [S("19", 27)], ["Método A, separador mecánico", "Método B, cuarteo", "Método C, apilamiento miniatura", "Ninguno: todos están permitidos"], "c")
q("3E", SU, "En la ASTM C136, ¿cuándo NO deben usarse los resultados para aceptación?",
  "Correcta la A: si la masa total después de tamizar difiere en más de 0,3 % de la inicial. El 1 % (B) es el criterio de suficiencia de tamizado de cada malla. Los 10 minutos (C) son el tiempo máximo de agitación, y agitar más degrada el material, pero no es este criterio. La D es la reducción por cuarteo.",
  [S("19", 53), S("19", 52)], ["Si la masa final difiere más de 0,3 % de la inicial", "Si en la suficiencia pasa menos del 1 %", "Si se agitó durante 10 minutos", "Si la muestra se redujo por cuarteo"], "a")
q("3E", SU, "En la prueba del cono (ASTM C128), al levantar el molde la arena conserva perfectamente su forma. Esto indica que:",
  "Correcta la B: si el cono conserva su forma, todavía hay humedad libre y hay que seguir secando. La A correspondería a un leve desplome, y la C a un desmoronamiento abrupto. La D no es lo que mide la prueba.",
  [S("19", 84)], ["La arena está en condición SSS", "La arena todavía tiene humedad libre", "La arena está más seca que SSS", "La arena tiene impurezas orgánicas"], "b")
q("3E", SU, "En el ensayo ASTM C40, la arena se considera posiblemente perjudicial si el color del líquido es más oscuro que:",
  "Correcta la C: el vidrio estándar No. 3, que equivale a Gardner No. 11. Los demás vidrios no son la referencia de la norma.",
  [S("19", 95)], ["El vidrio No. 1", "El vidrio No. 2", "El vidrio No. 3 (Gardner No. 11)", "El vidrio No. 5"], "c")
q("3E", SU, "En la ASTM C29, procedimiento varillado, ¿cómo se llena y compacta el molde?",
  "Correcta la A. La B describe el procedimiento suelto. La C confunde con los 25 golpes del mazo en el cono de la C128. La D usa un número de capas y de golpes que no da el manual.",
  [S("19", 105), S("19", 106)], ["En 3 capas, con 25 golpes de varilla por capa, sin tocar fuerte el fondo en la primera", "Con cucharón desde no más de 50 mm sobre el borde, sin compactar",
                                 "Con 25 caídas del mazo desde unos 5 mm", "En 2 capas, con 50 golpes por capa"], "a")
q("3E", SU, "En la ASTM C131 (Los Ángeles), ¿cuántas esferas lleva la carga abrasiva de la graduación A?",
  "Correcta la D: A → 12, B → 11, C → 8 y D → 6 esferas.",
  [S("19", 116)], ["6", "8", "11", "12"], "d")
q("3E", SU, "En la ASTM C127, ¿por qué no se recomienda el procedimiento para agregados livianos?",
  "Correcta la B: los poros de los agregados livianos no se llenan necesariamente en 24 h de inmersión. La A, la C y la D no son la razón que da el manual.",
  [S("19", 66), S("19", 67)], ["Porque flotan en el tanque", "Porque sus poros no se llenan de agua en 24 h de inmersión", "Porque se degradan en el horno", "Porque no pasan la malla No. 4"], "b")
q("3E", SM, "Marque el equipo que se usa en la ASTM C117 (material más fino que 75 µm por lavado):",
  "Correctas la A, la B y la C: mallas No. 16 y No. 200, horno a 110 ± 5 °C y un contenedor para agitar con agua. La D (picnómetro) es de la ASTM C128 y la E (vidrios de color) es de la ASTM C40.",
  [S("19", 38)], ["Mallas No. 16 y No. 200", "Horno de 110 ± 5 °C", "Contenedor para agitar la muestra con agua", "Picnómetro", "Vidrio de color estándar"], ["a", "b", "c"])

# ---------- Respuesta corta (teoría) ----------
q("3C", RC, "Explique por qué la condición saturada superficie seca (SSS) es la referencia para dosificar los agregados.",
  "Es la única condición en la que el agregado no absorbe ni cede agua; con cualquier otra humedad cambia el agua efectiva de la mezcla.",
  [navas24(6), pca(115)], respuesta_modelo="Porque en SSS (w = D) el agregado no absorbe ni cede agua a la mezcla. Si está más seco absorbe agua de la pasta y baja la relación a/c real; si tiene agua libre la aporta y la sube.",
  puntos_clave=["w = D", "no absorbe ni cede agua", "seco: absorbe y baja la a/c real", "húmedo: aporta y sube la a/c"])
q("3B", RC, "Describa el mecanismo de la reacción álcali-sílice y mencione dos normas para evaluarla.",
  "Se resume del PCA y de las diapositivas del curso.",
  [pca(122), S("15", 16), S("15", 17)], respuesta_modelo="El hidróxido alcalino de la solución de poros ataca la sílice reactiva del agregado y forma un gel que, al absorber agua, se expande y genera presiones internas que agrietan el concreto. Se evalúa con la ASTM C227 o la ASTM C1260 (barras de mortero) y con la ASTM C289.",
  puntos_clave=["hidróxido alcalino + sílice reactiva → gel", "el gel absorbe agua y se expande", "presiones internas y grietas", "ASTM C227, C1260 o C289"])
q("3D", RC, "¿Por qué el módulo de finura no basta para comparar dos arenas?",
  "Lo dicen Navas y la PCA.",
  [navas16(22), pca(109)], respuesta_modelo="Porque granulometrías muy diferentes pueden dar el mismo MF; solo indica qué tan gruesa o fina es la arena, no su distribución completa ni su calidad.",
  puntos_clave=["el mismo MF con granulometrías distintas", "solo indica finura", "no indica calidad"])
q("3E", RC, "Diferencie la densidad que se obtiene con la ASTM C127 de la que se obtiene con la ASTM C29.",
  "El manual de laboratorio pide hacer esta distinción.",
  [S("19", 66), S("19", 99)], respuesta_modelo="La C127 da la densidad de las partículas del agregado (aparente, bruta seca o SSS), sin los vacíos entre partículas. La C29 da la densidad masiva o peso unitario, que sí incluye los vacíos entre partículas (suelto o varillado).",
  puntos_clave=["C127: densidad de las partículas", "sin vacíos entre partículas", "C29: densidad masiva (peso unitario)", "incluye los vacíos"])
q("3E", RC, "Mencione los tres métodos de reducción de muestras de la ASTM C702 y cuándo se usa cada uno en el agregado fino.",
  "Se resume de la sección 1.2.8.1 del manual.",
  [S("19", 27)], respuesta_modelo="A: separador mecánico, para arena más seca que SSS. B: cuarteo, y C: apilamiento miniatura, para arena con humedad libre en la superficie. Si se quiere usar B o C con arena seca, primero se humedece.",
  puntos_clave=["A: separador, arena seca", "B: cuarteo", "C: apilamiento miniatura", "B o C: arena con humedad libre"])
q("3A", RC, "Mencione cuatro características deseables de un agregado para concreto.",
  "Las da la diapositiva de características deseables del curso.",
  [S("15", 10)], respuesta_modelo="Resistente a compresión y a abrasión, durable, limpio, no reactivo, y con buena forma, textura y graduación.",
  puntos_clave=["resistente", "durable", "limpio", "no reactivo", "forma, textura y graduación"])
