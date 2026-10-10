import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    #Se crea la variable file donde se guardan la dirección de la data y un dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    df = df.iloc[:,[1,3]]
    df.columns = ["value","codes"]

    #Se separa la columna codes por ","
    df["codes"] = df["codes"].str.split(",")

    #Se le asigna un valor de fila para cada separación anterior manteniendo su mismo valor
    df = df.explode("codes")

    #Se crea el dicionario donde se guardarán los datos
    dictionary = dict()

    #Se agrupan los datos por code y se agregan al dicionario
    resultado = df.groupby(["codes"])["value"].sum().sort_index()

    for code,sum in resultado.items():
        dictionary[code] = sum

    return dictionary

print(pregunta_11())
