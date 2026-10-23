import os.path
import pandas as pd

ACTIVTY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMISSION_FOLDER = os.path.join(ACTIVTY_FOLDER, "submission")
DATA_FOLDER = os.path.join(ACTIVTY_FOLDER, "data")


def pregunta_01():
    """El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de

    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los campos
    de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    # Lectura de datos
    file = os.path.join(DATA_FOLDER, "solicitudes_de_credito.csv.gz")
    data = pd.read_csv(file, sep=";", index_col=0)

    # Se crea variable data_clean que guardará el dataset limpio
    data_clean = data[[
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]].copy()

    # Se eliminan los registros nulos a excepción de la columna 'comuna_ciudadano'
    checking_columns = [
        column
        for column in data_clean.columns
        if column != "comuna_ciudadano"
    ]
    data_clean = data_clean.dropna(subset=checking_columns)

    # Las columnas tipo object se les remueve los espacios de los extremos, guiones y se convierten a minúsculas
    text_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for column in text_columns:
        data_clean[column] = (
            data_clean[column]
            .astype(str)
            .str.lower()
            .str.replace("-", " ")
            .str.replace("_", " ")
            .str.strip()
        )

    # Las columnas 'estrato' y 'monto_del_credito' se convierten a tipo entero
    data_clean["estrato"] = data_clean["estrato"].astype(int)
    data_clean["monto_del_credito"] = (
        data_clean["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

    # la columna 'fecha_de_beneficio' se convierte a fecha con su respectivo formato
    data_clean["fecha_de_beneficio"] = pd.to_datetime(
        data_clean["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce"
    ).fillna(
        pd.to_datetime(
            data_clean["fecha_de_beneficio"],
            format="%d/%m/%Y",
            errors="coerce",
        )
    )
    data_clean["fecha_de_beneficio"] = data_clean[
        "fecha_de_beneficio"
    ].dt.strftime("%Y-%m-%d")

    # Se eliminan los registros duplicados
    data_clean = data_clean.drop_duplicates()

    # Se crea el directorio de salida si no existe y se guarda el archivo limpio
    os.makedirs(SUBMISSION_FOLDER, exist_ok=True)
    output_file = os.path.join(SUBMISSION_FOLDER, "solicitudes_de_credito.csv")
    data_clean.to_csv(output_file, sep=";", index=False)



if __name__ == "__main__":
    print(pregunta_01())