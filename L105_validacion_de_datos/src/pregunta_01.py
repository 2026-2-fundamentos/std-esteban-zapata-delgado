
import json
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    


    PROJECT_FOLDER = Path(__file__).resolve().parents[1]
    INPUT_FILE = PROJECT_FOLDER / "data" / "ventas.csv.gz"
    OUTPUT_FILE = PROJECT_FOLDER / "submission" / "data_quality_report.json"

    REQUIRED_COLUMNS = ("supplier_id", "supplier","country", "city", "purchase_date",
                        "amount", "discount", "weight","units","unit_price","contact_email")

    data = pd.read_csv(INPUT_FILE)


    #Resultados pedidos
    row_count=len(data)

    column_count = len(data.columns)

    #Preparación de los nombres de las columnas
    data.columns = (data.columns.str.strip().str.lower().str.replace(" ","_"))
    missing_required_columns = sorted(set(REQUIRED_COLUMNS)-set(data.columns))
    unexpected_columns = sorted(set(data.columns)-set(REQUIRED_COLUMNS))

    duplicate_row_count = data.duplicated().sum()

    duplicate_supplier_id_row_count = len(data[data.duplicated(subset=['supplier_id'], keep=False)])

    missing_value_count_by_column = data.isna().sum().to_dict()

    def es_correo_valido(email):
      # Si es nulo, NaN o no es texto, es inválido
      if pd.isna(email) or not isinstance(email, str):
          return False
      
      # Quitar espacios al inicio y final
      email = email.strip()
      
      # 1. Debe tener exactamente un '@'
      if email.count('@') != 1:
          return False
      
      usuario, dominio_extension = email.split('@')
      
      # 2. El usuario no puede estar vacío
      if not usuario:
          return False
      
      # 3. Debe tener al menos un punto en el dominio y partes no vacías
      if '.' not in dominio_extension:
          return False
      
      partes_dominio = dominio_extension.split('.')
      
      # Ninguna parte (dominio o extensión) debe estar vacía
      # (Evita casos como "user@domain." o "user@.com")
      if any(len(parte) == 0 for parte in partes_dominio):
          return False
          
      return True

    valid_email_count = data["contact_email"].apply(es_correo_valido).sum()
    invalid_email_count = len(data["contact_email"])-valid_email_count

    invalid_unit_count = data["units"].apply(lambda x: isinstance(x,int) and x>0).sum()

    country_values = sorted(data["country"].unique().tolist())

    data_quality_report = {
        "row_count": int(row_count),
        "column_count": int(column_count),
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": int(duplicate_row_count),
        "duplicate_supplier_id_row_count": int(duplicate_supplier_id_row_count),
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": int(invalid_email_count),
        "invalid_unit_count": int(invalid_unit_count),
        "country_values": country_values
    }

    # Crear la carpeta submission si no existe
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Escribir el reporte en formato JSON
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            data_quality_report,
            file,
            indent=2,
            ensure_ascii=False,
            default=lambda x: x.item() if isinstance(x, np.generic) else str(x)
        )

    
main()