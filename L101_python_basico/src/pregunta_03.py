import pandas as pd
import os.path
import glob
import shutil
import numpy as np

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")

def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    #Se lee el archivo data y se carga el dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")

    df = pd.read_csv(file,sep="\t",header=None)

    #Se crea un Dataframe agrupado por la columna letras y se calcula la suma sobre la segunda columna ('value)
    df_letras = df.groupby(0)[1].sum()

    #Se crea la lista donde se almacenas las tuplas
    tuplas = [(letra, int(suma)) for letra, suma in df_letras.items()]

    return tuplas


