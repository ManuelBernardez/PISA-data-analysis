# Preparación de datos: PISA 2025, estudiantes y escuelas de Argentina.
# Lee los archivos SPSS (.sav) de la OCDE, se queda con Argentina y las
# variables elegidas, y guarda tres CSV livianos en data/:
#   - pisa2025_arg_estudiantes.csv: una fila por estudiante
#   - pisa2025_arg_escuelas.csv: una fila por escuela
#   - pisa2025_arg_codigos_faltantes.csv: tipos de faltante por pregunta
# Se ejecuta una sola vez: python preparar_datos.py

import pandas as pd
import pyreadstat

ARCHIVO_ESTUDIANTES = "data/raw/CY09_MS_STU_PUF.sav"
ARCHIVO_ESCUELAS = "data/raw/CY09_MS_SCH_PUF.sav"

# Variables de estudiantes (nombres verificados en PISA2025_Codebook.xlsx)
vars_estudiantes = (
    ["CNT", "CNTSCHID", "CNTSTUID", "MALE", "REPEAT", "ESCS", "W_FSTUWT"]
    # 10 valores plausibles por materia (el análisis usa PV1; el resto, para chequear)
    + [f"PV{i}{materia}" for materia in ["MATH", "READ", "SCIE"] for i in range(1, 11)]
    # Clima en las clases de ciencias y distracción con dispositivos
    + ["ST097Q01TA", "ST097Q02TA", "ST097Q03TA", "ST097Q04TA", "ST097Q05TA", "ST097Q06DA", "DISCLISCI"]
    # Pantallas y celular
    + ["ST326Q04JA", "ST326Q05JA", "ST326Q06JA", "IC177Q02JA", "ST322Q06JA", "ST250Q04JA"]
    # Inteligencia artificial
    + ["ST438Q01DA", "ST438Q02DA", "ST438Q03DA", "ST438Q04DA", "AIUSESCH", "IC170Q10DA"]
)

vars_escuelas = ["CNT", "CNTSCHID", "PRIVATESCH", "SC001Q01TA", "SC190Q02JA"]

# Preguntas para la tabla de tipos de faltante, en el orden del cuestionario.
# La página es la del PDF "STUDENT QUESTIONNAIRE PISA 2025". Las preguntas IC
# pertenecen al cuestionario TIC, que es aparte y no figura en ese PDF.
preguntas_faltantes = [
    ("ST250Q04JA", "principal", 8),
    ("REPEAT", "principal", 27),  # derivada de la pregunta ST127
    ("ST097Q01TA", "principal", 34),
    ("ST097Q06DA", "principal", 34),
    ("ST326Q05JA", "principal", 56),
    ("ST438Q04DA", "principal", 61),
    ("ST322Q06JA", "principal", 62),
    ("IC170Q10DA", "TIC", None),
    ("IC177Q02JA", "TIC", None),
]

# --- Lectura 1: valores válidos -------------------------------------------
# El archivo de estudiantes pesa más de 2 GB: se lee en pedazos de 100.000 filas
# y de cada pedazo se guardan solo las filas de Argentina. pyreadstat convierte
# todos los códigos de faltante de SPSS (5 a 9, 95 a 99, 9997) en valores vacíos.
pedazos = []
for pedazo, meta in pyreadstat.read_file_in_chunks(
    pyreadstat.read_sav, ARCHIVO_ESTUDIANTES, chunksize=100000, usecols=vars_estudiantes
):
    pedazos.append(pedazo[pedazo["CNT"] == "ARG"])
estudiantes = pd.concat(pedazos)
print("Estudiantes de Argentina:", estudiantes.shape)

