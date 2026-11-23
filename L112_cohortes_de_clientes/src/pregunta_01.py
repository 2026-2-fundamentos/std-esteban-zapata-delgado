import os.path
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER, "data")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission")


def build_cohort_analysis() -> pd.DataFrame:
    """
    Construye el análisis de retención por cohortes mensuales y guarda:
    1. submission/cohort_retention.csv
    2. submission/cohort_retention_heatmap.png
    """
    file = os.path.join(DATA_FOLDER, "sales.csv.gz")
    data = pd.read_csv(file)

    # 1. Limpiar fechas y registros sin cliente o fecha válida
    data["OrderDate"] = pd.to_datetime(data["OrderDate"], errors="coerce")
    data = data.dropna(subset=["CustomerID", "OrderDate"]).copy()

    # 2. Período de orden y cohorte (mes de primera compra en formato AAAA-MM)
    data["order_period"] = data["OrderDate"].dt.to_period("M")
    data["cohort_period"] = data.groupby("CustomerID")["order_period"].transform("min")
    data["cohort_month"] = data["cohort_period"].astype(str)

    # 3. Meses transcurridos desde la primera compra
    data["period_index"] = (
        (data["order_period"].dt.year - data["cohort_period"].dt.year) * 12
        + (data["order_period"].dt.month - data["cohort_period"].dt.month)
    ).astype(int)

    # 4. Clientes distintos activos por cohorte y período
    df = (
        data.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    # 5. Tamaño de cada cohorte (clientes activos en period_index == 0) y tasa de retención
    cohort_sizes = (
        df[df["period_index"] == 0][["cohort_month", "active_customers"]]
        .rename(columns={"active_customers": "cohort_size"})
    )
    df = df.merge(cohort_sizes, on="cohort_month", how="left")
    df["retention_rate"] = df["active_customers"] / df["cohort_size"]

    # 6. Ordenar y asegurar columnas exactas
    df = (
        df[["cohort_month", "period_index", "active_customers", "cohort_size", "retention_rate"]]
        .sort_values(["cohort_month", "period_index"])
        .reset_index(drop=True)
    )

    # Asegurar que exista la carpeta submission/
    os.makedirs(SUBMISSION_FOLDER, exist_ok=True)

    # 7. Exportar CSV sin índice
    csv_path = os.path.join(SUBMISSION_FOLDER, "cohort_retention.csv")
    df.to_csv(csv_path, index=False)

    # 8. Generar mapa de calor (períodos no observados quedan como NaN -> vacíos)
    pivot = (
        df.pivot(index="cohort_month", columns="period_index", values="retention_rate")
        .sort_index(ascending=True)
    )

    fig_width = max(8, pivot.shape[1] * 0.9)
    fig_height = max(5, pivot.shape[0] * 0.55)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    im = ax.imshow(pivot.values, aspect="auto", cmap="Blues", vmin=0, vmax=1)

    ax.set_xticks(np.arange(pivot.shape[1]))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(np.arange(pivot.shape[0]))
    ax.set_yticklabels(pivot.index)

    ax.set_xlabel("Período (meses desde la primera compra)")
    ax.set_ylabel("Cohorte (AAAA-MM)")
    ax.set_title("Tasa de retención por cohorte")

    # Escribir porcentajes solo en celdas observadas (no NaN)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.iloc[i, j]
            if pd.notna(val):
                text_color = "white" if val > 0.55 else "black"
                ax.text(
                    j,
                    i,
                    f"{val * 100:.1f}%",
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=8.5,
                )

    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    cbar.set_label("Tasa de retención")

    plt.tight_layout()
    heatmap_path = os.path.join(SUBMISSION_FOLDER, "cohort_retention_heatmap.png")
    plt.savefig(heatmap_path, bbox_inches="tight", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    build_cohort_analysis()