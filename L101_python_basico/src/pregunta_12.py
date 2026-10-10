import numpy as np
import pandas as pd
import os.path

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    #Se crea la dirección de los datos y un dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Se eliminan las columnas 2,3 y 4 ya que no son importantes para el análisis y además se asignan nombres a las columnas
    df = df.iloc[:,[0,4]]
    df.columns = ["letter","metrics"]

    #Se organiza por letra
    df = df.sort_values(by="letter")

    #Se separan las parejas key:value
    df["metrics"] = df["metrics"].str.split(",")
    df = df.explode("metrics")
    df["metrics"] = df["metrics"].str.split(":")

    #Se eliminan los valores key y se deja unicamente los valores
    df["metrics"] = df["metrics"].apply(lambda x: int(x[1]))

    #Se agrupan los datos por letter
    df = df.groupby("letter")["metrics"].sum().reset_index()

    #Se crea diccionario y se almacenan los resultados
    dictionary = dict()

    for letter,sum in df.itertuples(index=False):
        dictionary[letter] = sum
    return dictionary


