# Auditoría técnica del contenido — 9 de octubre de 2026

**Alcance:** las 147 tarjetas, 183 preguntas y 60 términos del glosario (temas 1, 2 y 3). Cuatro agentes con perfil de ingeniero de materiales y normativa ASTM/ACI revisaron cada ítem contra la página que cita, en las fuentes del curso. Después se verificó cada hallazgo: las citas con texto se comprobaron automáticamente y las que están en tablas, diapositivas o exámenes escaneados se revisaron a ojo.

**Reglas:** solo se cambia lo que respaldan las fuentes del curso. Si algo parece dudoso pero las fuentes no lo resuelven, se marca «⚠ Verificar» para consultarlo con el profe. Se respetaron las decisiones C1–C21 de ALCANCE.md. No se tocaron los enunciados copiados de exámenes ni la estructura de los ítems: no se agregó, borró ni reordenó nada, así que el progreso guardado sigue valiendo.

## Resultado

- **79 correcciones en 68 ítems:** 5 de severidad alta (en 2 ítems), 22 media y 52 baja.
- **8 ítems nuevos con «⚠ Verificar»:** ahora son 41 (15 tarjetas y 26 preguntas).
- **2 contradicciones nuevas en ALCANCE.md §7:** C22 y C23.
- **Una clave cambiada:** p3-3C-x17 pasa de Falso a Verdadero.
- Las correcciones están en `tools/contenido/correcciones.json`. Cada una guarda el texto anterior, la razón y la evidencia (documento, página y cita), y `construir.py` las aplica al regenerar `data/`.

## Lo más importante (severidad alta)

1. **Contracción autógena (p2-2B-x11).** La respuesta modelo decía que se evita «reduciendo la a/c».
   - En la clave del examen II-2022 (X04), «reducir a/c» está en la columna de la contracción **plástica**.
   - Para la autógena, la clave da vibración y curado.
   - Además, Navas indica que la autógena es significativa justamente con a/c muy bajas.
   - Se corrigieron la respuesta modelo y la explicación.
2. **Agua de diseño contra agua de dosificación (p3-3C-x17).** La explicación se contradecía: decía «Falso» y a la vez que el agua dosificada es menor que la de diseño, lo que hace verdadera la afirmación.
   - En el cuestionario (X01, pág. 6) la equis impresa está en F, pero la corrección al margen marca V, y la justificación impresa respalda el V.
   - Se adoptó **Verdadero**, con «⚠ Verificar» y la contradicción C23.

## Cambios de severidad media, por tema

- **Agua:**
  - Se agregó la fila «cloruro de calcio: 2 % del peso del cemento» de la tabla de tolerancias, que faltaba en todo el contenido.
  - Se precisó que la C114 es el análisis químico del cemento hidráulico.
  - Se aceptó «sodio» como segunda respuesta válida para la sal que acelera o retarda el fraguado (la clave de X04 la da).
  - Se quitó de una explicación un dato sobre la ASTM C305 que no está en ninguna fuente.
  - Se agregó la marca de la contradicción C18 (curado pronto) a la tarjeta de la contracción autógena.
- **Agregados, clasificación y rocas:**
  - El límite entre agregados normales y pesados es 1 900 kg/m³ en la diapositiva y 1 920 kg/m³ en el manual: se marcó «⚠ Verificar» (C22).
  - Se aclaró que la condición de la reacción álcali-sílice es **superar** el 0,6 % de álcalis.
  - El tema de ensayos RAS se marcó INCOMPLETO (faltan las págs. impresas 123–125 de la PCA).
  - Se marcó para consultar la ASTM C994, que podría ser la C944.
- **Volúmenes y masas:**
  - El Vv de las fórmulas de porosidad y razón de vacíos incluye los poros permeables (diagrama 13: 4). No es solo el espacio entre partículas de la ASTM C29. Se aclaró en la tarjeta y en el glosario.
  - La GBS sí lleva especificación en el registro de control de calidad del profe (2,50 mínimo).
  - Se corrigió la fuente de la tarjeta del volumen del saco de cemento.
