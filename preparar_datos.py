# Preparación de datos: PISA 2025, estudiantes y escuelas de Argentina.
# Lee los archivos SPSS (.sav) de la OCDE, se queda con Argentina y las
# variables elegidas, y guarda dos CSV livianos en data/.
# Se ejecuta una sola vez: python preparar_datos.py

import pandas as pd
import pyreadstat

ARCHIVO_ESTUDIANTES = "data/raw/CY09_MS_STU_PUF.sav"
ARCHIVO_ESCUELAS = "data/raw/CY09_MS_SCH_PUF.sav"

# Variables de estudiantes (nombres verificados en PISA2025_Codebook.xlsx)
vars_estudiantes = (
    ["CNT", "CNTSCHID", "CNTSTUID", "MALE", "REPEAT", "ESCS"]
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

# El archivo de estudiantes pesa más de 2 GB: se lee en pedazos de 100.000 filas
# y de cada pedazo se guardan solo las filas de Argentina.
pedazos = []
for pedazo, meta in pyreadstat.read_file_in_chunks(
    pyreadstat.read_sav, ARCHIVO_ESTUDIANTES, chunksize=100000, usecols=vars_estudiantes
):
    pedazos.append(pedazo[pedazo["CNT"] == "ARG"])

estudiantes = pd.concat(pedazos)
print("Estudiantes de Argentina:", estudiantes.shape)

# El archivo de escuelas es chico y se lee entero
escuelas, meta = pyreadstat.read_sav(ARCHIVO_ESCUELAS, usecols=vars_escuelas)
escuelas = escuelas[escuelas["CNT"] == "ARG"]
print("Escuelas de Argentina:", escuelas.shape)

# Los códigos de "sin respuesta" de SPSS (95 a 99, 9997) ya llegan como valores vacíos.
estudiantes.to_csv("data/pisa2025_arg_estudiantes.csv", index=False)
escuelas.to_csv("data/pisa2025_arg_escuelas.csv", index=False)
print("CSV guardados en data/")