# --- Lectura 2: códigos de faltante ---------------------------------------
# Con user_missing=True los códigos de faltante se conservan como números,
# así se puede distinguir "no administrado" de "sin respuesta".
columnas_codigos = ["CNT", "CNTSTUID"] + [p[0] for p in preguntas_faltantes]
pedazos = []
for pedazo, meta in pyreadstat.read_file_in_chunks(
    pyreadstat.read_sav, ARCHIVO_ESTUDIANTES, chunksize=100000,
    usecols=columnas_codigos, user_missing=True
):
    pedazos.append(pedazo[pedazo["CNT"] == "ARG"])
codigos = pd.concat(pedazos)

# Las dos lecturas recorren el archivo en el mismo orden: se verifica antes de copiar
assert (estudiantes["CNTSTUID"].values == codigos["CNTSTUID"].values).all()

# Código 7 = "no administrado". Los mismos estudiantes lo tienen en todas las
# preguntas del cuestionario principal, así que se toma ST097Q06DA como referencia.
estudiantes["cuestionario_administrado"] = (codigos["ST097Q06DA"] != 7).astype(int).values

# El cuestionario TIC es aparte: código 97 en sus preguntas = no administrado
estudiantes["cuestionario_tic_administrado"] = (codigos["IC170Q10DA"] != 97).astype(int).values

# Valor original de IC170Q10DA, con los códigos 6 (no disponible), 96, 97 y 99,
# para poder desglosar los vacíos de esa pregunta en el notebook
estudiantes["ia_escuela_codigo_original"] = codigos["IC170Q10DA"].values

# Tabla resumen: las preguntas de 1 dígito usan los códigos 6, 7 y 9;
# las de 2 dígitos, 96, 97 y 99 (según meta.missing_ranges).
filas = []
for columna, cuestionario, pagina in preguntas_faltantes:
    base = 0 if meta.missing_ranges[columna][0]["lo"] == 5 else 90
    filas.append({
        "variable": columna,
        "cuestionario": cuestionario,
        "pagina_cuestionario": pagina,
        "no_administrado": (codigos[columna] == base + 7).sum(),
        "sin_respuesta": (codigos[columna] == base + 9).sum(),
        "perdido_sistema": (codigos[columna] == base + 6).sum(),
    })
tabla_faltantes = pd.DataFrame(filas)
print(tabla_faltantes)

# --- Escuelas ----------------------------------------------------------------
# El archivo de escuelas es chico y se lee entero
escuelas, meta = pyreadstat.read_sav(ARCHIVO_ESCUELAS, usecols=vars_escuelas)
escuelas = escuelas[escuelas["CNT"] == "ARG"]
print("Escuelas de Argentina:", escuelas.shape)

estudiantes.to_csv("data/pisa2025_arg_estudiantes.csv", index=False)
escuelas.to_csv("data/pisa2025_arg_escuelas.csv", index=False)
tabla_faltantes.to_csv("data/pisa2025_arg_codigos_faltantes.csv", index=False)

# --- Comparación con otros países (sección 4.8 del notebook) ----------------
# Solo las variables que se comparan; nada del cuestionario TIC, que Chile y
# Brasil no aplicaron.
paises_comparacion = ["ARG", "CHL", "BRA", "ESP", "JPN"]
vars_comparacion = (
    ["CNT", "CNTSCHID", "ESCS", "ST097Q06DA",
     "ST438Q01DA", "ST438Q02DA", "ST438Q03DA", "ST438Q04DA", "W_FSTUWT"]
    + [f"PV{i}{materia}" for materia in ["MATH", "READ", "SCIE"] for i in [1, 5]]
)
pedazos = []
for pedazo, meta in pyreadstat.read_file_in_chunks(
    pyreadstat.read_sav, ARCHIVO_ESTUDIANTES, chunksize=100000, usecols=vars_comparacion
):
    pedazos.append(pedazo[pedazo["CNT"].isin(paises_comparacion)])
comparacion = pd.concat(pedazos)
print("Comparación entre países:", comparacion.shape)
print(comparacion["CNT"].value_counts())
comparacion.to_csv("data/comparacion_paises_pisa2025.csv", index=False)

print("CSV guardados en data/")
