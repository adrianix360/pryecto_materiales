"""Catálogo de normas ASTM para el entrenamiento «Normas» (data/normas.json).

Cada norma: qué determina («mide», con las palabras de la fuente), con cuáles se confunde, un gancho
de memoria (ayuda de Claude, NO dato del curso: la app lo rotula así) y su fuente con página.
Regla del proyecto: nada inventado. Lo que no tenga respaldo lleva «verificar».
Nombres y páginas: ver comentarios en cada entrada. Códigos de fuente: comun.FUENTES (17 = manual de cementos).
"""
from comun import S

FAMILIAS = [
    {"id": "muestreo", "titulo": "Muestreo y reducción"},
    {"id": "granulometria", "titulo": "Granulometría y finos"},
    {"id": "densidad", "titulo": "Densidad, vacíos y humedad"},
    {"id": "calidad", "titulo": "Calidad del agregado: impurezas y abrasión"},
    {"id": "forma", "titulo": "Forma de las partículas"},
    {"id": "reactividad", "titulo": "Reactividad álcali-agregado"},
    {"id": "agua", "titulo": "Agua para concreto"},
    {"id": "mortero", "titulo": "Mortero y cemento"},
]

# (id, familia, mide, detalle, confunde_con, gancho, fuente, verificar)
_N = [
    ("D75", "muestreo", "Muestreo de agregados en campo", "",
     ["C702"], "Primero se toma la muestra en campo (D75) y después se reduce al tamaño de ensayo (C702).",
     [S("19", 6), S("08", 3)], ""),
    ("C702", "muestreo", "Reducción de muestras de agregado", "",
     ["D75"], "La C702 viene después de la D75: ya tenés la muestra y hay que reducirla.",
     [S("19", 23), S("08", 3)], ""),

    ("C117", "granulometria", "Material más fino que 75 µm (malla No. 200) en el agregado, por lavado",
     "", ["C136"], "Lavar: lo fino pasa la malla No. 200 con el agua (117 lava; 136 tamiza).",
     [S("19", 36), S("08", 3)], ""),
    ("C136", "granulometria", "Análisis granulométrico de agregados finos y gruesos",
     "", ["C117", "C33"], "La torre de mallas es la 136. Los límites de la curva son los de la C33.",
     [S("19", 47), S("08", 3)], ""),
    ("C33", "granulometria", "Especificaciones estándar de agregados para concreto",
     "La PCA presenta con la C33 los límites granulométricos del fino y del grueso (11, págs. 3 a 5).",
     ["C136"], "La C33 es la especificación (los límites); la C136 es el ensayo que da la curva.",
     [S("19", 6), S("11", 3), S("08", 3)], ""),

    ("C127", "densidad", "Densidad relativa (gravedad específica) y absorción del agregado grueso",
     "", ["C128"], "Los dos números van seguidos: el 127 es el grueso y el 128, el fino.",
     [S("19", 62), S("13", 11), S("08", 3)], ""),
    ("C128", "densidad", "Densidad relativa (gravedad específica) y absorción del agregado fino",
     "", ["C127"], "El 128 viene después del 127: primero el grueso, luego el fino.",
     [S("19", 76), S("13", 11), S("08", 3)], ""),
    ("C29", "densidad", "Densidad masiva (peso unitario) y vacíos en agregados",
     "", ["C566"], "29: el peso unitario, lo que pesa el recipiente lleno de agregado.",
     [S("19", 99), S("08", 2)], ""),
    ("C566", "densidad", "Contenido de humedad de una muestra de agregado, por secado",
     "", ["C29"], "566: la humedad, se seca la muestra y se compara la masa.",
     [S("19", 66), S("08", 1)], ""),

    ("C40", "calidad", "Impurezas orgánicas en el agregado fino",
     "", ["C131"], "40: la colorimetría del agregado fino (impurezas orgánicas).",
     [S("19", 92), S("08", 3)], ""),
    ("C131", "calidad", "Resistencia a la degradación del agregado grueso por abrasión e impacto, en la Máquina de Los Ángeles",
     "", ["C418", "C994"], "131: Los Ángeles, el tambor con bolas de acero.",
     [S("19", 112), S("15", 11), S("08", 3)], ""),
    ("C418", "calidad", "Resistencia a la abrasión del hormigón mediante chorro de arena",
     "", ["C131", "C994"], "418: chorro de arena.",
     [S("15", 11)], ""),
    ("C994", "calidad", "Resistencia a la abrasión en superficies de concreto o mortero por el método de corte rotativo",
     "", ["C131", "C418"], "994: corte rotativo (la herramienta que gira sobre la superficie).",
     [S("15", 11)],
     "La diapositiva (15, pág. 11) dice ASTM C994; ese método podría ser la ASTM C944 (dígitos invertidos). "
     "Ninguna fuente del curso dice C944: consultar con el profe."),

    ("D4791", "forma", "Partículas planas, elongadas, o planas y elongadas, en agregado grueso",
     "Planas: espesor/ancho < 0,5. Elongadas: largo/ancho > 1,5. Máximo 15 % en masa de la muestra (15, pág. 19).",
     ["D5821"], "D4791 = planas y elongadas (se mide la relación largo/ancho/espesor).",
     [S("14", 14), S("15", 19), S("15", 20), S("08", 3)],
     "La clave del examen de I-2025 dice D4790 y D5260; las diapositivas dicen D4791 (ALCANCE.md, C14)."),
    ("D5821", "forma", "Porcentaje de partículas fracturadas en agregado grueso",
     "La diapositiva lo muestra con partículas angulosas o cuboidales (15, pág. 19).",
     ["D4791"], "D5821 = fracturadas (caras partidas). No son las planas ni las elongadas: esas son D4791.",
     [S("15", 19)], ""),

    ("C227", "reactividad", "Prueba de barra de mortero: expansiones por reactividad álcali-sílice, a 3 y 6 meses",
     "Rechazo si la expansión es > 0,05 % en 3 meses o > 0,10 % en 6 meses (15, pág. 17).",
     ["C1260", "C289"], "C227 es la barra lenta (meses); C1260 es la barra rápida (14 días).",
     [S("15", 17), S("08", 3)], ""),
    ("C1260", "reactividad", "Prueba de barra de mortero: expansiones a 14 días",
     "Rechazo si la expansión es > 0,10 % en 14 días (15, pág. 17).",
     ["C227", "C289"], "C1260 es la barra rápida: 14 días. La C227 tarda meses.",
     [S("15", 17), S("08", 3)], ""),
    ("C289", "reactividad", "Reactividad potencial del agregado: sílice disuelto en solución de hidróxido de sodio",
     "", ["C227", "C1260"], "C289 es química: se mide sílice disuelto, no expansión de barras.",
     [S("15", 17)], ""),
    ("C586", "reactividad", "Reactividad álcali-carbonato: expansiones de cilindros de roca en hidróxido de sodio, 1 año",
     "El producto de la reacción forma grietas en la pasta: el agregado ataca la pasta (15, pág. 18).",
     ["C227", "C1260", "C289"], "C586: carbonatos, cilindros de roca, un año (dolomita).",
     [S("15", 18), S("08", 3)], ""),

    ("C1602", "agua", "Especificación del agua de mezcla para concreto de cemento hidráulico (límites químicos y requisitos de desempeño)",
     "La tabla de límites químicos (05, pág. 8) cita la C114 para cloruro y sulfato, y la C1603 para el total de sólidos.",
     ["C1603", "C114"], "C1602 es la especificación (los límites); C114 y C1603 son los métodos con que se miden.",
     [S("05", 7), S("05", 8), S("08", 3)], ""),
    ("C1603", "agua", "Medición de sólidos en agua (total de sólidos)",
     "", ["C1602", "C114"], "C1603 = sólidos en el agua.",
     [S("05", 7), S("05", 8)], ""),
    ("C114", "agua", "Análisis químico del cemento hidráulico (la tabla de límites del agua lo cita como método para cloruro y sulfato)",
     "", ["C1602", "C1603"], "C114 = análisis químico: cloruro y sulfato en la tabla.",
     [S("05", 7), S("05", 8), S("08", 3)], ""),

    ("C109", "mortero", "Esfuerzo a compresión de cubos de mortero de 50 mm; con agua no potable debe dar al menos 90 % del control a 7 días",
     "", ["C191", "C305", "C1437"], "C109 rompe los cubos (compresión); C191 mide el fraguado.",
     [S("17", 12), S("05", 9), S("08", 1)], ""),
    ("C191", "mortero", "Tiempo de fraguado del cemento hidráulico con la aguja de Vicat; con agua no potable, de 1:00 antes a 1:30 después del control",
     "", ["C109"], "C191 = Vicat, la aguja que mide cuánto tarda en fraguar.",
     [S("17", 11), S("05", 9)], ""),
    ("C305", "mortero", "Mezclado mecánico de pastas de cemento hidráulico y morteros de consistencia plástica",
     "", ["C1437", "C109"], "En el laboratorio el orden es C305 (mezclar), C1437 (flujo) y C109 (moldear y romper cubos).",
     [S("17", 12)], ""),
    ("C1437", "mortero", "Flujo de mortero de cemento hidráulico",
     "", ["C305", "C109"], "C1437 viene justo después de mezclar: se mide el flujo del mortero.",
     [S("17", 12)], ""),
]

NORMAS = []
for (i, fam, mide, detalle, confunde, gancho, fuente, verificar) in _N:
    n = {"id": i, "designacion": "ASTM " + i, "familia": fam, "mide": mide}
    if detalle:
        n["detalle"] = detalle
    n["confunde_con"] = confunde
    n["gancho"] = gancho
    n["fuente"] = fuente
    if verificar:
        n["verificar"] = verificar
    NORMAS.append(n)
