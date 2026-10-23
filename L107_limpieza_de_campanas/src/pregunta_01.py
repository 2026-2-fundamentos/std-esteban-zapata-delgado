import pandas as pd
import os.path
import glob

ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER,"data")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER,"submission")
TEMP_FOLDER = os.path.join(ACTIVITY_FOLDER,"temp")

def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    #Leer y concatenar todos los archivos CSV comprimidos (.csv.gz)
    files = glob.glob(os.path.join(DATA_FOLDER, "bank-marketing-campaing-*.csv.gz"))
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)

    #Creación de la tabla client
    client_df = df[["client_id", "age","job", "marital", "education","credit_default","mortgage"]].copy()
    client_df["job"] = client_df["job"].str.strip().str.replace(".","",regex=False).str.replace("-","_",regex=False)
    client_df["education"] = client_df["education"].str.strip().str.replace(".","_",regex=False).replace("unknown",pd.NA)
    client_df["credit_default"] = (client_df["credit_default"]=="yes").astype(int)
    client_df["mortgage"] = (client_df["mortgage"]=="yes").astype(int)

    #Creación de la tabla campaign
    campaign_df = df[["client_id", "number_contacts", "contact_duration",
           "previous_campaign_contacts", "previous_outcome", "campaign_outcome"]].copy()

    campaign_df["previous_outcome"] = (campaign_df["previous_outcome"]=="success").astype(int)
    campaign_df["campaign_outcome"] = (campaign_df["campaign_outcome"]=="yes").astype(int)

    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12",
    }
    
    months = df["month"].str.lower().map(month_map)
    days = df["day"].astype(str).str.zfill(2)

    campaign_df["last_contact_date"] = "2022-" + months + "-" + days

    #Creación de la tabla Economics
    economic_df = df[["client_id","cons_price_idx","euribor_three_months"]].copy()


    #Conversión de las tablas a csv
    if os.path.exists(SUBMISSION_FOLDER):
        for file in glob.glob(f"{SUBMISSION_FOLDER}/*"):
            os.remove(file)
    else:
        os.makedirs(SUBMISSION_FOLDER)

    client_path = os.path.join(SUBMISSION_FOLDER,"client.csv")
    client_df.to_csv(client_path,sep=",",index=False)

    campaign_path = os.path.join(SUBMISSION_FOLDER,"campaign.csv")
    campaign_df.to_csv(campaign_path,sep=",",index=False)

    economics_path = os.path.join(SUBMISSION_FOLDER,"economics.csv")
    economic_df.to_csv(economics_path,sep=",",index=False)

    return (client_df,campaign_df,economic_df)

    


if __name__ == "__main__":
    clean_campaign_data()