- **Granulometría:**
  - Una arena con MF 2,2 es «fina», no «muy fina», según la tabla del curso.
  - La pregunta de tamaño máximo en losas ahora pide la regla propia de las losas (1/3 del espesor), porque la regla de 1/5 también daba una respuesta defendible.
  - Se corrigió la explicación del distractor «mezcladoras más eficientes».
- **Ensayos de laboratorio:**
  - El manual da dos órdenes distintos de pesada en la C127: se marcó «⚠ Verificar».
  - Se quitó el símbolo δBS del límite de agregados livianos, porque en el curso δBS es la densidad de las partículas.
  - Se reemplazó una afirmación sin respaldo sobre el cuarteo («la arena húmeda conserva la forma del cono») por el requisito de flujo libre del separador.

## Cambios de severidad baja

Son precisiones de redacción y de fuentes:
- espacio de miles y coma decimal;
- «al menos 2 m», «al menos 4 kg», «± 10 g»;
- la regla de redondeo de la C117;
- la precisión del reporte en la C128;
- explicaciones de distractores que no decían por qué eran falsos;
- páginas de fuente que faltaban (ACI 116R, PCA y manual).

## No aplicado (decisiones de Adrián)

- **Escoria de alto horno:** la diapositiva dice «subproducto del acero» y el ACI 116R la asocia al hierro. Se mantiene la diapositiva del profe (regla §0.2).
- **p3-3D-x11:** el enunciado no es copia completa del examen 2009 (X14); omite la ubicación, el cemento y la dosificación 1:3:3,5. ¿Se completa o se deja el recorte?
- **t3-3D-12:** lista los métodos para corregir la granulometría (masa retenida, factor, fórmula, combinación). ALCANCE §5 excluye el factor k. ¿Se queda la tarjeta?

## Anexo: las 79 correcciones

