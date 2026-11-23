import pandas as pd
import numpy as np
import os.path

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER,"submission")

def entry_day_function(data1,data2):
    """
    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
               domingo, con los dos canales juntos: `day_name`, `requests`,
               `median_calendar_days` y `median_business_days`.
        
    """
    data = pd.concat([data1,data2],ignore_index=True)

    data = calculos(data)

    entry_day = data.groupby("day_name",as_index=False).agg(requests = ("record_id","size"),
                                                            median_calendar_days = ("calendar_days","median"),
                                                            median_business_days = ("business_days","median"))

    entry_day["day_name"] = pd.Categorical(entry_day["day_name"],categories=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],ordered=True)
    return entry_day.sort_values(by="day_name")


def channel_function(data):
    requests = data.shape[0]
    answered = data["out_date"].dropna().shape[0]
    on_time_rate = data[data["business_days"] <= 15].shape[0] / data.shape[0]
    median = data["business_days"].median()
    pending = requests - answered

    return requests, answered, pending, median, on_time_rate

def yearly_function(yearly_list, channel, df):
    yearly = df.groupby(["year"],as_index=False).agg(requests = ("record_id","size"),
                                                          answered = ("out_date","count"),
                                                          on_time = ("on_time","sum")).copy()
    yearly["channel"] = channel
    yearly["pending"] = yearly["requests"] - yearly["answered"]
    yearly["on_time_rate"] = yearly["on_time"] / yearly["requests"]
    yearly_list.append(yearly)


def calculos(data):
    data = data.drop_duplicates().copy()
    data["in_date"] = pd.to_datetime(data["in_date"]).dt.normalize()
    data["out_date"] = pd.to_datetime(data["out_date"]).dt.normalize()

    respondidas = data["out_date"].notna()
    inicio = (data.loc[respondidas, "in_date"] + pd.Timedelta(days=1)).values.astype(
        "datetime64[D]"
    )
    fin = (data.loc[respondidas, "out_date"] + pd.Timedelta(days=1)).values.astype(
        "datetime64[D]"
    )

    data["business_days"] = np.nan
    data.loc[respondidas, "business_days"] = np.busday_count(inicio, fin)
    data["calendar_days"] = (data["out_date"] - data["in_date"]).dt.days
    data["year"] = data["in_date"].dt.year
    data["on_time"] = data["business_days"] <= 15

    return data


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    file1 = os.path.join(DATA_FOLDER,"historical_requests_letter.csv.gz")
    file2 = os.path.join(DATA_FOLDER,"historical_requests_web.csv.gz")

    letter = pd.read_csv(file1)
    web = pd.read_csv(file2)

    data_dic = {"letter":letter, "web": web}

    channel_summary = pd.DataFrame(columns=["channel","requests","answered","pending","median_business_days","on_time_rate"])
    yearly_list = []




    for channel,df in data_dic.items():
        df = calculos(df)
        requests,answered,pending,median_business_days,on_time_rate = channel_function(df)

        new_register_channel = pd.DataFrame({"channel":[channel],"requests":[requests],"answered":[answered],
                                             "pending":[pending],"median_business_days":[median_business_days],
                                             "on_time_rate":[on_time_rate]})
        channel_summary = pd.concat([channel_summary,new_register_channel],ignore_index=True)        
    
        #Creación dataframe yearly_summary
        if channel == "letter":
          yearly_function(yearly_list, channel, df)
        else:
          yearly_function(yearly_list,channel,df)




    yearly_summary = pd.concat(yearly_list,ignore_index=True)
    yearly_summary = yearly_summary.sort_values(by = ["year","channel"])
    yearly_summary = yearly_summary[["year","channel","requests","pending","on_time_rate"]]

    #Se exportan los archivos en csv
    channel_summary.to_csv(os.path.join(SUBMISSION_FOLDER,"channel_summary.csv"),index=False)
    yearly_summary.to_csv(os.path.join(SUBMISSION_FOLDER,"yearly_summary.csv"),index=False)
    entry_day_function(letter,web).to_csv(os.path.join(SUBMISSION_FOLDER,"entry_day_summary.csv"),index=False)

    return "Operación exitosa"


    
if __name__ == "__main__":
    print(pregunta_01())
    
