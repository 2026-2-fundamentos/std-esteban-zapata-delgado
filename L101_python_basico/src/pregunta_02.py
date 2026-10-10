import pandas as pd
import os.path
import glob
import shutil
import numpy as np

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    #Se lee el archivo data.csv.gz y se carga en un DataFrame de pandas
    file_path = os.path.join(DATA_FOLDER, "data.csv.gz")
    df = pd.read_csv(file_path, sep="\t", header=None)

    #Se cuenta la cantidad de registros por letra en la primera columna
    letter_counts = df[0].value_counts().sort_index()

    #Se crea una lista de tuplas (letra, cantidad) a partir del conteo de registros
    tuplas=[]
    for letter, count in letter_counts.items():
        tuplas.append((letter, count))

    return tuplas


