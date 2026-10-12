import os.path
import numpy as np
import pandas as pd
import re

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    #Se leen y obtienen las filas del archivo
    file_g = os.path.join(DATA_FOLDER,"clusters_report.txt")
    with open(file_g, "r", encoding="utf-8") as file:
        lines = file.readlines()

    clusters = []
    current_cluster = None

    # Expresión regular para capturar la línea inicial de cada clúster
    pattern = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$")

    # 2. Omitir las primeras 4 líneas (encabezados y separadores)
    for line in lines[4:]:
        line_str = line.rstrip()
        if not line_str.strip():
            continue

        match = pattern.match(line_str)
        if match:
            if current_cluster:
                clusters.append(current_cluster)

            cluster_id = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            palabras = match.group(4).strip()

            current_cluster = {
                "cluster": cluster_id,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "palabras": [palabras],
            }
        else:
            # Si es continuación del texto de palabras clave
            if current_cluster:
                current_cluster["palabras"].append(line_str.strip())

    if current_cluster:
        clusters.append(current_cluster)

    # 3. Formatear y limpiar las palabras clave
    data = []
    for item in clusters:
        # Unir todas las líneas de texto separadas por un espacio
        texto_unido = " ".join(item["palabras"])

        # Normalizar espacios múltiples
        texto_limpio = " ".join(texto_unido.split())

        # Quitar el punto final si existe
        if texto_limpio.endswith("."):
            texto_limpio = texto_limpio[:-1]

        data.append(
            {
                "cluster": item["cluster"],
                "cantidad_de_palabras_clave": item[
                    "cantidad_de_palabras_clave"
                ],
                "porcentaje_de_palabras_clave": item[
                    "porcentaje_de_palabras_clave"
                ],
                "principales_palabras_clave": texto_limpio,
            }
        )

    # 4. Crear y retornar el DataFrame
    df = pd.DataFrame(data)
    return df
      
