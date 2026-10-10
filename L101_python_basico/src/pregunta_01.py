import os
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission")

def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.
    """
    file_path = os.path.join(DATA_FOLDER, "data.csv.gz")
    
    # 1. Usar separador de tabulación '\t'
    df = pd.read_csv(file_path, sep="\t",header=None)
    
    # 2. Tomar la segunda columna (índice 1) y calcular la suma como int
    resultado = int(df.iloc[:, 1].sum())
    
    return resultado

