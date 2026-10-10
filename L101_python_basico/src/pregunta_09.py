import os.path
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    #Se crea la variable file donde se guardan la dirección de la data y un dataframe
    file = os.path.join(DATA_FOLDER,"data.csv.gz")
    df = pd.read_csv(file,sep="\t",header=None)

    #Nos quedamos únicamente con la quinta columna y se le asigna nombre de metrics
    metrics = df.iloc[:,4]

    #Se divide cada fila por coma
    metrics = metrics.str.split(",")

    #Separamos cada elemento de las listas en filas individuales
    metrics = metrics.explode()

    #Separamos cada elemento por clave:valor
    metrics = metrics.str.split(":",expand=True)
    metrics.columns = ["key","value"]
    metrics = metrics.sort_values(by="key")
    metrics["value"] = metrics["value"].astype(int)


    #Se agrupan los datos por llave y cuantas veces aparecen
    frequency_key=metrics["key"].value_counts().sort_index()
    
    #Se crea un diccionario vacio
    dictionary = dict()

    #Se recorre y agrega las metricas con su frecuencia en el dicionario
    for key,count in frequency_key.items():
        dictionary[key]=count

    return dictionary
    