# Data Challenge: PISA 2025 en Argentina

Trabajo final individual de Introducción al Análisis de Datos (Tecnicatura Universitaria en Programación, UTN-FRH). Analiza las respuestas de los estudiantes argentinos de 15 años que participaron de PISA 2025 (OCDE) para estudiar qué factores del entorno de aprendizaje se asocian con su desempeño en Matemática, Lectura y Ciencias.

## Preguntas guía
1. ¿Qué factores del entorno de aprendizaje (distracción por dispositivos en clase, tiempo de pantallas por ocio, clima disciplinario y nivel socioeconómico) se asocian con mayores diferencias de desempeño en Matemática, Lectura y Ciencias?
2. ¿Cómo usan los estudiantes los chatbots de inteligencia artificial para la escuela y cómo se relaciona ese uso con su desempeño?

Los resultados describen asociaciones, no causas.

## Fuente
OCDE, PISA 2025 Database (archivos públicos de estudiantes y escuelas): https://www.oecd.org/en/data/datasets/pisa-2025-database.html

## Instalación (Windows, Python 3.13)
```
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución
1. Abrir `data_challenge_pisa_argentina.ipynb` en VS Code o Jupyter y ejecutar todas las celdas. El notebook usa solo el CSV de `data/`.
2. En Google Colab: subir el notebook y ejecutar la celda de carga, que permite subir el CSV.
3. Para regenerar el CSV desde los archivos originales de PISA (no incluidos en el repositorio): descomprimir los archivos `.sav` en `data/raw/` y ejecutar `python preparar_datos.py`.
