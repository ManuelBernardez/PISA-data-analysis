# Proyecto: Data Challenge (Introducción al Análisis de Datos, UTN)

Trabajo individual final. Se entrega como notebook de Jupyter y se presenta oralmente el 26/11/2026 (5 minutos, con apoyo visual). Entorno: Windows 10, PowerShell, Python 3.13, VS Code.

## Consigna
- Dataset real con >= 3.000 registros y >= 4 columnas relevantes.
- Notebook ejecutable sin errores, con pandas, matplotlib y/o seaborn.
- Debe girar alrededor de 1 o 2 preguntas guía respondibles con filtrado, transformación, cálculo o visualización.
- Estructura obligatoria del notebook:
  1. Introducción (dataset, fuente y contexto, pregunta guía)
  2. Exploración inicial
  3. Limpieza (faltantes, duplicados, formatos y tipos)
  4. Transformaciones (columnas derivadas, filtrados, uniones, normalización o categorización)
  5. Visualización (gráficos descriptivos y comparativos, con breve análisis)
  6. Conclusiones (respuesta a la pregunta guía, reflexión y limitaciones)
- Conceptos que tienen que aparecer: .head(), .info(), .describe(), .dropna(), .fillna(), .duplicated(), .drop_duplicates(), .rename(), .sort_values(), .apply(), .loc[], .iloc[], .plot(), plt.bar(), plt.pie(), plt.scatter().
- Buenas prácticas: celdas Markdown explicativas, comentarios útiles, celdas ordenadas, sin código sin uso, gráficos con título, etiquetas y leyenda claros.
- El notebook también tiene que poder correr en Google Colab (celda simple y comentada para subir el archivo).

## Materiales de la cursada: única fuente de técnicas
- Están en `materiales/` (presentaciones .pptx y notebooks .ipynb). No modificar, mover ni borrar nada. Esa carpeta va en el .gitignore.
- Usar SOLO técnicas, librerías, funciones y gráficos vistos ahí. Nada de estadística avanzada ni machine learning.
- Si hace falta (o es muy útil) algo que no se vio: decir qué es, por qué hace falta y qué alternativa hay dentro de lo visto, y esperar mi OK.
- Excepciones permitidas, avisando y justificando: herramientas solo para preparar el entorno o leer archivos (por ejemplo pyreadstat para abrir .sav). python-pptx solo de forma temporal, sin agregarlo a requirements.txt.
- Mantener en este archivo un resumen de lo que se vio en clase (temas, librerías, funciones, gráficos y estilo de los notebooks).

### Resumen de lo visto en clase (relevado el 12/11/2026)
- Temas: Python básico (tipos, colecciones, funciones, lambda, comprehensions); NumPy básico; pandas (carga, exploración, nulos, conversiones, selección, columnas derivadas, regex con `.str`, agrupaciones); EDA (tendencia central, dispersión, outliers por IQR, correlación Pearson/Spearman, correlación ≠ causalidad); visualización con matplotlib y seaborn.
- Pandas en código de clase: read_csv, to_csv, head, tail, sample, shape, dtypes, info, describe, columns, value_counts(normalize=True), unique, nunique, isnull/isna/notna, fillna, dropna(subset=), drop(columns=), drop_duplicates, replace, astype, to_numeric(errors='coerce'), loc, iloc, filtros booleanos, isin, apply(lambda) y apply(axis=1), map(dict), assign, join, rank, nlargest, idxmax, sort_values, reset_index, round, groupby + agg/mean/median/sum/size/count/transform/filter, unstack, crosstab(normalize=), pd.cut(bins, labels), corr(numeric_only=True), np.select.
- Solo en diapositivas o Markdown (no en código): rename, to_datetime, pivot_table, iloc de filas. No aparecen: merge, concat, pd.qcut, np.where, plt.subplots, plt.hist, plt.boxplot, savefig, sns.countplot, sns.regplot, google.colab.
- Gráficos (Clase Final): `plt.style.use('seaborn-v0_8')` y `sns.set_palette('muted')` al inicio; cada gráfico con `plt.figure(figsize=...)`, `plt.title`, `plt.xlabel`, `plt.ylabel` en español y `plt.show()`. Tipos: sns.barplot, Series.plot(kind='pie', autopct='%1.1f%%') con "Otras", sns.lineplot(marker='o'), sns.scatterplot(alpha=0.6), sns.boxplot, sns.histplot, sns.heatmap(annot=True, cmap='coolwarm', fmt='.2f'). Criterios: ordenar categorías por valor, torta con pocas categorías, alpha si hay superposición.
- Estilo de los notebooks: secciones numeradas en Markdown, tablas Markdown para explicar, interpretación en prosa después del código, comentarios cortos en español que explican el porqué.
- Excepciones aprobadas para este proyecto: `plt.savefig` (gráficos en `img/`) y celda comentada de Colab con `files.upload()`. `merge` se reemplaza por `set_index` + `join`; `pd.qcut` por `pd.cut` con los cuartiles de `describe()`.
- Entorno: pandas 3.x (no usar `inplace=True` sobre una columna seleccionada; asignar el resultado: `df["col"] = df["col"].fillna(...)`).

