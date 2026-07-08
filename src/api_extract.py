from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
import pandas as pd
import logging

import json
import requests

logging.basicConfig(level=logging.INFO)

def get_database_url() -> str:
    load_dotenv()

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    get_database_url()
)

raw_path = os.getenv("RAW_DATA_PATH")
output_path = os.getenv("OUTPUT_DATA_PATH")
url = os.getenv("API_URL")

def extract_from_api(url:str, path:str) -> pd.DataFrame:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response. json()
            # print(json.dumps(data, indent=2)[:500])
        
            raw_file = f"{path}data.json"
            with open(f"{raw_file}", "w") as f:
                json.dump(data, f, indent=2)
            print(f"Save RAW JSON to {raw_file}")

            df = pd.json_normalize(data)

            return df
        else:
            print(f"Request failed with status: {response.status_code}")
    except requests.RequestException as exc:
        print(f"Network error: {exc}")

df_raw = extract_from_api(url, raw_path)

 
def transform_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # df["Customer Name"] = (df["Customer Name"].str.strip().str.title())
    # df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    # df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    # df["status"] = df["status"].fillna("unknown").str.lower().str.strip()
    # df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    # df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    # df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")

    df_exploded = df.explode("items")
    df_items = pd.json_normalize(df_exploded["items"])
    # df = df_items

    return df_items 

df_cleaned = transform_raw_data(df_raw).sort_values("id").drop_duplicates("id", keep="last")
# print(df_cleaned.columns)

if engine:
    if not df_cleaned.empty:

        # last_id = df_cleaned["id"].iloc[-1]

        df_delta = df_cleaned

        rows_to_load = len(df_delta)
        print(rows_to_load)
        if rows_to_load > 0:
            # print(f"{output_path}")
            output_file = f"{output_path}data_cleaned.csv"
            df_delta.to_csv(f"{output_file}", index=False)
            print(f"Save CSV to {output_file}")

""" if engine:
    logging.info("Database connection established successfully.")
    if not df_cleaned.empty:
        logging.info("Data transformation completed successfully.")
        last_loaded_timestamp = get_last_loaded_timestamp(engine, "stg_orders")
        
        df_delta = df_cleaned[df_cleaned["updated_at"] > last_loaded_timestamp].copy()

        rows_to_load = len(df_delta)
        if rows_to_load > 0:
            df_delta["etl_insert_timestamp"] = pd.Timestamp.now()
            df_delta.to_csv(f"{output_path}orders_cleaned.csv", index=False)
            df_delta.to_sql("stg_orders", engine, if_exists="append", index=False)
            
            log_etl_activity(engine, source="orders_dirty.csv", rows_affected=rows_to_load, status="success")
            logging.info(f"Loaded {rows_to_load} new rows into the database.")

        else:
            logging.info("No new data to load. Skipping database update.")
            log_etl_activity(engine, source="orders_dirty.csv", rows_affected=0, status="no new data")

    # df_cleaned.to_sql(
    # "stg_orders",
    # engine,
    # if_exists="replace",
    # index=False)
    # logging.info("Loaded to postgres successfully.")

    # df_cleaned.to_sql(
    # "raw_api_orders",
    # engine,
    # if_exists="append",
    # index=False,
    # method="multi"
# ) """

if __name__ == "_main_":
    main()