| Ítem | Campo | Severidad | Razón | Evidencia (doc: pág.) |
|---|---|---|---|---|
| p2-2B-x11 | respuesta modelo | alta | En la clave de X04, «Reducir a/c» está en la columna de la contracción PLÁSTICA; para la autógena solo aparecen «Vibración» y «Curado». Además, reducir la a/c no evita la contracción autógena: según Navas, se vuelve… | X04: 1; 20: 2 |
| p2-2B-x11 | explicación | alta | La explicación atribuye a la clave una respuesta («reducir la a/c») que la clave pone en la columna de la contracción plástica, y que contradice a Navas para la autógena. | X04: 1; 20: 2 |
| p3-3C-x17 | explicación | alta | La explicación actual se contradice: dice que el agua dosificada es menor, que es lo mismo que decir que el agua de diseño es mayor, y eso vuelve verdadera la afirmación del enunciado. Este texto se aplica junto con el cambio… | X01: 6; X06: 3 |
| p3-3C-x17 | nota «verificar» | alta | Mientras se confirma la clave, el ítem debe llevar la marca VERIFICAR para que el estudiante no memorice una respuesta dudosa. | X01: 6 |
| p3-3C-x17 | respuesta correcta | alta | La justificación impresa de la clave («es menor porque los agregados aportan el resto») y la corrección al margen («V») hacen verdadera la afirmación; la equis impresa en F la contradice. Se adopta V con VERIFICAR. | X01: 6 |
| g-porosidad-n | definición | media | El glosario define «Vacíos» solo como espacio entre partículas (sentido de la ASTM C29). Sin la aclaración, la porosidad queda mal calculada, porque el Vv del formulario también incluye los poros permeables. | 24: 12; 13: 4 |
| g-razon-de-vacios-e | definición | media | Es la misma ambigüedad sobre Vv: con la definición de «Vacíos» del glosario, e daría un valor menor que el del formulario. | 24: 12; 13: 10 |
| p2-2A-x09 | respuesta modelo | media | La clave del examen marca dos respuestas válidas (bicarbonatos y sodio); la respuesta modelo y los puntos clave solo dan una, y el autocalificado rechazaría «sodio». | X04: 1; 05: 3 |
| p2-2A-x09 | puntos clave | media | Mismo motivo: la clave acepta también «sodio» (bicarbonato de sodio, NaHCO₃, en la diapositiva). | X04: 1 |
| p2-2B-x06 | explicación | media | El dato sobre el contenido de la ASTM C305 no aparece en ninguna fuente del curso (regla «nada inventado»); la explicación se sostiene sin él. | 06: 8; X02: 2 |
| p3-3B-x10 | fuente | media | La explicación (capa de limo y arcilla que debilita la adherencia y aumenta la demanda de agua) está en la pág. impresa 119 (PDF 1), que es la que cita la propia clave («Pag 119»). La pág. 120 solo tiene la Tabla 5-7. | 10: 1 |
| p3-3D-t04 | enunciado | media | Las fuentes enuncian «un quinto de la dimensión más pequeña del miembro» sin excluir las losas. En una losa, la dimensión menor es el espesor, así que una lectura literal da 24 mm (la opción A) y también sería defendible. El… | 11: 7; 16: 5 |
| p3-3D-t04 | explicación | media | Hay que ajustar la explicación al enunciado corregido. La actual da a entender que la regla de un quinto no aplica a una losa, y las fuentes no lo dicen. | 11: 7 |
| p3-3D-x01 | explicación | media | La explicación misma cita el «mezclado más fuerte o más largo» y luego dice que la D no aparece en las fuentes, lo que se contradice. Hay que explicar por qué la D no es la respuesta. | 20: 3; 20: 3; X02: 1 |
| p3-3D-x11 | explicación | media | Según la tabla 22, un MF de 2,2 es arena «fina», no «muy fina» (< 2,0). Conviene además señalar que 2,2 queda fuera del rango aceptable de 2,3–3,1. | 22: 1; 16: 6 |
| t2-2A-11 | reverso | media | ALCANCE 2.7 pide la tabla completa de tolerancias; la fila del cloruro de calcio (2 %) no aparece en ninguna tarjeta, pregunta ni glosario del proyecto. Encaja en la tarjeta de cloruros. | 25: 1 |
| t2-2B-07 | nota «verificar» | media | ALCANCE §7 C18 manda marcar VERIFICAR y mostrar las dos atribuciones; la tarjeta afirma la de Navas sin la marca, a diferencia de p2-2B-x28. | 20: 2; X01: 8 |
| t3-3A-06 | nota «verificar» | media | La C19 manda llevar VERIFICAR en el rango de GBS y la tarjeta no lo lleva. Además hay una contradicción nueva entre dos fuentes del profe (1 900 contra 1 920 kg/m³) que no está en ALCANCE §7; por la regla 0.3 se muestran las… | 14: 9; 19: 63 |
| t3-3A-14 | nota «verificar» | media | Por conocimiento general, el método de corte rotativo para superficies de concreto o mortero es la ASTM C944, no la C994; la diapositiva parece tener los dígitos invertidos. Ninguna fuente del curso dice C944, así que no se… | 15: 11 |
| t3-3B-14 | reverso | media | Tal como está, «exceso de álcalis (máximo 0,6 %)» puede leerse como que el exceso no pasa de 0,6 %. El 0,6 % es el máximo permitido; la condición de la reacción es superarlo. | 15: 13; X06: 3; 10: 5 |
| t3-3B-16 | nota «verificar» | media | ALCANCE §0.4 y 3.14 piden marcar INCOMPLETO el tema de RAS (ensayos y control). Ningún ítem del lote (ni del proyecto) lleva esa marca; esta tarjeta de ensayos es la más afectada. Lo mismo podría anotarse en p3-3B-t06 y t3-3B-17. | 10: 4; 15: 17 |
| t3-3C-17 | reverso | media | En el formulario y en el diagrama del curso, Vv incluye los poros permeables además del espacio entre partículas (por eso Vm = Vs(1 + e)). Si no se aclara, el estudiante lo confunde con los «vacíos» de la ASTM C29, que… | 13: 4; 13: 10; 24: 12 |
| t3-3C-20 | reverso | media | La frase tajante choca con la diapositiva del profe (13, pág. 8), que pone a la GBS como criterio de aceptación, y con la clave de X01 (F/V 15). También omite el matiz de la propia PCA. | 02: 2; 13: 8; X01: 6 |
| t3-3C-21 | fuente | media | La pregunta 6 de X06 trata de las partículas planas y alargadas; el 0,035 m³ está en X01, pág. 6 (F/V 12). | X01: 6 |
| t3-3E-17 | nota «verificar» | media | La tarjeta sigue el orden de la pág. 70, pero el mismo manual (págs. 74 y 75) da el orden inverso, que además es el de la norma ASTM C127. Son dos indicaciones del profe que chocan: hay que marcarlo VERIFICAR (regla 3 de… | 19: 70; 19: 74; 19: 75 |
| t3-3E-19 | reverso | media | En el curso, δBS es la densidad bruta seca de las partículas (Ps/VB, 19: 64); un δBS de 1 120 kg/m³ equivaldría a GBS ≈ 1,12. El umbral de los livianos se refiere a la densidad bruta o peso unitario masivo (14: 11), así que el… | 19: 67; 19: 66; 14: 11 |
| t3-3E-37 | reverso | media | Que la arena húmeda «conserva la forma del cono» en el cuarteo no aparece en ninguna fuente (regla «nada inventado»); el respaldo documental de la razón es el requisito de flujo libre del separador (págs. 25 y 28). Ver el… | 19: 25; 19: 28; 19: 27 |
| g-agregado | fuente | baja | La parte «que se usa con un medio cementante para hacer concreto o mortero» no está en 19, pág. 6; viene del ACI 116R (12, págs. 2–3). | 19: 6; 12: 3 |
| g-agregado-liviano | definición | baja | Regla 7 (espacio de miles). | 14: 9 |
| g-agregado-pesado | definición | baja | Regla 7 (espacio de miles). Ver además la diferencia 1 900 / 1 920 kg/m³ anotada en t3-3A-06. | 14: 9 |
| g-agua-de-mezcla | definición | baja | Omite la condición de la PCA (sin fuerte sabor u olor), que sí recoge la tarjeta t2-2A-01. | 01: 1 |
| g-asentamiento | fuente | baja | La diapositiva 06: 9 solo lista las normas; «medida de la consistencia» viene del ACI 116R, pág. 60. | 12: 60 |
| g-eflorescencia | fuente | baja | Ni 05: 5 ni la PCA definen eflorescencia como «depósito de sales en la superficie»; la definición está en el ACI 116R, pág. 25. | 12: 25 |
| g-modulo-de-finura-mf | definición | baja | Misma precisión que en la tarjeta t3-3D-08: la serie de seis mallas es la del agregado fino. | 19: 48 |
| g-modulo-de-finura-mf | fuente | baja | La serie de mallas del MF para el agregado grueso viene de la PCA (Tabla y texto de la pág. impresa 109). | 11: 4 |
| g-ppm | fuente | baja | La tabla 25 usa «ppm» sin explicarlo; la expansión «partes por millón» está en la PCA, pág. impresa 97. | 01: 3 |
| g-tasa-de-evaporacion | definición | baja | Es una tasa (por área y por hora), no una cantidad; el eje del ábaco de la diapositiva da las unidades. | 06: 8 |
| g-vacios | definición | baja | Distingue los vacíos de la ASTM C29 del Vv de las fórmulas de porosidad y razón de vacíos. El «cerca de» sigue a la PCA. | 19: 99; 02: 2 |
| g-vibracion | fuente | baja | La diapositiva 06: 5 muestra los tipos, pero no dice que la vibración sirve para consolidar; eso está en el ACI 116R, pág. 70 (que también describe la externa «attached ... on the forms»). | 12: 70 |
| p2-2A-x13 | explicación | baja | La explicación (texto propio, no del examen) debe usar coma decimal como el resto del sitio. | X01: 3 |
| p2-2A-x17 | nota «verificar» | baja | Ninguna fuente de teoría dice que el magnesio cause más eflorescencias y expansiones que el calcio: la diapositiva los pone al mismo nivel y la clave de X04 acepta ambos. La clave de X01 solo da magnesio; conviene marcar… | 05: 5; X04: 1 |
| p2-2B-x10 | respuesta modelo | baja | La clave acepta cuatro formas de evitarla y la respuesta modelo omite «reducir a/c», que además respalda Navas. | X04: 1; 20: 3 |
| p2-2B-x14 | nota «verificar» | baja | La nota dice que ninguna fuente de teoría la explica, pero el ACI 116R (fuente 12) sí la define; conviene citarla como respaldo (y agregar 12, pág. 36, a fuente). | 12: 36 |
| p3-3A-t01 | explicación | baja | Regla 7: el enunciado de la misma pregunta escribe «2 240 kg/m³» con espacio y la explicación no. | 14: 9 |
| p3-3A-x04 | explicación | baja | Regla 7 (espacio de miles). La respuesta_modelo es copia de la clave y no se toca. | 14: 9 |
| p3-3A-x04 | puntos clave | baja | Regla 7 (espacio de miles). | 14: 9 |
| p3-3A-x11 | explicación | baja | La única fuente citada (19, pág. 112) no define la tenacidad; la definición solo está en la clave del examen. La explicación debe decir de dónde sale y usar el manual para lo que sí dice. | X01: 6; 19: 112 |
| p3-3A-x15 | explicación | baja | Regla 7 (espacio de miles) y falta la unidad en el rango. | 14: 9 |
| p3-3B-x07 | explicación | baja | La pregunta es sobre los agregados de río; la explicación actual no los menciona. La pág. 19 de la conferencia lo respalda y debería sumarse a la fuente. | 26: 19 |
| p3-3B-x08 | explicación | baja | La explicación no justifica por qué el granito es correcto. Conviene agregar 26, págs. 56 y 58 a la fuente. Nota: la PCA (10, pág. 2, Tabla 5-8) lista las andesitas entre las sustancias potencialmente reactivas álcali-sílice;… | 26: 56; 26: 58 |
| p3-3B-x09 | fuente | baja | La explicación dice que la C (mármol, cuarcita) son metamórficas; 26, pág. 9 solo nombra el mármol. La cuarcita como metamórfica está en 15, pág. 5. | 15: 5 |
| p3-3B-x16 | puntos clave | baja | Misma ambigüedad que en t3-3B-14: el 0,6 % es el máximo permitido, y la condición es superarlo. | 15: 13; X06: 3 |
| p3-3B-x17 | explicación | baja | La afirmación es sobre los finos de menos de 75 µm; la explicación mezcla sus efectos con los de las impurezas orgánicas sin decir cuál hace qué, y omite el efecto principal de los finos (adherencia). | 10: 1; 10: 1 |
| p3-3B-x17 | fuente | baja | El texto de la clave (retraso del fraguado, menor resistencia) y el efecto de los finos están en la pág. impresa 119, no en la 120. | 10: 1 |
| p3-3C-x23 | nota «verificar» | baja | ALCANCE C19 adopta 2,4–2,8 con VERIFICAR. La tarjeta t3-3C-19 y la pregunta p3-3C-x10 llevan la marca; esta pregunta, cuya respuesta es justamente el límite en disputa, no la lleva. | 19: 63; 14: 9 |
| p3-3D-x03 | explicación | baja | La explicación da a entender que en una losa sin refuerzo no hay límite. El criterio de un tercio del espesor sigue aplicando, y conviene recordarlo para no generalizar. | 11: 7; X01: 1 |
| p3-3E-t01 | explicación | baja | La opción D es «Ninguno: todos están permitidos», no un método; la explicación actual no dice por qué es falsa. | 19: 27 |
| p3-3E-t02 | explicación | baja | La explicación de la D solo la nombra y no dice por qué no invalida el ensayo. | 19: 53; 19: 27 |
| p3-3E-t05 | opción a | baja | El manual dice que la varilla no debe tocar el fondo, sin el matiz «fuerte»; así queda igual que la tarjeta t3-3E-29 y que la pág. 110. | 19: 106 |
| p3-3E-x06 | explicación | baja | Quien dice expresamente que se fija un límite máximo de pérdida es la PCA (09, impresa 118), no el manual; la explicación atribuye la frase a la fuente equivocada. | 09: 2; 19: 112 |
| t2-2A-08 | reverso | baja | La diapositiva muestra el título real de la C114 (análisis químico del cemento hidráulico); la tarjeta lo omite y puede llevar a pensar que es una norma específica de agua. | 05: 7; X02: 3 |
| t2-2A-09 | nota «verificar» | baja | El 50 000 ppm de la PCA es para agua de lavado según la C94, no para la C1602; aclararlo ayuda a entender la diferencia de C1. | 01: 2 |
| t2-2A-13 | nota «verificar» | baja | La PCA no «fija» un límite de 2,5 %: describe el efecto por encima de ese valor (así lo recoge C21). | 01: 6 |
| t3-3A-06 | reverso | baja | Regla 7 (espacio de miles); la propia diapositiva escribe «1 900» y «1 120». | 14: 9 |
| t3-3B-07 | reverso | baja | «Casi siempre» exagera el «comúnmente» de la fuente. Además, la redacción actual sugiere que todos los problemas listados producen partículas planas, cuando solo la textura fluidal (lajamiento) lo hace. | 26: 54; 26: 53 |
| t3-3B-17 | reverso | baja | La PCA limita la RAC a ciertas rocas dolomíticas (de composición específica y poco común); escrito sin «ciertas», parece que toda roca dolomítica reacciona. | 10: 5 |
| t3-3B-18 | reverso | baja | La tabla dice «puede causar» (no siempre) y además menciona erupciones y deterioro, que la tarjeta omite. La pregunta p3-3B-t05 usa «erupciones» en la opción correcta, así que conviene que la tarjeta lo traiga. | 10: 2; 10: 2 |
| t3-3C-14 | reverso | baja | El formulario define D en porcentaje (ec. 19). Si se sustituye «2» en lugar de «0,02», el resultado es absurdo, y la pregunta p3-3C-t04 usa justo ese distractor (4,60). | 13: 10 |
| t3-3D-08 | reverso | baja | El manual dice que el MF se puede calcular para el fino y para el grueso, pero que la lista de seis mallas es la del fino. Tal como está, la tarjeta presenta esa serie como general. | 19: 48; 11: 4 |
| t3-3D-08 | fuente | baja | La serie de mallas del MF para el agregado grueso viene de la PCA (Tabla y texto de la pág. impresa 109). | 11: 4 |
| t3-3E-02 | reverso | baja | El manual da 2 m como longitud mínima, no como longitud fija. | 19: 8 |
| t3-3E-11 | reverso | baja | Los valores son correctos, pero la convención del proyecto pide espacio de miles («1 000 g»). | 19: 39 |
| t3-3E-12 | reverso | baja | La tarjeta omite la regla general (entero más cercano) y solo da la excepción, lo que puede llevar a reportar siempre al 0,1 %. | 19: 42 |
| t3-3E-23 | reverso | baja | Los 4 kg son una masa mínima, no un valor fijo. | 19: 82 |
| t3-3E-24 | reverso | baja | La tarjeta de «resultado y criterio» del C128 no dice cómo se reporta, a diferencia de la del C127 (t3-3E-20); el manual da la misma precisión para ambos ensayos. | 19: 87 |
| t3-3E-29 | nota «verificar» | baja | La pág. 100, dentro del C29, también trae un texto que pertenece al C40; conviene anotarlo junto con el de la pág. 111. | 19: 100 |
| t3-3E-33 | reverso | baja | Falta el espacio de miles y la tolerancia de la masa total que da el cuadro 1.9.1. | 19: 115 |
| t3-3E-37 | fuente | baja | La pág. 27 solo da la regla de elección del método; el fundamento del «por qué» (flujo libre por los canales) está en las págs. 25 y 28. | 19: 28 |
| t3-3E-39 | fuente | baja | ALCANCE.md indica que el respaldo de la C566 está en 08 y 13: 8; la tarjeta solo cita 19: 66. Se agregan 13: 8 (registro con la C566, diapositiva del profe) y 19: 80 (el mismo texto en la sección del C128). | 19: 80; 13: 8 |
