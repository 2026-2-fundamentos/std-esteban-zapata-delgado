import pandas as pd
import os.path
import glob
import numpy as np

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER,"submission")




def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Una autoridad aeronáutica publica cada año un ranking de aerolíneas según
    su tasa de demora, y algunas aerolíneas se quejan de que es injusto: las
    demoras se acumulan a lo largo del día, de modo que una aerolínea con
    muchos vuelos en la tarde y la noche parece peor aunque opere igual de
    bien que las de más. Su tarea es construir un ranking que tenga en cuenta
    la mezcla de horarios de cada aero  línea.

    El archivo `data/flights_by_carrier_day_hour.csv.gz` tiene los vuelos
    nacionales entre 2006 y 2008, agregados por año, mes, día de la semana,
    hora programada de salida (`scheduled_departure_hour`) y aerolínea
    (`reporting_airline`). Use las columnas `operated_flights` (vuelos
    operados) y `delayed_departure_15_flights` (vuelos que salieron con 15
    minutos o más de demora).

    Siga estos pasos:

    1. Calcule la tasa nacional de demora de cada hora programada de salida:
       vuelos demorados sobre vuelos operados, con todas las aerolíneas
       juntas.
    2. Para cada aerolínea, calcule las demoras esperadas: en cada hora,
       multiplique sus vuelos operados por la tasa nacional de esa hora, y
       sume sobre todas las horas. Son las demoras que tendría si en cada hora
       se comportara como el promedio nacional.
    3. Divida las demoras observadas entre las esperadas. Un valor mayor que 1
       significa que la aerolínea se demora más de lo que explican sus
       horarios.

    Genere dos archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `hourly_delay_rates.csv`, con una fila por hora, de 0 a 23:
       `scheduled_departure_hour`, `operated_flights`,
       `delayed_departure_15_flights` y `delay_rate`.

    2. `carrier_adjusted_delays.csv`, con una fila por aerolínea:
       `reporting_airline`, `operated_flights`,
       `delayed_departure_15_flights`, `delay_rate` (la tasa sin ajustar),
       `expected_delayed_flights`, `observed_to_expected_ratio`, `crude_rank`
       y `adjusted_rank`. Incluya solamente aerolíneas con al menos 100 000
       vuelos operados. `crude_rank` es la posición según `delay_rate` y
       `adjusted_rank` la posición según `observed_to_expected_ratio`; en
       ambos, 1 es la peor aerolínea. Ordene la tabla por `adjusted_rank`.

    Compare los dos rankings: las aerolíneas que cambian de posición son las
    que el ranking sin ajustar juzga mal por sus horarios.

    La función también debe retornar las dos tablas, en el mismo orden.

    Ejemplo del formato de `carrier_adjusted_delays.csv`:

        reporting_airline,operated_flights,...,crude_rank,adjusted_rank
        EV,819223,...,1,1
        ...
    """
    file = os.path.join(DATA_FOLDER,"flights_by_carrier_day_hour.csv.gz")

    data = pd.read_csv(file,sep=",")

    #Creación de los dataframes
    hourly_delay_rates = data_per_hour_function(data)

    carrier_adjusted_delays = data_per_airline_function(data,hourly_delay_rates)

    #Exportacion de los datos a csv
    hourly_delay_rates.to_csv(os.path.join(SUBMISSION_FOLDER,"hourly_delay_rates.csv"),index=False)
    carrier_adjusted_delays.to_csv(os.path.join(SUBMISSION_FOLDER,"carrier_adjusted_delays.csv"),index=False)

def data_per_hour_function(df):
    data_per_hour = df.groupby(["scheduled_departure_hour"],as_index=False).agg(operated_flights = ("operated_flights","sum"),
                                                              delayed_departure_15_flights = ("delayed_departure_15_flights","sum"))

    data_per_hour["delay_rate"] = data_per_hour["delayed_departure_15_flights"] / data_per_hour["operated_flights"]
    data_per_hour = data_per_hour.sort_values(by = "scheduled_departure_hour",ascending = True)
    return data_per_hour

def data_per_airline_function(df, data_per_hour):
    # 1. Agrupar vuelos operados y demorados por aerolínea y hora
    airline_hourly = df.groupby(
        ["reporting_airline", "scheduled_departure_hour"], as_index=False
    ).agg(
        operated_flights=("operated_flights", "sum"),
        delayed_departure_15_flights=("delayed_departure_15_flights", "sum"),
    )

    # 2. Traer la tasa nacional correspondiente a cada hora
    airline_hourly = pd.merge(
        airline_hourly,
        data_per_hour[["scheduled_departure_hour", "delay_rate"]],
        on="scheduled_departure_hour",
        how="left",
    )

    # 3. Calcular las demoras esperadas en cada hora (vuelos * tasa nacional de esa hora)
    airline_hourly["expected_delayed_flights"] = (
        airline_hourly["operated_flights"] * airline_hourly["delay_rate"]
    )

    # 4. Sumar sobre todas las horas para obtener el total por aerolínea
    data_per_airline = airline_hourly.groupby(
        ["reporting_airline"], as_index=False
    ).agg(
        operated_flights=("operated_flights", "sum"),
        delayed_departure_15_flights=("delayed_departure_15_flights", "sum"),
        expected_delayed_flights=("expected_delayed_flights", "sum"),
    )

    # 5. Filtrar aerolíneas con al menos 100 000 vuelos operados
    data_per_airline = data_per_airline[
        data_per_airline["operated_flights"] >= 100_000
    ].copy()

    # 6. Calcular tasa sin ajustar y ratio observado / esperado
    data_per_airline["delay_rate"] = (
        data_per_airline["delayed_departure_15_flights"]
        / data_per_airline["operated_flights"]
    )
    data_per_airline["observed_to_expected_ratio"] = (
        data_per_airline["delayed_departure_15_flights"]
        / data_per_airline["expected_delayed_flights"]
    )

    # 7. Calcular rankings (1 = peor aerolínea, por eso ascending=False; .astype(int) evita decimales)
    data_per_airline["crude_rank"] = (
        data_per_airline["delay_rate"].rank(ascending=False, method="min").astype(int)
    )
    data_per_airline["adjusted_rank"] = (
        data_per_airline["observed_to_expected_ratio"]
        .rank(ascending=False, method="min")
        .astype(int)
    )

    # 8. Ordenar por adjusted_rank y garantizar el orden exacto de columnas
    columns_order = [
        "reporting_airline",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
        "expected_delayed_flights",
        "observed_to_expected_ratio",
        "crude_rank",
        "adjusted_rank",
    ]
    data_per_airline = data_per_airline.sort_values(
        by="adjusted_rank", ascending=True
    )[columns_order]

    return data_per_airline

    df = df.copy()
    df["indicator"] = df["delayed_departure_15_flights"] / df["expected_delayed_flights"]
    return df
    
    

if __name__ == "__main__":
    pregunta_01()
