
"""
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """
import os.path
import glob
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")
OUTPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission")

def pregunta_01():
    # 1. Asegurar que la carpeta de destino exista
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    def load_dataset(dataset_type):
        phrases = []
        targets = []
        sentiments = ["negative", "neutral", "positive"]

        for sentiment in sentiments:
            folder_path = os.path.join(DATA_FOLDER, dataset_type, sentiment)
            
            # Ordenar alfabéticamente la lista de archivos devuelta por glob
            file_paths = sorted(glob.glob(os.path.join(folder_path, "*")))

            for file_path in file_paths:
                with open(file_path, "r", encoding="utf-8") as f:
                    phrases.append(f.read().strip())
                    targets.append(sentiment)

        return pd.DataFrame({"phrase": phrases, "target": targets})

    # 2. Generar DataFrames para train y test
    df_train = load_dataset("train")
    df_test = load_dataset("test")

    # 3. Guardar en la carpeta 'submission/' con encabezados e index=False
    df_train.to_csv(
        os.path.join(OUTPUT_FOLDER, "train_dataset.csv"),
        index=False
    )
    
    df_test.to_csv(
        os.path.join(OUTPUT_FOLDER, "test_dataset.csv"),
        index=False
    )

    return "Exito!!"

if __name__ == "__main__":
    print(pregunta_01())
    