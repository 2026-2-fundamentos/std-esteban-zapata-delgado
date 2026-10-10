import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    #Se obtiene el path de los datos y se crea un dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Se Toma la quinta columna (índice 4) y dividimos por comas
    metrics = df[4].str.split(",")

    #Se Expande las listas en filas individuales
    metrics = metrics.explode()

    #Metricas individuales por puntos
    pairs = metrics.str.split(":",expand=True)

    pairs.columns=["clave","valor"]

    #Se convierte la columna valor en entero
    pairs["valor"] = pairs["valor"].astype(int)

    #Se agrupa por clave y se calcula su mínimo y máximo
    groups = pairs.groupby(["clave"])["valor"].agg(["min","max"])

    #Se crean las tuplas
    tuples = [(key,mini,maxi) for key,mini,maxi in groups.itertuples()]
    return tuples