## Dataset: PISA 2025 (OCDE), estudiantes de Argentina
- Plan B: PISA 2022, misma estructura.
- Página donde encontrar los archivos PUF del PISA 2025: https://webfs.oecd.org/pisa2022/index.html
- Archivos descargados en `data/raw/` (estudiantes y escuelas, formato SPSS .sav). Documentación en `data/raw/documentacion/`: `CY08MSP_PISA2025_CODEBOOK.xlsx`, `STUDENT QUESTIONNAIRE PISA 2025.pdf`, `SCHOOL QUESTIONNAIRE PISA 2025.pdf`.
- Atención: ese codebook es en realidad el de PISA 2022 (hojas `CY08MSP_*`); los datos son 2025 (`CY09_MS_*_PUF`). Fuente de verdad para nombres y etiquetas 2025: metadatos del `.sav` (pyreadstat, `metadataonly=True`) y el cuestionario 2025. El codebook 2022 sirve solo de referencia.
- El zip de estudiantes usa compresión Deflate64: se descomprime con el Explorador de Windows o 7-Zip, no con Python.
- Clave de unión confirmada en escuelas 2025: `CNT` + `CNTSCHID`.
- Preguntas guía elegidas: A (factores del entorno de aprendizaje y brechas de desempeño) + C (uso de chatbots de IA y desempeño). Si ST438 tiene demasiados faltantes en Argentina, C se reemplaza por B (brecha por distracción dentro de un mismo nivel socioeconómico).
- Fuente: https://www.oecd.org/en/data/datasets/pisa-2025-database.html
- Es una edición muy reciente: NO confiar en la memoria para nombres de variables. Leer siempre el codebook y los cuestionarios. Verificar que una variable exista antes de usarla (por ejemplo uso de IA o puntajes de aprendizaje digital).
- Antes de filtrar, mostrar una tabla de variables propuestas (código, significado, escala) y esperar mi OK.
- Los archivos son pesados: leerlos en pedazos con pyreadstat, filtrar Argentina, guardar un CSV liviano en `data/`. El notebook trabaja solo con ese CSV. El script de preparación es `preparar_datos.py`. `data/raw/` va en el .gitignore.
- Puntajes: usar un valor plausible (o el promedio) y declarar la simplificación y la ausencia de pesos y réplicas en las limitaciones.
- Uniones: estudiantes y escuelas por código de país e ID de escuela (confirmar los nombres de las variables en el codebook).

## Enfoque
- Población: estudiantes de 15 años. Las conclusiones valen solo para ellos; dejarlo escrito en las limitaciones.
- Interés: qué factores perjudican más el aprendizaje (distracción por dispositivos, uso de pantallas, clima de clase, nivel socioeconómico) y cómo se relacionan con el desempeño en Matemática, Lectura y Ciencias.
- Las conclusiones se vinculan con MaestrIA (asistente de IA para diseño, corrección y feedback de evaluaciones escritas, donde el docente revisa y decide). Hablar de asociaciones, nunca de causas.
- Alcance acotado: 1 o 2 preguntas guía. Proponer 2 o 3 candidatas con razonamiento y esperar mi elección.

## Estilo de redacción
Todo el texto (Markdown del notebook, README, conclusiones, guion) en español de Argentina, formal y académico, pero natural y cercano, como lo escribiría un estudiante que entiende lo que hizo. Moderado: ni informal ni exageradamente "argentinizado".
- Vocabulario de Argentina (computadora, celular, estudiantes, escuela secundaria). Sin lunfardo ni coloquialismos (che, re, laburo, pibes). Sin formas de España (ordenador, móvil, vosotros).
- Impersonal o primera persona para decisiones propias ("se observa que...", "opté por eliminar..."). Sin voseo en el texto académico. En el texto, decimal con coma y miles con punto (3,5 y 11.093).
- Frases de largo variado, concretas y con datos. Explicar qué se hizo y por qué, con los números del análisis.
- Evitar el tono genérico de IA: arranques como "En el mundo actual" o "En la era digital"; muletillas como "cabe destacar", "es fundamental", "es importante tener en cuenta"; adjetivos grandilocuentes (crucial, multifacético, panorama, paradigma); la estructura "no solo... sino también"; enumeraciones siempre de a tres; abuso de guiones largos, negritas y viñetas; resúmenes que repiten lo anterior al final de cada sección.
- Precisar las limitaciones (qué falta, qué se simplificó). No inventar pasos del proceso que no ocurrieron.

## Código
- Simple y legible, como lo escribiría un estudiante que entiende lo que hace. Sin abstracciones, clases ni funciones innecesarias.
- Comentarios cortos, en español, solo donde aporten. Las explicaciones van en celdas Markdown.
- Rutas relativas (`data/archivo.csv`).

## Estructura del proyecto
Notebook en la raíz; carpetas `data/`, `data/raw/`, `img/` (gráficos), `presentacion/`, `materiales/`. Además `.venv`, `requirements.txt`, `.gitignore` y `README.md` corto (descripción, pregunta guía, instalación, ejecución).

## Forma de trabajo
- Una sección del notebook por vez, mostrándome cada una antes de seguir.
- Pedir confirmación antes de instalar algo fuera de requirements.txt o de salirse de lo visto en clase.
- Cierre: reiniciar el kernel y ejecutar todo (`jupyter nbconvert --execute`); revisar que cada gráfico tenga título, etiquetas y leyenda, que no quede código sin usar y que todo lo usado esté en `materiales/` (salvo excepciones acordadas); dejar guardadas las salidas.
- Entrega final: guion de presentación oral de 5 minutos, en lenguaje simple y natural, con 3 o 4 gráficos clave.