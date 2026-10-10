import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    #Se lee el archivo y se convierte en dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Se extraen los meses de la segunda columna
    meses = df[2].apply(lambda x: x.split("-")[1])

    #Se cuentan cuántos registros hay para cada fecha
    conteo_meses = meses.value_counts().sort_index()

    #Se crean las tuplas de conteo meses
    tuplas = [(mes,valor) for mes,valor in conteo_meses.items()]

    return tuplas



if __name__ =="__main__":
    print(pregunta_04())
