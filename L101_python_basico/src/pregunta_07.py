import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    file = os.path.join(DATA_FOLDER, "data.csv.gz")
    df = pd.read_csv(file, sep="\t", header=None)

    # Nos quedamos con las primeras dos columnas
    df = df.iloc[:, :2]
    df.columns = ["letter", "value"]

    # Convertimos 'value' a entero para asegurar un ordenamiento numérico
    df["value"] = df["value"].astype(int)

    # Agrupamos conservando duplicados y el orden original mediante list
    resultado = df.groupby("value")["letter"].apply(list)

    # Convertimos la Serie agrupada a la lista de tuplas requerida
    tuplas = [(int(value), letters) for value, letters in resultado.items()]

    return tuplas
