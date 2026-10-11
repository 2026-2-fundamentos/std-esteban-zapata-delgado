import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    file1 = os.path.join(DATA_FOLDER,"tbl0.tsv")
    file2 = os.path.join(DATA_FOLDER,"tbl2.tsv")
    df1 = pd.read_csv(file1,sep="\t")
    df2 = pd.read_csv(file2,sep="\t")

    df = pd.merge(df1,df2,on="c0",how="inner")

    df = df.groupby("c1")["c5b"].sum().sort_index()
    return df

