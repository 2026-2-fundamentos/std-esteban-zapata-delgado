import pandas as pd
import numpy as np
import os
import glob
import json

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")
OUTPUT_FOLDER = os.path.join(ACTIVITY_FOLDER,"temp")

def clear_folder(folder):
    if os.path.exists(folder):
        for file in glob.glob(f"{folder}/*"):
            os.remove(file)


def age_group(df):
    condiciones = [
        df["age"].between(18,29),
        df["age"].between(30,39),
        df["age"].between(40,49),
        df["age"].between(50,64)
    ]
    categorias =["18-29","30-39","40-49","50-64"]
    df["age_group"] = np.select(condiciones,categorias)
    return df

def bmi_group(df):
    # 2. Grupo de IMC (bmi_group)
    cond_bmi = [
        df["bmi"] < 18.5,
        df["bmi"].between(18.5, 25, inclusive="left"),
        df["bmi"].between(25, 30, inclusive="left"),
        df["bmi"] >= 30,
    ]
    cat_bmi = ["bajo peso", "normal", "sobrepeso", "obesidad"]
    df["bmi_group"] = np.select(cond_bmi, cat_bmi)
    return df

def children_group(df):    
    # 3. Grupo de hijos (children_group)
    cond_children = [df["children"] == 0, df["children"].between(1, 2), df["children"] >= 3]
    cat_children = ["0", "1-2", "3+"]
    df["children_group"] = np.select(cond_children, cat_children)
    return df

def with_children(df):
    return df[
        ["age_group", "sex", "bmi_group", "children_group", "region"]
    ].columns.tolist()

def without_children(df):
    return df[["age_group", "sex", "bmi_group", "region"]].columns.tolist()
    


def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir 
    qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    file = os.path.join(DATA_FOLDER, "insurance.csv.gz")
    df = pd.read_csv(file)

    clear_folder(OUTPUT_FOLDER)

    # ------------------------------------------------
    # Tarea 1: Cuasi-identificadores originales
    # ------------------------------------------------
    orig_qis = ["age", "sex", "bmi", "children", "region"]
    orig_class_sizes = df.groupby(orig_qis)[orig_qis[0]].transform("count")

    # Clave 1: original_k
    original_k = int(orig_class_sizes.min())

    # Clave 2: original_unique_records
    original_unique_records = int((orig_class_sizes == 1).sum())

    # Aplicar categorizaciones a los datos para los esquemas
    df = age_group(df)
    df = bmi_group(df)
    df = children_group(df)

    # ------------------------------------------------
    # Tarea 2: Evaluación de Esquemas (schemes)
    # ------------------------------------------------
    schemes_def = {
        "with_children": with_children(df),
        "without_children": without_children(df),
    }

    schemes = {}
    published_dfs = {}

    for scheme_name, qis in schemes_def.items():
        # quasi_identifiers
        quasi_identifiers = qis

        # equivalence_classes (clases antes de suprimir)
        equivalence_classes = int(len(df.groupby(qis)))

        # k_before_suppression
        class_sizes = df.groupby(qis)[qis[0]].transform("count")
        k_before_suppression = int(class_sizes.min())

        # Aplicar k = 5 supresión
        published_mask = class_sizes >= 5
        df_pub = df[published_mask].copy()

        # suppressed_records y published_records
        suppressed_records = int((~published_mask).sum())
        published_records = int(published_mask.sum())

        # published_classes
        published_classes = int(len(df_pub.groupby(qis)))

        # classes_without_smoker_diversity
        classes_without_smoker_diversity = int(
            (df_pub.groupby(qis)["smoker"].nunique() == 1).sum()
        )

        # records_without_smoker_diversity
        smoker_unique_per_record = df_pub.groupby(qis)["smoker"].transform(
            "nunique"
        )
        records_without_smoker_diversity = int(
            (smoker_unique_per_record == 1).sum()
        )

        # Construcción exacta en el orden de claves del esquema
        schemes[scheme_name] = {
            "quasi_identifiers": quasi_identifiers,
            "equivalence_classes": equivalence_classes,
            "k_before_suppression": k_before_suppression,
            "suppressed_records": suppressed_records,
            "published_records": published_records,
            "published_classes": published_classes,
            "classes_without_smoker_diversity": classes_without_smoker_diversity,
            "records_without_smoker_diversity": records_without_smoker_diversity,
        }

        published_dfs[scheme_name] = df_pub

    # ------------------------------------------------
    # Tarea 3: Seleccionar el esquema con menos supresiones
    # ------------------------------------------------
    selected_scheme = min(
        schemes, key=lambda s: schemes[s]["suppressed_records"]
    )
    df_selected_pub = published_dfs[selected_scheme]

    # ------------------------------------------------
    # Tarea 4: Métricas comparativas
    # ------------------------------------------------
    mean_charges_original = float(df["charges"].mean())
    mean_charges_published = float(df_selected_pub["charges"].mean())

    smoker_rate_original = float((df["smoker"] == "yes").mean())
    smoker_rate_published = float((df_selected_pub["smoker"] == "yes").mean())

    # ------------------------------------------------
    # Tarea 5: Construcción final del reporte privacy_report.json
    # (Siguiendo estrictamente la lista de claves especificada)
    # ------------------------------------------------
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published,
    }

    # Guardar reporte JSON en submission/
    submission_folder = os.path.join(ACTIVITY_FOLDER, "submission")
    os.makedirs(submission_folder, exist_ok=True)

    json_path = os.path.join(submission_folder, "privacy_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # ------------------------------------------------
    # Tarea 6: Guardar insurance_published.csv
    # ------------------------------------------------
    output_cols = schemes_def[selected_scheme] + ["smoker", "charges"]
    csv_path = os.path.join(submission_folder, "insurance_published.csv")
    df_selected_pub[output_cols].to_csv(csv_path, index=False)

    return report


if __name__ == "__main__":
    import pprint

    pprint.pprint(pregunta_01())