import pandas as pd
import os.path
import numpy as np

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER,"submission")


def profitability(df):
       """
       `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
              líneas), `orders` (pedidos distintos), `sales`, `profit`,
              `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
              `loss_line_rate` y `lost_profit`.
       """
       lines = len(df)
       orders = df["Order ID"].nunique()
       sales = df["Sales"].sum()
       profit = df["Profit"].sum()
       profit_margin = profit/sales
       loss_lines = df["loss_line"].sum()
       loss_lines_rate = loss_lines/lines
       lost_profit = df[df["Profit"]<0]["Profit"].map(abs).sum()

       profitable_summary = pd.DataFrame({"lines":[lines],"orders":[orders],"sales":[sales],"profit":[profit],
                                             "profit_margin":[profit_margin],"loss_lines":[loss_lines],
                                             "loss_line_rate":[loss_lines_rate],"lost_profit":[lost_profit]})
       return profitable_summary

def discount_function(df):
       """
       `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.
       """
       discount = df.groupby(["discount_band"], as_index=False).agg(
        lines=("Sales", "count"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
      )
       losses = df[df["Profit"] < 0].groupby("discount_band")
       loss_lines_by_band = losses["Sales"].count()
       lost_profit_by_band = losses["Profit"].sum().abs()

       loss_lines = discount["discount_band"].map(loss_lines_by_band).fillna(0)
       discount["lost_profit"] = (
         discount["discount_band"].map(lost_profit_by_band).fillna(0.0)
       )

       discount["profit_margin"] = discount["profit"] / discount["sales"]
       discount["loss_line_rate"] = loss_lines / discount["lines"]

       orden_bandas = ["0%", "1%-5%", "6%-10%", "más de 10%"]
       discount["discount_band"] = pd.Categorical(
         discount["discount_band"], categories=orden_bandas, ordered=True
       )

       columnas = [
         "discount_band",
         "lines",
         "sales",
         "profit",
         "profit_margin",
         "loss_line_rate",
         "lost_profit",
       ]

       return discount.sort_values("discount_band")[columnas]


def priority_function(df):
    """
    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
         que más utilidad pierden: `Customer Segment`, `Product Category`,
         `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
         solamente segmentos con al menos 100 líneas y ordénelos por
         `lost_profit` de mayor a menor.
    """
    df = df.copy()
    df["lines"] = 1
    df["perdidas"] = np.where(df["Profit"] < 0, df["Profit"].abs(), 0.0)

    grouped = df.groupby(["Customer Segment", "Product Category"], as_index=False).agg(
        lines=("lines", "sum"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        lost_profit=("perdidas", "sum"),
    )

    # Filtrar segmentos con al menos 100 líneas
    grouped = grouped[grouped["lines"] >= 100]

    # Ordenar de mayor a menor pérdida antes de tomar los 5 primeros
    priority = grouped.sort_values(by="lost_profit", ascending=False).head(5).copy()

    priority["profit_margin"] = priority["profit"] / priority["sales"]

    columns = [
        "Customer Segment",
        "Product Category",
        "lines",
        "sales",
        "profit",
        "profit_margin",
        "lost_profit",
    ]

    return priority[columns]       

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """
    file = os.path.join(DATA_FOLDER,"superstore_orders.csv.gz")

    data = pd.read_csv(file, sep =";",decimal=",")
    #Columnas de interes 
    columns = ["Order ID","Sales","Profit","Discount","Customer Segment","Product Category"]
    data_interes = data[columns]

   #Se crea la columna Profit Margin
    data_interes["profit_margin"] = data["Profit"] / data["Sales"]
   #Se crea la columna Loss line
    data_interes["loss_line"] = data_interes["Profit"].apply(lambda x: 1 if x<0 else 0)

    loss_line_rate = data_interes["loss_line"].sum()/data_interes.shape[0]

    lost_profit = data_interes[data_interes["Profit"]<0]["Profit"].map(abs).sum()

    def discount_band(row):
           if row ==0:
                  return "0%"
           elif row <= 0.05:
                  return "1%-5%"
           elif row <= 0.1:
                  return "6%-10%"
           else:
                  return "más de 10%"
    data_interes["discount_band"] = data_interes["Discount"].apply(discount_band)


    #Creación Dataframe profitability_summary
    profitability_summary = profitability(data_interes)
    profitability_summary.to_csv(os.path.join(SUBMISSION_FOLDER,"profitability_summary.csv"),index = False)

    #Creación DataFrame discount
    discount_summary = discount_function(data_interes)
    discount_summary.to_csv(os.path.join(SUBMISSION_FOLDER,"discount_summary.csv"),index = False)

    #Creación DatFrame priority
    priority_segments = priority_function(data_interes)
    priority_segments.to_csv(os.path.join(SUBMISSION_FOLDER,"priority_segments.csv"),index = False)


if __name__ == "__main__":
      pregunta_01()


