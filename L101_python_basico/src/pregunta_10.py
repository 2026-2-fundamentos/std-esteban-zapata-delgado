import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    #Se crea la variable file donde se guardan la dirección de la data y un dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Nos quedamos con las columnas 1,4 y 5
    df = df.iloc[:,[0,3,4]]

    #Se asignan nombres a las columnas
    df.columns = ["letter","codes","metrics"]

    #Se calculan la cantidad de codes y pairs in metrics por fila
    df["count_codes"] = df["codes"].apply(lambda x: len(x.split(",")))
    df["count_metrics"] = df["metrics"].apply(lambda x: len(x.split(",")))

    #Se eliminan las columnas codes y metricas ya que no son necesarias para el resultado
    df = df.drop(columns=["codes","metrics"])

    #Se crean las tuplas
    tuplas = [(letter,codes,metrics) for letter,codes,metrics in df.itertuples(index=False)]

    return tuplas
