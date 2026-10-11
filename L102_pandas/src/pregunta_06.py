import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """
    file = os.path.join(DATA_FOLDER,"tbl1.tsv")
    df = pd.read_csv(file,sep="\t")

    df["c4"] = df["c4"].apply(lambda x: x.upper())

    c4 = df["c4"].unique()

    c4 = sorted(c4)
    return c4
