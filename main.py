from dotenv import load_dotenv
import os
from ingestion.bigquery_connector import BigQueryConnector
from ingestion.csv_connector import CSVConnector

# load environment variables from .env
load_dotenv()

# build config from .env
config = {
    "credentials_path": os.getenv("GCP_CREDENTIALS_PATH"),
    "project_id": os.getenv("GCP_PROJECT_ID")
}

if __name__ == "__main__":

    # --- LAYER 1: INGESTION ---
    print("=" * 40)
    print("LAYER 1: Ingestion starting...")
    print("=" * 40)

    # TheLook via BigQuery
    bq_connector = BigQueryConnector(config=config)
    df_thelook = bq_connector.extract(
        date_from="2023-01-01",
        date_to="2024-12-31"
    )
    print(f"TheLook: {len(df_thelook)} rows pulled.")

    # Amazon via CSV
    csv_connector = CSVConnector(config={})
    df_amazon = csv_connector.extract(
        file_path="data/Amazon Sale Report.csv",
        source_name="amazon"
    )
    print(f"Amazon: {len(df_amazon)} rows pulled.")

    # Dirty Financial via CSV
    df_dirty = csv_connector.extract(
        file_path="data/dirty_financial_transactions.csv",
        source_name="dirty_financial"
    )
    print(f"Dirty Financial: {len(df_dirty)} rows pulled.")

    print("Ingestion complete.")

    # --- LAYER 2: MEDIATION --- (coming soon)
    # --- LAYER 3: DETECTION --- (coming soon)
    # --- LAYER 4: SCORING ---   (coming soon)
    # --- LAYER 5: DASHBOARD --- (coming soon)
