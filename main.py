from dotenv import load_dotenv
import os
from ingestion.bigquery_connector import BigQueryConnector

# load environment variables from .env
load_dotenv()

# build config from .env
config = {
    "credentials_path": os.getenv("GCP_CREDENTIALS_PATH"),
    "project_id": os.getenv("GCP_PROJECT_ID")
}

if __name__ == "__main__":
    print("Starting ingestion...")

    # initialize connector with config
    connector = BigQueryConnector(config=config)

    # pull data
    df = connector.extract(
        date_from="2023-01-01",
        date_to="2024-12-31"
    )

    print(f"Ingestion complete. {len(df)} rows pulled.")
