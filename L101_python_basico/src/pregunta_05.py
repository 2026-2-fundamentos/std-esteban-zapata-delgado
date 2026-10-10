import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    #Se crea el archivo donde se almacena la data y se convierte en dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Se agrupan los datos por letra y se saca su máximo y su mínimo
    letras_df = df.groupby(0)[1].agg(["max","min"])

    #Se crean las tuplas (letra,maximo,minimo)
    tuplas = [(letter,maxi,mini) for letter,maxi,mini in letras_df.itertuples()]

    return tuplas
    

if __name__ == "__main__":
    print(pregunta_05())
