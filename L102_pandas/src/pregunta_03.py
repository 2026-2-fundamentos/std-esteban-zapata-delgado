import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.

    Ejemplo del formato de la respuesta:

        c1
        A     8
        B     7
        C     5
        ...
    """
    file = os.path.join(DATA_FOLDER,"tbl0.tsv")
    df = pd.read_csv(file,sep="\t")

    return df["c1"].value_counts().sort_index()


