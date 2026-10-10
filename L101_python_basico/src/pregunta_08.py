import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """
    #Se crea la variable file donde se guardan la dirección de la data y un dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Nos quedamos únicamente con las primeras dos columnas y se asignan nombres a las columnas
    df = df.iloc[:,:2]
    df.columns = ["letter","value"]
    df["value"] = df["value"].astype(str)


    #Ahora agrupamos el dataframe por los valores que toma la columna 'value'
    resultado=df.groupby(["value"])["letter"].unique()

    #Se crean las tuplas
    tuplas = [(int(value),list(sorted(array))) for value,array in resultado.items()]

    return tuplas 


